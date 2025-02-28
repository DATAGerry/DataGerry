# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2025 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Process Manager
Manager for handling CMDB processes
"""
import logging
import multiprocessing
import threading
from time import sleep
from cmdb.utils.helpers import load_class
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ProcessManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ProcessManager:
    """
    Manages the lifecycle of CMDB processes

    The ProcessManager is responsible for starting, stopping, and managing these
    processes in the correct order
    """

    def __init__(self):
        """
        Initializes a new instance of ProcessManager

        This sets up the necessary attributes, including service definitions,
        process tracking lists, and a shutdown event
        """
        self.__service_defs: list[CmdbProcess] = self._initialize_service_definitions()
        self.__process_list: list[multiprocessing.Process] = []
        self.__process_controllers: list[ProcessController] = []
        self.__flag_shutdown: threading.Event = threading.Event()


    def _initialize_service_definitions(self) -> list:
        """
        Initializes the service definitions in the correct order

        Returns:
            list: A list of CmdbProcess instances defining the services to manage
        """
        return [
            CmdbProcess("webapp", "cmdb.interface.gunicorn.WebCmdbService"),
        ]


    def start_app(self) -> bool:
        """
        Starts all services defined in `__service_defs`

        This method iterates through the list of service definitions, loads
        the corresponding class, and starts a new process for each service.
        A ProcessController is also initialized to manage the process lifecycle.

        Returns:
            bool: True if all services started successfully
        """
        if not self.__service_defs:
            LOGGER.error("No service definitions found. Nothing to start.")
            return False

        for service_def in self.__service_defs:
            service_name = service_def.get_name()

            try:
                service_class = load_class(service_def.get_class())
                service_instance = service_class()

                process = multiprocessing.Process(target=service_instance.start, name=service_name)
                process.start()
                self.__process_list.append(process)
                # start process controller
                proc_controller = ProcessController(process, self.__flag_shutdown, self.stop_app)
                proc_controller.start()
                self.__process_controllers.append(proc_controller)
            except Exception as err:
                LOGGER.error("Failed to start service '%s': %s", service_name, err)
                return False

        return True


    def stop_app(self) -> None:
        """
        Stops all running services

        This method sets the shutdown flag, notifies process controllers,
        and ensures all processes are properly terminated
        """
        self.__flag_shutdown.set()
        # go through processes in different order
        for process in reversed(self.__process_list):
            if process.is_alive():
                LOGGER.info("Terminating service: %s (PID: %s)", process.name, process.pid)
                process.terminate()

        # Ensure processes have time to shut down cleanly
        sleep(1)

        # Confirm processes are stopped
        for process in reversed(self.__process_list):
            process.join(timeout=5)  # Give it some time to exit
            if process.is_alive():
                LOGGER.warning("Force killing unresponsive service: %s (PID: %s)", process.name, process.pid)
                process.kill()  # Force kill if terminate() didn't work

        # Clear process lists
        self.__process_list.clear()
        self.__process_controllers.clear()


class CmdbProcess:
    #TODO: REFACTOR-FIX
    """Definition of a CmdbProcess"""

    def __init__(self, name, classname):
        """Create a new instance

        Args:
            name(str): name of the process
            classname(str): classname of the process
        """
        self.__name = name
        self.__classname = classname


    def get_name(self):
        """return the process name

        Returns:
            str: name of the process
        """
        return self.__name


    def get_class(self):
        """return the class name

        Returns:
            str: name of the class
        """
        return self.__classname


class ProcessController(threading.Thread):
    #TODO: REFACTOR-FIX
    """Controlls the state of a process"""

    def __init__(self, process, flag_shutdown, cb_shutdown):
        """Creates a new instance
        
        Args:
            process(multiprocessingProcess): process to control
            flag_shutdown(threading.Event): shutdown flag
            cb_shutdown(func): callback function if a process crashed
        """
        super().__init__()
        self.__process = process
        self.__flag_shutdown = flag_shutdown
        self.__cb_shutdown = cb_shutdown


    def run(self):
        self.__process.join()
        # terminate app, if process crashed
        if not self.__flag_shutdown.is_set():
            self.__cb_shutdown()
