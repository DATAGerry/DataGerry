*************
TODO: Exports
*************

| 

=======================================================================================================================

| 

Export Types
============

| 

Types can be exported in JSON format. In the Types list, click on the yellow "Export" button to get a file
in JSON format. By default, all Object Types will be exported. If you only want to export specific types, select items
in the list and click on the "Export" button.

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

| 

Export is also possible from the menu, select "Toolbox" -> "Exporter" -> "Objects".

.. figure:: img/object-import-export.png
    :width: 300

    Figure 19: Export / Import via Toolbox

| 