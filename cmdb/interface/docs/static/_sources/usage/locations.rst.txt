*********
Locations
*********

.. _locations-anchor:

**Locations** give users the possibility to structure their :ref:`Objects <objects-anchor>` in a tree like shape where
the top elements are for example a country or a city and the sub elements are something like offices, rooms, servers
etc. This will enhance the overview as well as give the possibility to quickly find an :ref:`Object <objects-anchor>`.
The location tree can be found in the sidebar inside the “LOCATIONS”-Tab.

.. figure:: img/locations/locations_sidebar.png
    :width: 200
    :alt: Locations tab in sidebar

    Picture: Locations tab in sidebar

| 

=======================================================================================================================

| 

Initialise location for a type
------------------------------

In order to display :ref:`Objects <objects-anchor>` in the Locations-Tab the corresponding :ref:`Type <types-anchor>`
needs to have assigned the Special Control **Location** in it's type configuration. To do this open the type overview
via **Framework => Types** in the top right corner and press the **Edit**-Icon from the **Actions**-column for the
:ref:`Type <types-anchor>` which should get the **Locations** functionality.

In the type configuration switch to the **Content**-Tab and on the left side in **Special Controls** drag the
**Location**-Control inside the fields-area of a section.

.. note::
  A **Location-Control** can only be assigned once to a :ref:`Type <types-anchor>`

.. figure:: img/locations/locations_special_control.png
    :width: 700

    Picture: Location control in type configuration

The **Location**-Control contains two fields, **“Label”** and **“Selectable as Location”**. The **“Label”** is used
in the object overview to identify the location field and the **“Selectable as Location”** defines if this
:ref:`Type <types-anchor>` can be used as a top location for other :ref:`Objects <objects-anchor>`. This is useful
if you have a :ref:`Type <types-anchor>` where you don't want them to have any :ref:`Objects <objects-anchor>` below
it, for example you have a :ref:`Type <types-anchor>` Server and a :ref:`Type <types-anchor>` Processor. The server
is the top location for the Processor but the Processor can not be the top location for any other
:ref:`Types <types-anchor>`.

| 

=======================================================================================================================

| 

Configure location for object
-----------------------------

After the **Location**-Special Control has been added to the :ref:`Type <types-anchor>` (see previous step) switch to
the object overview of an :ref:`Object <objects-anchor>` of this :ref:`Type <types-anchor>`. The **Location**-Special
Control added two fields to the :ref:`Object <objects-anchor>`. The first is the location selection named after the
**"Label"** which was set in the type configuration. In this field the top location for this
:ref:`Object <objects-anchor>` can be selected.The drop down list contains always the **Root**-Location which is the
top most **Location** possible. Furthermore the drop down will also contain all :ref:`Objects <objects-anchor>` which
have a **Location** selected (but not :ref:`Objects <objects-anchor>` which are directly below the current
:ref:`Object <objects-anchor>` in the **Location Tree**).

.. figure:: img/locations/locations_dropdown_selection.png
    :width: 700

    Picture: Selection of top location for current location

| 

The second added field **"Label in location tree"** is used to set the name of this :ref:`Object <objects-anchor>`
when displayed in the **Location tree**.

.. figure:: img/locations/locations_added_fields.png
    :width: 700
    :alt: Added fields to object from special control “Location”

    Picture: Added fields to :ref:`Object <objects-anchor>` from **Location**-Special Control

| 

When the top location is selected and the :ref:`Object <objects-anchor>` is saved it will appear in the
**Locations**-Tab in the sidebar. Each :ref:`Object <objects-anchor>` in the **Locations**-Tab can be clicked
and will open the object overview of the selected :ref:`Object <objects-anchor>`.

.. figure:: img/locations/locations_displayed_sidebar.png
    :width: 700
    :alt: Locations in the “Locations”-Tab

    Picture: **Locations** in the **Locations**-Tab

| 