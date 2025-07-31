************************
On-Premises Installation
************************

This page provides a detailed overview of how to install DataGerry on various operating systems and platforms.

| 

=======================================================================================================================

| 

Overview
========

DataGerry can be installed in different environments depending on your use case and infrastructure preferences.
The following installation methods are supported:

- **Docker Image** (simplified deployment via containers)
- **RPM Package** (for RHEL/CentOS-based systems)
- **tar.gz Archive with Setup Script** (for Debian/Ubuntu and other distributions)
- **Deb Package** (for Debian-based systems)

For the fastest setup, we recommend using Docker along with the provided docker-compose configuration.

=======================================================================================================================

Requirements
============

DataGerry has the following system requirements:

- **Linux Operating System**
- **MongoDB 6.0** (MongoDB 4.4+ is generally compatible but not officially supported)

Although DataGerry ships with a built-in web server, it is recommended to place it behind **Nginx** for improved
performance and security.

| 

=======================================================================================================================

| 

Configuration
=============


Most of DataGerry's configuration is stored in MongoDB. However, a few parameters—such as the MongoDB connection
itself must be defined outside the database. These settings are provided in an INI-style configuration file
named ``cmdb.conf``.

Example:

.. include:: ../../../etc/cmdb.conf
    :literal:

You can also override configuration options using environment variables:

.. code-block:: bash

   DATAGERRY_<section_name>_<option_name>
   DATAGERRY_Database_port=27018

This approach is especially useful when running DataGerry in Docker environments.

| 

=======================================================================================================================

| 

Setup via Docker Image
======================

The quickest way to get started with DataGerry is using Docker. We provide a docker-compose file that sets up the
following containers:

    - **DataGerry**
    - **MongoDB**
    - **Nginx**

All data is persisted using Docker volumes on the host machine.

Start by copying the following ``docker-compose.yml`` into a new directory:

.. include:: ../../../contrib/docker/compose/ssl/docker-compose.yml
    :literal:

Create a subdirectory named ``cert`` containing your SSL certificate and key:

.. code-block:: console

    ./docker-compose.yml
    ./cert/cert.pem
    ./cert/key.pem

If SSL is not required, you can use the following simplified docker-compose file for a quick start:

.. include:: ../../../contrib/docker/compose/nossl/docker-compose.yml
    :literal:

To start the stack, run:

.. code-block:: console

    $ docker-compose up -d

You can now access the DataGerry frontend:

.. code-block:: console

    http://<host> or https://<host>
    user: admin
    password: admin

| 

Docker Images and Tags
-----------------------

DataGerry Docker images are available on `Docker Hub <https://hub.docker.com/r/becongmbh/datagerry>`_.

You can use the following tags:

- ``latest``  
  Points to the most recent stable release. Good for testing or quick setup, but it will upgrade to new major  
  versions automatically.

- ``<release>`` (e.g. ``2.2.0``)  
  Use a specific version tag for predictable behavior in production environments.

To specify a tag in your ``docker-compose.yml``:

.. code-block:: yaml

    # Replace this line
    image: becongmbh/datagerry:latest

    # With a specific release version
    image: becongmbh/datagerry:2.2.0

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Setup via RPM 
=============

For **Red Hat Enterprise Linux (RHEL)** and compatible systems like **CentOS** or **Oracle Linux**, DataGerry can
be installed using an RPM package.

Download the RPM from:  
`BuildKite RPM Package <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-rpm>`_

Supported Platforms:

    - RHEL/CentOS 9 (tested and verified)

| 

=======================================================================================================================

MongoDB Setup
-------------

DataGerry requires MongoDB 6.0. MongoDB 4.4+ may work but is not guaranteed.

Installation instructions are available here:  
`MongoDB Installation for RHEL <https://www.mongodb.com/docs/v6.0/tutorial/install-mongodb-on-red-hat/>`_

| 

=======================================================================================================================

DataGerry Installation
----------------------

Once MongoDB is installed, install the RPM package:

.. code-block:: console

    $ sudo rpm -ivh DATAGERRY-<version>.x86_64.rpm

Configure MongoDB connection settings in:

.. code-block:: console

    /etc/datagerry/cmdb.conf

Enable and start the DataGerry service:

.. code-block:: console

    $ sudo systemctl enable datagerry.service
    $ sudo systemctl start datagerry.service

You can now access the frontend:

.. code-block:: console

    http://<host>:4000
    user: admin
    password: admin

.. note::
   If the frontend is not accessible, verify that port 4000 is open in your server's firewall.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Setup via tar.gz / zip Archive
==============================

For Linux distributions that are not RPM-based, we provide a ``tar.gz`` and ``zip`` archive containing a setup script
for simplified installation. This method requires **systemd** and has been tested on the following distributions:

    - Ubuntu 20.04
    - Ubuntu 22.04

This approach should also work on other distributions that support systemd.

| 

=======================================================================================================================

MongoDB Setup
-------------

DataGerry requires **MongoDB 6.0** as its database backend. MongoDB 4.4+ is generally compatible, though not officially supported.

To install MongoDB, follow the official MongoDB guide for your platform:  
`MongoDB Installation Guide <https://www.mongodb.com/docs/v6.0/administration/install-on-linux/>`_

=======================================================================================================================

DataGerry Installation
----------------------

Download the archive from the following source:

- `BuildKite ZIP Package <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-zip>`_

Choose either the ``zip`` or ``tar.gz`` archive depending on your preference.

**Installation using zip:**

.. code-block:: console

    $ unzip datagerry-<version>.zip
    $ cd datagerry
    $ sudo ./setup.sh

**Installation using tar.gz:**

.. code-block:: console

    $ tar -xzvf datagerry-<version>.tar.gz
    $ cd datagerry
    $ sudo ./setup.sh

| 

Configuration
-------------

After the setup, configure the MongoDB connection in the configuration file:

.. code-block:: console

    /etc/datagerry/cmdb.conf

You can also override configuration values using environment variables (see the configuration section for details).

| 

Service Activation
------------------

Enable and start the DataGerry service using systemd:

.. code-block:: console

    $ sudo systemctl enable datagerry.service
    $ sudo systemctl start datagerry.service

| 

Accessing the Web Interface
---------------------------

Once started, you can access the DataGerry web interface at:

.. code-block:: console

    http://<host>:4000
    user: admin
    password: admin

.. note::
   If you are unable to access the frontend, ensure that port **4000** is open and not blocked by your system firewall.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Setup via DEB Package
=====================

For Debian-based systems, DataGerry provides a `.deb` package for easy installation.

.. note::
   You only need to install **MongoDB** separately. Other required services are included with the package.

| 

MongoDB Setup
-------------

Follow the official MongoDB guide to install MongoDB 6.0 on Debian:

`Install MongoDB on Debian <https://www.mongodb.com/docs/v6.0/tutorial/install-mongodb-on-debian/>`_

| 

DataGerry Installation
----------------------

Download the DEB package from:

- `BuildKite DEB Package <https://buildkite.com/organizations/becon-gmbh/packages/registries/datagerry-deb>`_

Navigate to the directory containing the package and run:

.. code-block:: console

    $ sudo apt install ./<datagerry-version>.deb

| 

Web Interface Access
--------------------

Once installed, you can access the DataGerry web frontend at:

.. code-block:: console

    http://<host>:4000
    user: admin
    password: admin

.. note::
   If the interface is not reachable, ensure that port **4000** is open in your firewall settings.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Nginx
-----

| 

We recommend using **Nginx** as a reverse proxy to enhance performance, enable SSL, and improve accessibility.

After installing Nginx for your platform, adapt the following configuration for your environment:

.. include:: ../../../contrib/nginx/nginx.conf
    :literal:

This setup will:

    - Listen on ports **80 (HTTP)** and **443 (HTTPS)**
    - Automatically redirect HTTP to HTTPS
    - Forward HTTPS requests from `https://<host>/` to the DataGerry backend at `http://127.0.0.1:4000`

.. tip::
   Using a reverse proxy is especially useful for integrating with Let's Encrypt, securing the UI, and supporting
   custom domains.

| 
