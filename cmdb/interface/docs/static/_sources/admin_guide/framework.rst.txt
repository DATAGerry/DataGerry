**************
Basic Concepts
**************

| 

Importing/Exporting Types
-------------------------
Object Types can be exported in JSON format. In the Object Types list, click on the yellow "Export" button to get a file
in JSON format. By default, all Object Types will be exported. If you only want to export specific types, select items
in the list and click on the "Export" button.

Object Types can also be imported from a JSON file. In the menu, choose "Type Import/Export" -> "Import Type" and upload
a JSON file with type definitions. During the import, you can choose, which types from the JSON file should be imported.

=======================================================================================================================

| 

=======================================================================================================================

Managing Objects
================
You can access Objects in DataGerry in several ways:

 * using the Category tree on the left side
 * using the search bar at the top

When using the Category tree, you can choose an Object Type (e.g. router) and get a list with all objects of that type.
By default, only summary fields of an object are shown in the table, with the yellow settings button, additional fields
can be faded in.

| 

=======================================================================================================================

| 

Active und Inactive Objects
---------------------------
Objects in DataGerry can be active or inactive. Inactive Objects are hidden in the WebUI and were not exported to
external systems with Exportd. By default, all new created Objects in DataGerry are active. You can set an Object to
inactive by hitting the small switch on the Object view page.

If you want to see inactive Objects in the WebUI, click on the switch under the navigation bar.

.. figure:: img/objects_active_switch.png
    :width: 300

    Figure 8: Active / Inactive objects switch

| 

=======================================================================================================================

| 

Object tables search / filter
-----------------------------

Searching a table is one of the most common user interactions with a DataGerry table, and DataGerry provides a number
of methods for you to control this interaction. There are tools for the table search(search) and for each individual
column (filter). Each search (table or column) can be marked as a regular expression (allowing you to create very complex
interactions).

| Please note that this method only applies the search to the table - it does not actually perform the search.

.. figure:: img/table_search_filter/object_table_search_initial.png
    :width: 600

    Figure 9: Unfiltered object overview

| 

Table search
^^^^^^^^^^^^
The search option offers the possibility to check the results in a table.
The search is performed across all searchable columns. If matching data is found in a column,
the entire row is matched and displayed in the result set. See Figure 10: *Search result after searching for "B"*

.. figure:: img/table_search_filter/object_table_search_result.png
    :width: 600

    Figure 10: Search result after searching for "B"

| 

Table filter
^^^^^^^^^^^^
While the search function offers the possibility to search the table,
the filter method provides the ability to search for data in a specific column.

The column searches are cumulative, so additional columns can be inserted to apply multiple individual column searches,
presenting the user with complex search options.

.. figure:: img/table_search_filter/object_table_filter_result.png
    :width: 600

    Figure 11: Filter result after filtering for "B"

The search terms within different rows are linked with each other with the condition *OR* (Figure 12: *Filtering by OR-expression*).
The search terms within a row are all linked with the condition *AND* (Figure 13: *Filter by AND-expression*).
Only the filtered objects are available for exporting the values from the current table.

.. figure:: img/table_search_filter/object_table_filter_example_1_result.png
    :width: 600

    Figure 12: Filtering by OR expression

.. figure:: img/table_search_filter/object_table_filter_example_2_result.png
    :width: 600

    Figure 13: Filtering by AND expression

|

.. note::
    Date values must be searched according to the following format:

    **Format**: *YYYY-MM-DDThh:mmZ*

    **Example**: *2019-12-19T11:02*

| 

=======================================================================================================================

| 

Bulk change of Objects
----------------------
The bulk change is a function in DataGerry with which several objects can be changed in one step
on the basis of change templates. With this change, the selected objects adopt the field values of the change template.


**Start**

Simply select all objects you want to change and click on the yellow button for mass changes above the list.

.. figure:: img/objects_bulk_change_list.png
    :width: 600

    Figure 14: Select objects for bulk change

**Template**

A change template is generated based on the assigned object type. The following change template is identical
to the creation of a regular object. Store all contents that you want to
transfer to the objects later and save your entries.

.. figure:: img/objects_bulk_change_active.png
    :width: 600

    Figure 15: Change template

**Preview**:

In the preview, all changes made are listed and can be adjusted again if necessary.

.. figure:: img/objects_bulk_change_preview.png
    :width: 600

    Figure 16: Overview of changes

**Result**:

After a preview, the selected objects will be changed.

.. figure:: img/objects_bulk_change_list.png
    :width: 600

    Figure 17: Bulk change result

| 

=======================================================================================================================

| 

Exporting Objects
-----------------
Objects can be exported in several formats. Currently we support:

 * CSV
 * Microsoft Excel (xlsx)
 * JSON
 * XML

To export objects, click the "Export" button in an object list and select the desired format. Only objects of a single
type can be exported (therefore you will not find the "Export" button in a list with objects of multiple types).

.. figure:: img/raw-custom-export.png
    :width: 600

    Figure 18: Export from object list overview


.. list-table:: Table 2: Supported export types
   :width: 100%
   :widths: 25 75
   :align: left
   :header-rows: 1

   * - Type
     - Description
   * - Raw Export
     - All fields of the objects are exported raw. This functionality makes it easier for the user to make some changes
       and import the changed data back into DataGerry.
   * - Customer Export
     - Only the fields selected by the user are exported. When using a quick filter in the table, only iltered objects
       are exported and only rendered fields are displayed instead of raw data.


| Export is also possible from the menu, select "Toolbox" -> "Exporter" -> "Objects".

.. figure:: img/object-import-export.png
    :width: 300

    Figure 19: Export / Import via Toolbox

| 

=======================================================================================================================

| 

Importing Objects
-----------------
To import Objects, choose "Objects Import/Export" -> "Import Objects" from the menu. Currently we support the import of
the following file formats:

 * CSV
 * JSON

To start an import, upload a file and choose the file format. Depending on the format, you have to make some settings
before an import can start.

| 

CSV Import
^^^^^^^^^^
During an import from a CSV file, a mapping of rows to object fields must be defined with a drag and drop assistent.
If the CSV file contains a header that matches the name of object fields, the mapping will be predefined in the WebUI.
Also object references can be resolved with "Foreign Keys". For example, router objects with a field "location" should
be imported. There are Location objects in DataGerry with a field "name", that contains an unique name of a Location
(e.g. FRA1). The CSV file with router Objects contains the unique location name. If you choose "foreign key:
location:name" in the mapping wizard, a reference to the correct Location object will be set during the import.

| 

JSON
^^^^
DataGerry can import Objects from a JSON file. The JSON format correspond to the format that was created when exporting
Objects.

| 