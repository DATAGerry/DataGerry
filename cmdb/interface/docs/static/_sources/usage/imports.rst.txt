*******
Imports
*******

| 

=======================================================================================================================

| 

Importing Types
===============

| 

Types can also be imported from a JSON file. In the menu, choose "Type Import/Export" -> "Import Type" and upload
a JSON file with type definitions. During the import, you can choose, which types from the JSON file should be imported.

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