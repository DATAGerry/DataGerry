*************
CMDB Concepts
*************

DataGerry is a flexible asset management solution (also known as a **CMDB**) that allows users to build their
own data models by defining custom types. The core unit of data in DataGerry is the **Object**.

An **Object** represents a real-world asset or entity—such as a router, server, building, or service contract.
Each **Object** is based on a **Type**, which defines a set of **fields** representing the attributes of that
**Object**. Examples of such fields include:

    * **Hostname** (text)
    * **Maintenance Status** (checkbox)
    * **Location** (dropdown)
    * **Warranty Expiration** (date)

Each field is assigned a specific **data type**, offering a high level of flexibility for modeling any kind of
structured information. This enables teams to manage technical infrastructure, business assets, or virtually
any domain-specific data within a single platform—tailored entirely to their own requirements.

The basic concepts of **Data Structure Modeling** will be explained in more detail
in the upcoming sections.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Categories
==========

| 

**Categories** in DataGerry are used to organize **Types** by grouping them together and enhancing the organisational
overview in the sidebar. They can be structured hierarchically by assigning an existing **Category** as a parent. To
manage **Categories**, navigate to **Framework => Categories**.

| 

**Categories overview**

In the **Categories** overview, you will find the **"Category-Tree"**, which visualizes the current structure of all
**Categories**. The **"Category-List"** provides a detailed view of each existing **Category**, including information
such as PublicID and ParentID. At the top right corner, there are two buttons: the **"Add"** - Button for creating a
new **Category**, and the **"Edit"** - Button for rearranging or deleting existing **Categories** in the
**"Category-Tree"**.

.. figure:: img/categories_overview.png
    :width: 1000

    Picture: Overview of **Categories**

| 

In DataGerry, the tree structure of **Categories** and their assigned **Types** is visible in the sidebar under the
**"CATEGORIES"** tab on the left side. Any **Type** that is not assigned to a **Category** appears in the
**"UNCATEGORIZED"** section below.

.. figure:: img/categories_sidebar.png
    :width: 200

    Picture: Displayed **Categories** in the Sidebar of DataGerry

| 

=======================================================================================================================

| 

Create a Category
-----------------
To create a new **Category** click the **"+Add"**-Button in the **"Categories Overview"**. All unassigned **Types**
are displayed in the left **"Unassigned types"** overview and can be Drag/Dropped into the **"Types"** area within the
**"Basic information"** section. In the **"Basic information"**-Section it is poosible to set the following
properties:

| 

.. list-table:: Table: Fields for **Categories**
   :width: 60%
   :widths: 25 75
   :align: center
   :header-rows: 1

   * - Field
     - Description
   * - Name
     - A unique identifier for the **Category**
   * - Label
     - The displayed label of the **Category**
   * - Icon
     - The icon of the **Category** is displayed in various views , such as the sidebar
   * - Parent
     - Select the top **Category** if this one should be a sub **Category**
   * - Types
     - Drag/Drop **Types** in this section which should be grouped by this **Category**

| 

.. figure:: img/categories_add.png
    :width: 1000

    Picture: Adding a **Category**

| 

=======================================================================================================================

| 

Edit/Delete a Category
----------------------
To edit a **Category** press the **"Edit"**-Button  located in the top right corner of the **"Categories View"**.
This action will toggle the display of the **"Category-Tree"** section. Within this view, you can rearrange
the order of **Categories** by dragging and dropping the icon to the right of the **Category** - Label. Each
**Category** is accompanied by two actions: accessing its **'Edit'** form or deleting it (by clicking the
**Trash Bin** - Icon).

.. note::
    Deleting a **Category** will not delete the assigned **Types**.

.. figure:: img/categories_edit_tree.png
    :width: 1000

    Picture: Edit a **Category** in **"Category-Tree"**

| 

When editing a **Category** within the **"Edit"**-Form you can additionaly rearange the order of the assigned
**Types** as well as modify the assignments.

.. figure:: img/categories_edit_form.png
    :width: 1000

    Picture: Edit a **Category** in **"Edit"**-Form

| 

=======================================================================================================================

| 

=======================================================================================================================

Types
=====

| 

**Types** are structured entities that enclose various sections, each containing specific fields. These fields are
designed to capture and describe the attributes and characteristics of real-world objects. By organizing information
into sections, **Types** provide a systematic way to represent complex **Objects** and their properties, ensuring
consistency and clarity in data management.

**Types** serve as blueprints for **Objects**, defining the structure and characteristics each **Object** can possess.
In other words, a **Type** specifies the fields and potential values that an **Object** can include, ensuring that
all **Objects** of a particular **Type** adhere to a consistent format and set of attributes.

To manage **Types** click **Framework -> Types** in the top right corner.

.. figure:: img/types_open_menu.png
    :width: 200

    Picture: Open **Types** management

| 

=======================================================================================================================

| 

Adding a Type
-------------
The type list (**Framework -> Types**) provides an overview of all the **Types** created so far, displayed in a table
format. Above the table, there is an **"Add"** button, which opens a form for creating a new **Type**. The form consists
of several steps.

| 

**Step 1 - Basic information**

In this step you need to provide some basic information about the type:

- **Name**: A unique identifier for the **Type**
- **Label**: The displayed label of the **Type**
- **Icon**: Select an icon for the **Type** by double clicking in the name (**"fa fa-cube"**) of the default icon

Once you have completed these fields, press the **"Next Step"** button to proceed to the next step.

| 

.. figure:: img/types_create_basic_information_step.png
    :width: 800

    Picture: Type creation - Step 1

| 

**Step 2 - Content**

In this step all sections and their correspondig fields are defined for the type. In the left sidebar are several
expandable elements which provide components to build up a type by drag and drop these components inside the area
in the center:

- **Global Section Templates**: For more infomation about this section see this link: TODO: Section Templates Anchor
- **Section Templates**: For more infomation about this section see this link: TODO: Section Templates Anchor
- **Structure Controls**: These components group fields. Fields can only be placed inside of
  these **Structure Controls**. More details can be found in the table below.
- **Basic Controls**: These components are the fields with different data formats. They need to be dragged and
  dropped inside of **Structure Controls**. More details are in the table below.
- **Special Controls**: These components are also fields but with a specific purpose. More details are in the table
  below.

| 

.. note::
  After you finished Step 1 and 2, the **Type** can be saved. Steps 3 and 4 are optional to configure.

| 

.. figure:: img/types_create_content_step.png
    :width: 800

    Picture: Definition of fields for **Type** - Step 2

| 

.. list-table:: Table: Structure Controls
   :width: 80%
   :widths: 15 85
   :align: left
   :header-rows: 1

   * - Type
     - Description
   * - Section
     - A container used to group fields
   * - Multi Data Section
     - Allows saving multiple values for the defined fields. See more: TODO: MDS Anchor
   * - Reference Section
     - Binds a section with all fields of a referencing object completely as a display. The search for
       the field values is run through like a normal field. The references are expanded accordingly, so
       that a distinction is made between field references and section references.

| 

.. figure:: img/types_reference_section.png
    :width: 600

    Picture: Definition of the object fields via reference section

| 

.. list-table:: Table: Basic and Special Controls
   :width: 80%
   :widths: 15 85
   :align: left
   :header-rows: 1

   * - Type
     - Description
   * - Text
     - A text field. Content validation with regular expression is possible
   * - Password
     - password field with integrated password generator and hiding of content
   * - Textarea
     - Textbox with multiple lines
   * - Checkbox
     - A boolean checkbox
   * - Radio
     - Selection between multiple options
   * - Select
     - Selection between multiple options with a dropdown menu
   * - Date
     - A Date picker
   * - Reference
     - Reference to another **Object** of a specific **Type**. E.g. connection between a PC and a hard drive.
       Embeds a summary of a referencing **Object** as a display. The summary for each object definition is
       predefined in the type generator under the “Meta” step (TODO: Create Meta Step Anchor). With the field type
       “Reference” it is possible to override the predefined summaries and make them user specific.
   * - Location
     - Can be only used once per **Type**. Follow this link for more information: TODO: Locations Anchor

| 

.. figure:: img/special_control_field.png
    :width: 600

    Picture: Special Control - Reference

| 

**Step 3 - Meta(Optional)**

In this step the meta information of the **Type** can be set. Each object can have summary fields. These fields
summarize the **Object** and are shown by default in object lists. On a router, this could be a management ip and
a hostname. The summary fields can be set under **“Summary”**. Also, external links can be set, which are shown on
the object page to add a quick link to the WebUI of another system. An External Link has a name, a label, an icon and
the link (URL) itself. In the link, use curved brackets to access values of an **Object** field.

| 

.. figure:: img/types_create_meta_step.png
    :width: 600

    Picure: Meta information of a **Type**

| 

**Step 4 - ACL (Optional)**

In this step advanced permissions can be set for this **Type**. The default setting is set to "ACL deactivated".
More information to this topic at this link: TODO: Access Control Anchor.

| 

.. figure:: img/types_create_acl_step.png
    :width: 600

    Picure: ACL settings for the **Type**

| 

=======================================================================================================================

| 

Editing/Deleting a Type
-----------------------

The type list (**Framework => Types**) table itself contains, apart from several useful information about the created
**Types**, two columns in the end with **"Actions"** and **"Clean"**. In the **"Actions"** column it is possible to
edit, clone or delete the existing **Types**.

.. warning::
  A **Type** can only be deleted if there are no exisitng **Objects** of this **Type**

| 

In the **"Clean"** column is a button which will turn red and state **"Unclean"** if you change the **Type** schema
(by adding or deleting fields/sections) This happens only if there is at least one **Object** of this **Type**. By
pressing the **"Unclean"**-Button it lets you update all your created **Objects** of this **Type** with the changes
you applied on the **Type** (for example a newly added field to the **Type** will be added to all existing 
**Objects** of that **Type**).

.. figure:: img/types_overview.png
    :width: 600

    Picure: **Types** overview table

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

Objects
=======

| 

You can access Objects in DataGerry in several ways:

 * using the Category tree on the left side
 * using the search bar at the top

When using the Category tree, you can choose an Object Type (e.g. router) and get a list with all objects of that Type.
By default, only summary fields of an object are shown in the table, with the yellow settings button, additional fields
can be faded in.

| 

=======================================================================================================================

| 

Active und Inactive Objects
---------------------------
Objects in DataGerry can be active or inactive. Inactive Objects are hidden in the WebUI. By default, all new created
Objects in DataGerry are active. You can set an Object to inactive by hitting the small switch on the Object view page.

If you want to see inactive Objects in the WebUI, click on the switch under the navigation bar.

.. figure:: img/objects_active_switch.png
    :width: 300

    Figure 8: Active / Inactive Objects switch

| 

=======================================================================================================================

| 

Object tables search / filter
-----------------------------

Searching a table is one of the most common user interactions with a DataGerry table, and DataGerry provides a number
of methods for you to control this interaction. There are tools for the table search(search) and for each individual
column (filter). Each search (table or column) can be marked as a regular expression (allowing you to create very complex
interactions).

| 

Please note that this method only applies the search to the table - it does not actually perform the search.

| 

.. figure:: img/object_table_search_initial.png
    :width: 600

    Figure 9: Unfiltered object overview

| 

Table search
^^^^^^^^^^^^
The search option offers the possibility to check the results in a table.
The search is performed across all searchable columns. If matching data is found in a column,
the entire row is matched and displayed in the result set. See Figure 10: *Search result after searching for "B"*

.. figure:: img/object_table_search_result.png
    :width: 600

    Figure 10: Search result after searching for "B"

| 

Table filter
^^^^^^^^^^^^
While the search function offers the possibility to search the table,
the filter method provides the ability to search for data in a specific column.

The column searches are cumulative, so additional columns can be inserted to apply multiple individual column searches,
presenting the user with complex search options.

.. figure:: img/object_table_filter_result.png
    :width: 600

    Figure 11: Filter result after filtering for "B"

| 

The search terms within different rows are linked with each other with the condition *OR*
(Figure 12: *Filtering by OR-expression*). The search terms within a row are all linked with the condition *AND*
(Figure 13: *Filter by AND-expression*). Only the filtered objects are available for exporting the values from the current
table.

.. figure:: img/object_table_filter_example_1_result.png
    :width: 600

    Figure 12: Filtering by OR expression

| 

.. figure:: img/object_table_filter_example_2_result.png
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

TODO: ObjectGroups
==================

| 

=======================================================================================================================

| 

TODO: Persons
=============

| 

=======================================================================================================================

| 

TODO: PersonGroups
==================

| 
