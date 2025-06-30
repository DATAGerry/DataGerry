*********
Locations
*********

**Locations** give users the possibility to structure their objects in a tree like shape where the top elements are for
example a country or a city and the sub elements are something like offices, rooms, servers etc. This will enhance the
overview as well as give the possibility to quickly find an object. The location tree can be found in the sidebar
inside the “LOCATIONS”-Tab.

.. figure:: img/locations_sidebar.png
    :width: 200
    :alt: Locations tab in sidebar

    Picture: Locations tab in sidebar

| 

=======================================================================================================================

| 

Initialise Location-Functionality for a Type
--------------------------------------------
In order to display **Objects** in the Locations-Tab the corresponding **Type** needs to have assigned the Special
Control **Location** in it's type configuration. To do this open the type overview via **Framework => Types** in the
top right corner and press the **Edit**-Icon from the **Actions**-column for the **Type** which should get the
**Locations** functionality. 

In the type configuration switch to the **Content**-Tab and on the left side in **Special Controls** drag the
**Location**-Control inside the fields-area of a section.

.. note::
  A **Location-Control** can only be assigned once to a **Type**.

.. figure:: img/locations_special_control.png
    :width: 700
    :alt: Location control in type configuration

    Picture: Location control in type configuration

The **Location**-Control contains two fields, “Label” and “Selectable as Location”. The “Label” is used in the object
overview to identify the location field and the “Selectable as Location” defines if this type can be used as a top
location for other objects .This is useful if you have a type where you don't want the have any objects below it,
for example you have a **Type** Server and a **Type** Processor. The server is the top location for the processor but
the processor can not be the top location for any other **Types**.

| 

=======================================================================================================================

| 

Configure a Location for an Object
----------------------------------

After the **Location**-Special Control has been added to the **Type**(see previous step) switch to the object overview
of an **Object** of this **Type**. The **Location**-Special Control added two fields to the **Object**. The first is
the location selection named after the "Label" which was set in the type configuration. In this field the top location
for this **Object** can be selected.The drop down list contains always the **Root**-Location which is the top most
**Location** possible. Furthermore the drop down will also contain all **Objects** which have a **Location** selected
(but not **Objects** which are directly below the current object in the **Location Tree**).

.. figure:: img/locations_dropdown_selection.png
    :width: 700
    :alt: Selection of top location for current location

    Picture: Selection of top location for current location

| 

The second added field "Label in location tree" is used to set the name of this **Object** when displayed in the
**Location tree**.

.. figure:: img/locations_added_fields.png
    :width: 700
    :alt: Added fields to object from special control “Location”

    Picture: Added fields to **Object** from **Location**-Special Control

| 

When the top location is selected and the **Object** is saved it will appear in the **Locations**-Tab in the sidebar.
Each **Object** in the **Locations**-Tab can be clicked and will open the object overview of the selected **Object**.

.. figure:: img/locations_displayed_sidebar.png
    :width: 700
    :alt: Locations in the “Locations”-Tab

    Picture: **Locations** in the **Locations**-Tab

| 