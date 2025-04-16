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
Registration of all REST API Routes for the FlaskApp
"""
import logging
import sys
from flask_cors import CORS

from cmdb.database import MongoDatabaseManager
from cmdb.database.database_services import (
    get_db_names_from_service_portal,
    CollectionValidator,
    DatabaseUpdater,
)

import cmdb
from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.config import app_config
from cmdb.interface.custom_converters import RegexConverter
from cmdb.interface.rest_api.responses.error_handlers import (
    internal_server_error,
    page_gone,
    not_acceptable,
    method_not_allowed,
    page_not_found,
    forbidden,
    unauthorized,
    bad_request,
    service_unavailable,
)

from cmdb.manager.system_manager.system_config_reader import SystemConfigReader
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
def create_rest_api(database_maanger: MongoDatabaseManager) -> BaseCmdbApp:
    """
    Initialisation of the Flask App

    Args:
        database_manager (MongoDatabaseManager): Manager which handles the Database connection

    Returns:
        BaseCmdbApp: The Flask App
    """
    # dbm = MongoDatabaseManager(
    #     **SystemConfigReader().get_all_values_from_section('Database')
    # )

    app = BaseCmdbApp(__name__, database_manager=database_maanger)
    app.url_map.strict_slashes = True

    # Import App Extensions
    CORS(app=app, expose_headers=['X-API-Version', 'X-Total-Count'])

    if cmdb.__MODE__ == 'DEBUG':
        config = app_config['development']
        app.config.from_object(config)
    elif cmdb.__MODE__ == 'TESTING':
        config = app_config['testing']
        app.config.from_object(config)
    else:
        config = app_config['production']
        app.config.from_object(config)

    with app.app_context():
        register_converters(app)
        register_error_pages(app)
        register_blueprints(app)

        if cmdb.__MODE__ != 'TESTING':
            try:
                LOGGER.info("Starting DataGerry Routine!")

                if not cmdb.__CLOUD_MODE__:
                    start_datagerry_setup(database_maanger)
                elif not cmdb.__LOCAL_MODE__:
                    # Check for updates in __CLOUD_MODE__
                    execute_update_checks(database_maanger)
                else:
                    pass # LOCAL_MODE does not need to run updates
            except Exception as err:
                LOGGER.error(
                    "Initialisation of DataGerry failed. Exception: %s. Type: %s", err, type(err), exc_info=True
                )
                sys.exit(1)

    return app


def register_converters(app: BaseCmdbApp):
    """
    Registers a Regex converter in the Flask App

    Args:
        app (BaseCmdbApp): The Flask App
    """
    app.url_map.converters['regex'] = RegexConverter


#pylint: disable=too-many-locals
#pylint: disable=too-many-statements
def register_blueprints(app: BaseCmdbApp):
    """
    Registers API routes for the app

    Params:
        app (BaseCmdbApp): Flask app where the API routes will be registered
    """
    #pylint: disable=import-outside-toplevel
    from cmdb.interface.rest_api.routes.auth_routes import auth_blueprint
    from cmdb.interface.rest_api.routes.system_routes.setup_routes import setup_blueprint
    from cmdb.interface.rest_api.routes.settings_routes.date_routes import date_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.objects_routes import objects_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.object_links_routes import links_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.types_routes import types_blueprint
    from cmdb.interface.rest_api.routes.connection import connection_routes
    from cmdb.interface.rest_api.routes.framework_routes.categories_routes import categories_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.location_routes import location_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.section_template_routes import section_template_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.users_routes import users_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.user_settings_routes import user_settings_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.groups_routes import groups_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.rights_routes import rights_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.search_routes import search_blueprint
    from cmdb.interface.rest_api.routes.exporter_routes.exporter_object_routes import exporter_blueprint
    from cmdb.interface.rest_api.routes.exporter_routes.exporter_type_routes import type_export_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.logs_routes import logs_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.setting_routes import settings_blueprint
    from cmdb.interface.rest_api.routes.importer_routes.import_routes import importer_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.docapi_routes import docapi_blueprint, docs_blueprint
    from cmdb.interface.rest_api.routes.media_library_routes.media_file_routes import media_file_blueprint
    from cmdb.interface.rest_api.routes.framework_routes.special_routes import special_blueprint
    from cmdb.interface.rest_api.routes.report_routes.report_category_routes import report_categories_blueprint
    from cmdb.interface.rest_api.routes.report_routes.report_routes import reports_blueprint
    from cmdb.interface.rest_api.routes.webhook_routes.webhook_routes import webhook_blueprint
    from cmdb.interface.rest_api.routes.webhook_routes.webhook_event_routes import webhook_event_blueprint
    from cmdb.interface.rest_api.routes.relation_routes.relations_routes import relations_blueprint
    from cmdb.interface.rest_api.routes.relation_routes.object_relation_routes import object_relations_blueprint
    from cmdb.interface.rest_api.routes.log_routes.object_relation_logs_routes import object_relation_logs_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.persons_routes import person_blueprint
    from cmdb.interface.rest_api.routes.user_management_routes.person_groups_routes import person_group_blueprint
    from cmdb.interface.rest_api.routes.importer_routes.importer_isms_routes import isms_importer_blueprint
    from cmdb.interface.rest_api.routes.framework_routes import (
        extendable_option_blueprint,
        object_group_blueprint,
    )
    from cmdb.interface.rest_api.routes.isms_routes import (
        risk_class_blueprint,
        likelihood_blueprint,
        impact_blueprint,
        impact_category_blueprint,
        protection_goal_blueprint,
        risk_matrix_blueprint,
        isms_config_blueprint,
        threat_blueprint,
        vulnerability_blueprint,
        risk_blueprint,
        control_meassure_blueprint,
        risk_assessment_blueprint,
        control_meassure_assignment_blueprint,
    )

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(setup_blueprint, url_prefix='/setup')
    app.register_blueprint(date_blueprint, url_prefix='/date')
    app.register_blueprint(objects_blueprint, url_prefix='/objects')
    app.register_blueprint(links_blueprint, url_prefix='/objects/links')
    app.register_blueprint(types_blueprint, url_prefix='/types')
    app.register_blueprint(connection_routes)
    app.register_blueprint(categories_blueprint, url_prefix='/categories')
    app.register_blueprint(location_blueprint, url_prefix='/locations')
    app.register_blueprint(section_template_blueprint, url_prefix='/section_templates')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(user_settings_blueprint, url_prefix='/users/<int:user_id>/settings')
    app.register_blueprint(groups_blueprint, url_prefix='/groups')
    app.register_blueprint(rights_blueprint, url_prefix='/rights')
    app.register_blueprint(search_blueprint)
    app.register_blueprint(exporter_blueprint, url_prefix='/exporter')
    app.register_blueprint(type_export_blueprint)
    app.register_blueprint(logs_blueprint, url_prefix='/logs')
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(importer_blueprint)
    app.register_blueprint(docapi_blueprint)
    app.register_blueprint(docs_blueprint, url_prefix='/docs')
    app.register_blueprint(media_file_blueprint)
    app.register_blueprint(special_blueprint)
    app.register_blueprint(report_categories_blueprint, url_prefix='/report_categories')
    app.register_blueprint(reports_blueprint, url_prefix='/reports')
    app.register_blueprint(webhook_blueprint, url_prefix='/webhooks')
    app.register_blueprint(webhook_event_blueprint, url_prefix='/webhook_events')
    app.register_blueprint(relations_blueprint, url_prefix='/relations')
    app.register_blueprint(object_relations_blueprint, url_prefix='/object_relations')
    app.register_blueprint(object_relation_logs_blueprint, url_prefix='/object_relation_logs')
    app.register_blueprint(extendable_option_blueprint, url_prefix='/extendable_options')
    app.register_blueprint(object_group_blueprint, url_prefix='/object_groups')
    app.register_blueprint(person_blueprint, url_prefix='/persons')
    app.register_blueprint(person_group_blueprint, url_prefix='/person_groups')

    # ISMS Blueprints
    app.register_blueprint(isms_config_blueprint, url_prefix='/isms/config')
    app.register_blueprint(risk_class_blueprint, url_prefix='/isms/risk_classes')
    app.register_blueprint(likelihood_blueprint, url_prefix='/isms/likelihoods')
    app.register_blueprint(impact_blueprint, url_prefix='/isms/impacts')
    app.register_blueprint(impact_category_blueprint, url_prefix='/isms/impact_categories')
    app.register_blueprint(protection_goal_blueprint, url_prefix='/isms/protection_goals')
    app.register_blueprint(risk_matrix_blueprint, url_prefix='/isms/risk_matrix')
    app.register_blueprint(threat_blueprint, url_prefix='/isms/threats')
    app.register_blueprint(vulnerability_blueprint, url_prefix='/isms/vulnerabilities')
    app.register_blueprint(risk_blueprint, url_prefix='/isms/risks')
    app.register_blueprint(control_meassure_blueprint, url_prefix='/isms/control_meassures')
    app.register_blueprint(risk_assessment_blueprint, url_prefix='/isms/risk_assessments')
    app.register_blueprint(control_meassure_assignment_blueprint, url_prefix='/isms/control_meassure_assignments')
    app.register_blueprint(isms_importer_blueprint, url_prefix='/isms/importer')

    if cmdb.__MODE__ == 'DEBUG':
        from cmdb.interface.rest_api.routes.debug_routes import debug_blueprint
        app.register_blueprint(debug_blueprint)

    # LOGGER.debug(f"routes: {app.url_map}")

def register_error_pages(app: BaseCmdbApp):
    """
    Registers error handlers for the app

    Params:
        app (BaseCmdbApp): Flask app where the error handlers will be registered
    """
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(406, not_acceptable)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(503, service_unavailable)

# -------------------------------------------------------------------------------------------------------------------- #

def start_datagerry_setup(dbm: MongoDatabaseManager) -> None:
    """
    Setup of DataGerry and runs database updates

    Args:
        dbm (MongoDatabaseManager): Manager for interaction with database
    """
    db_name = SystemConfigReader().get_value('database_name', 'Database')

    CollectionValidator(db_name, dbm, local_mode=True).validate_collections()

    database_updater = DatabaseUpdater(dbm, db_name)

    if database_updater.is_update_available():
        database_updater.run_updates()


def execute_update_checks(dbm: MongoDatabaseManager) -> None:
    """
    Setup of DataGerry and runs database updates

    Args:
        dbm (MongoDatabaseManager): Manager for interaction with database
    """
    # First retrieve all database names
    db_names = get_db_names_from_service_portal()

    # # Check each database if it is up to date
    for db_name in db_names:
        # Validate Collections
        CollectionValidator(db_name, dbm).validate_collections()

        database_updater = DatabaseUpdater(dbm, db_name)

        if database_updater.is_update_available():
            database_updater.run_updates()
