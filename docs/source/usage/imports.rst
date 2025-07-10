*******
Imports
*******

| 

The **Importer** section, accessible via **Toolbox --> Importer**, allows users to import various types of data into
the system through guided import procedures.

Upon navigating to the Importer, users are presented with a set of buttons—each representing a distinct type of
importable entity. Clicking a button will initiate a dedicated import workflow, typically involving steps such as
uploading a file, mapping fields, validating content, and confirming the import.

| 

=======================================================================================================================

| 

Available Import Options
========================

The following entities can be imported via the Toolbox:

- **Objects**  
  Allows the import of :ref:`Objects <objects-anchor>` such as servers, applications, or other infrastructure elements
  into the CMDB

- **Types**  
  Enables import of custom :ref:`Types <types-anchor>`, including their attributes and structural definitions

- **Threats**  
  Used to bulk import :ref:`Threats <isms-threat-anchor>` into the :ref:`ISMS <isms-anchor>` module. This is useful
  for initializing the :ref:`Threats <isms-threat-anchor>` catalog based on external standards or regulations

- **Vulnerabilities**  
  Allows the import of :ref:`Vulnerabilities <isms-vulnerability-anchor>` into the ISMS module which can be linked
  to :ref:`Threats <isms-threat-anchor>` and used in risk analysis

- **Controls**  
  Supports importing :ref:`Controls <isms-controls-anchor>` into the :ref:`ISMS <isms-anchor>` module such as security
  requirements or compliance rules (e.g., ISO 27001, NIST)

- **Risks**  
  Enables importing :ref:`Risks <isms-risk-anchor>` into the :ref:`ISMS <isms-anchor>` module

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Objects
=================
To import :ref:`Objects <objects-anchor>`, navigate to **Toolbox -> Importer** and click on the **Import Objects**
button. This will open the object import workflow, where you can upload your data and configure the import process.

Currently we support the import ofthe following file formats:

 * CSV
 * JSON

| 


Import Steps
------------

The object import is performed in 5 structured steps:

1. **File Format and Upload**  
   Choose the file format (**CSV** or **JSON**) and upload the file to be imported.

2. **File Configuration**  
   Depending on the selected format, various configuration options are available with default values

3. **Type Mapping**  
   - Select the :ref:`Type <types-anchor>` into which the data will be imported.
   - If importing from CSV, use the drag-and-drop assistant to map file columns to object fields.
   - Foreign keys (references to other objects) can also be configured here.

4. **Import Configuration**  
   Specify how to handle existing :ref:`Objects <objects-anchor>`:
   - If an :ref:`Object <objects-anchor>` with the same `public_id` already exists, choose whether it
   - should be updated or created
   - It is possible to limit the amount of imported :ref:`Objects <objects-anchor>`

1. **Review and Import**  
   A final overview displays the number of :ref:`Objects <objects-anchor>` ready for import.
   After confirming everything is correct, click **Start Import** to complete the process.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Types
===============

| 

Types can also be imported using a JSON file. To do this, navigate to **Toolbox -> Importer** and select the
**Import Types** option. Upload a JSON file containing one or more :ref:`Type <types-anchor>` definitions. During the
import process, the system will display all available :ref:`Types <types-anchor>` within the file, and you can choose
which specific :ref:`Types <types-anchor>` you want to import. This allows for selective importing and easy reuse of
exported :ref:`Type <types-anchor>` configurations.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Threats
=================

To import :ref:`Threats <isms-threat-anchor>`, go to **Toolbox -> Importer** and select the **Import Threats** option.
You can upload a CSV file to import multiple :ref:`Threats <isms-threat-anchor>` in a single operation. Please follow
the structure and rules below to ensure a successful import.

| 

CSV File Format
---------------

- Supported delimiters: `,` (comma) or `;` (semicolon)
- The first row must contain the column headers

| 

Required and Optional Headers
-----------------------------

The CSV file should include the following headers:

.. list-table:: CSV Headers for Threat Import
   :widths: 20 10 70
   :header-rows: 1

   * - Header
     - Required
     - Description
   * - ``name``
     - Yes (*)
     - The name of the Threat.
   * - ``source``
     - No
     - The source of the Threat. If the specified source does not exist, it will be created automatically.
   * - ``identifier``
     - No
     - An optional identifier for the Threat.
   * - ``description``
     - No
     - A detailed description of the Threat.

| 

Source Mapping
--------------

| 

The value provided in the ``source`` field is matched against existing Threat Sources by **name**.
This comparison is **case-sensitive**. For example, ``SourceA`` and ``sourcea`` are treated as different sources.
If no match is found, a new Source will be created automatically.

| 

Duplicate Handling
------------------

Before creating a new :ref:`Threat <isms-threat-anchor>`, the system performs a **case-sensitive comparison**
across all fields. A Threat will only be created if **no identical entry** already exists in the database.
This ensures that importing the same CSV file multiple times will not result in duplicate entries.

| 

Example CSV Content
-------------------

.. code:: bash

   name;source;identifier;description
   Threat1;Source1;Identifier1;Description1
   Threat2;Source2;Identifier2;Description2

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Vulnerabilities
==========================

To import :ref:`Vulnerabilities <isms-vulnerability-anchor>`, go to **Toolbox -> Importer** and select the
**Import Vulnerabilities** option. You can upload a CSV file to import multiple
:ref:`Vulnerabilities <isms-vulnerability-anchor>` at once. Follow the guidelines below to ensure a successful import
process.

| 

CSV File Format
---------------

- Supported delimiters: `,` (comma) or `;` (semicolon)
- The first row must contain the column headers.

| 

Required and Optional Headers
-----------------------------

Your CSV file should contain the following headers:

.. list-table:: CSV Headers for Vulnerability Import
   :widths: 20 10 70
   :header-rows: 1

   * - Header
     - Required
     - Description
   * - ``name``
     - Yes (*)
     - The name of the Vulnerability.
   * - ``source``
     - No
     - The source of the Vulnerability. If the specified source does not exist, it will be created automatically.
   * - ``identifier``
     - No
     - An optional identifier for the Vulnerability.
   * - ``description``
     - No
     - A detailed description of the Vulnerability.

| 

Source Mapping
--------------

The value in the ``source`` field is matched against existing Vulnerability Sources by **name**. This match
is **case-sensitive**. For instance, ``VulnDB`` and ``vulndb`` are treated as different values. If no matching
source exists, one will be created during import.

| 

Duplicate Handling
------------------

Before creating a new Vulnerability, the system performs a **case-sensitive comparison** of all fields.  
A Vulnerability is only created if no exact match exists in the database.  
This means re-importing the same CSV file will **not** result in duplicate entries.

| 

Example CSV Content
-------------------

.. code-block:: bash

   name;source;identifier;description
   Vulnerability1;Source1;Identifier1;Description1
   Vulnerability2;Source2;Identifier2;Description2

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Controls
==================

To import Controls, navigate to **Toolbox -> Importer** and select the **Import Controls** import option.  
You can upload a CSV file to import multiple Controls at once. Follow the format and requirements outlined below
for a successful import.

| 

CSV File Format
---------------

- Supported delimiters: `,` (comma) or `;` (semicolon)
- The first row must contain the column headers.

| 

Required and Optional Headers
-----------------------------

The CSV file should contain the following headers:

.. list-table:: CSV Headers for Control Import
   :widths: 25 10 65
   :header-rows: 1

   * - Header
     - Required
     - Description
   * - ``title``
     - Yes (*)
     - The title or name of the Control.
   * - ``control_measure_type``
     - Yes (*)
     - The type of the Control. Allowed values: ``CONTROL``, ``REQUIREMENT``, ``MEASURE``.
   * - ``source``
     - No
     - The source of the Control. Matched case-sensitively by name.
   * - ``implementation_state``
     - No
     - The implementation status (e.g., ``Planned``, ``In Progress``, ``Implemented``). Matched case-sensitively.
   * - ``identifier``
     - No
     - An optional identifier for the Control.
   * - ``chapter``
     - No
     - A logical grouping or chapter reference, if applicable.
   * - ``description``
     - No
     - A detailed explanation of the Control.
   * - ``is_applicable``
     - No
     - Indicates if the Control is applicable.  
       Accepted truthy values: ``True``, ``true``, ``Yes``, ``yes``, ``1``  
       Accepted falsy values: ``False``, ``false``, ``No``, ``no``, ``0``  
       Unknown or invalid values will be treated as ``false``.
   * - ``reason``
     - No
     - Justification if the Control is marked as not applicable.

| 

Source and Status Mapping
-------------------------

Values in the ``source`` and ``implementation_state`` fields are matched against existing entries **by name**.  
Matching is **case-sensitive**, so for example ``Source`` is not equal to ``source``.  
If no match is found, the value will be **automatically created**.

| 

Duplicate Handling
------------------

To avoid duplicates, the system performs a **case-sensitive** comparison across **all fields**.  
A new Control is created **only** if there is no exact match already present.  
Re-importing the same CSV will **not** create duplicates.

| 

Example CSV Content
-------------------

.. code-block:: bash

   title,control_measure_type,source,implementation_state,identifier,chapter,description,is_applicable,reason
   MC1,CONTROL,MC_SOURCE,In Progress,Identifier1,Chapter1Text,Description1,true,Reason1Text
   MC2,REQUIREMENT,MC_SOURCE2,In Progress,Identifier2,Chapter2Text,Description2,no,Reason2Text

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Importing Risks
===============

To import :ref:`Risks <isms-risk-anchor>`, navigate to **Toolbox -> Importer** and select the **Import Risks** option.
A CSV file can be uploaded to import multiple Risks at once. Follow the specifications below to ensure successful
processing.

| 

CSV File Format
---------------

- Supported delimiters: `,` (comma) or `;` (semicolon)
- The first row must contain the column headers.

| 

Required and Optional Headers
-----------------------------

.. list-table:: CSV Headers for Risk Import
   :widths: 25 10 65
   :header-rows: 1

   * - Header
     - Required
     - Description
   * - ``name``
     - Yes (*)
     - The name or title of the Risk.
   * - ``risk_type``
     - No (*)
     - The type of the Risk. Allowed values: ``THREAT_X_VULNERABILITY``, ``THREAT``, ``EVENT``.
   * - ``protection_goals``
     - No
     - Related protection goals (e.g., ``Confidentiality``, ``Integrity``, ``Availability``). Use comma-separated values.
   * - ``threats``
     - No
     - Associated Threats by name. Use comma-separated values.
   * - ``vulnerabilities``
     - No
     - Linked Vulnerabilities by name. Use comma-separated values.
   * - ``identifier``
     - No
     - An identifier for the Risk.
   * - ``consequences``
     - No
     - Potential consequences if the Risk materializes.
   * - ``description``
     - No
     - A detailed explanation or context of the Risk.

| 

Source Mapping
--------------

Values in the ``protection_goals``, ``threats``, and ``vulnerabilities`` fields are matched against
existing entries **by name**. Matching is **case-sensitive** (e.g., ``Source`` ≠ ``source``).  
If no match is found, the missing entries will be **automatically created**.

| 

Duplicate Handling
------------------

The system performs a **case-sensitive** comparison across all fields to detect duplicates.  
A Risk is created **only** if an exact match does not already exist.  
Re-importing the same CSV will **not** result in duplicate entries.

| 

Special Notes Based on `risk_type`
----------------------------------

Some fields are conditionally required based on the value of the ``risk_type``:

- ``THREAT_X_VULNERABILITY``:
  - ``threats`` is **required**
  - ``vulnerabilities`` is **required**
  - ``consequences`` must be **empty**

- ``THREAT``:
  - ``threats`` is **required**
  - ``vulnerabilities`` must be **empty**
  - ``consequences`` must be **empty**

- ``EVENT``:
  - ``threats`` must be **empty**
  - ``vulnerabilities`` must be **empty**
  - ``consequences`` is **required**
  - ``description`` is **required**

| 

Example CSV Content
-------------------

.. code-block:: bash

   name;risk_type;protection_goals;threats;vulnerabilities;identifier;consequences;description
   Risk1;THREAT;Confidentiality,Integrity;Fire,Water;;Identifier1;;
   Risk2;EVENT;Integrity;;;Identifier2;Consequences2;Description2
