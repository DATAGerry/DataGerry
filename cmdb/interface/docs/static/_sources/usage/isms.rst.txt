****
ISMS
****

.. _isms-anchor:

.. contents:: Table of Contents
    :local:

=======================================================================================================================

An **Information Security Management System (ISMS)** is a structured framework of policies, processes, and controls
designed to manage and protect an organization's sensitive data and information assets. It ensures that
information security risks are identified, evaluated, and mitigated systematically across all areas of the
organization.

The goal of an ISMS is not only to prevent data breaches or unauthorized access, but also to maintain the
confidentiality, integrity, and availability of information — often referred to as the **CIA triad**.

An effective ISMS is aligned with international standards such as **ISO/IEC 27001** and provides the foundation
for establishing trust, meeting regulatory compliance requirements, and ensuring continual improvement of security
posture.

Key elements of an ISMS include:

* **Risk Management** - Identifying, evaluating, and addressing security risks
* **Policies and Procedures** - Documenting rules and processes for information security
* **Roles and Responsibilities** - Defining who is accountable for different areas of security
* **Asset Management** - Tracking and classifying information assets and their importance
* **Incident Management** - Preparing for and responding to security breaches and incidents
* **Continual Improvement** - Regularly assessing and enhancing the ISMS based on audits and feedback

| 

The ISMS implementation in **DataGerry** supports organizations in modeling these concepts and maintaining
a centralized system to manage security-related documentation, responsibilities, risks, and controls.

To access the ISMS functionalities of DataGerry go to **Toolbox -> ISMS**.

.. figure:: img/isms/isms_overview.png
    :width: 600

    Picture: ISMS overview

In the following sections, you will find detailed explanations of how ISMS-related features are integrated into
DataGerry.

| 

=======================================================================================================================

| 

ISMS - Configuration
====================

Before risks can be assessed and treated effectively, an Information Security Management System (ISMS) requires a solid
foundation of clearly defined classification schemes and evaluation parameters. In DataGerry, the ISMS Configuration
provides the necessary building blocks for a consistent and repeatable risk assessment process.

This configuration defines how risks are identified, scored, and categorized, and it forms the basis for generating a
standardized **Risk Matrix**. It enables organizations to align their risk evaluation with internal policies or
external frameworks.

The following elements are part of the ISMS Configuration:

* **Risk Classes** - Define how risk levels are grouped and labeled (e.g., Low, Medium, High)
* **Likelihoods** - Represent the probability of a risk event occurring
* **Impacts** - Describe the potential consequences or severity if a risk occurs
* **Impact Categories** - Break down impacts into specific domains (e.g., Financial, Legal, Operational)
* **Protection Goals** - Define which security objectives are affected (e.g., Confidentiality, Integrity, Availability)
* **Risk Matrix** - Combines likelihoods and impacts to determine overall risk levels based on the configured classes

These configuration elements are used throughout the ISMS functionality of DataGerry to evaluate risks, document their
relevance, and decide on appropriate treatment strategies.

In the next sections, each of these configuration areas will be described in detail, including their purpose and how
they are managed in the system.

To access the ISMS Configuration go to **Toolbox -> Configure ISMS Settings**

| 

=======================================================================================================================

| 

Risk classes
------------

.. _isms-risk-class-anchor:

| 

Risk Classes (or Risk Levels) define how calculated risks are categorized within the ISMS framework.
They represent the severity or urgency of a given risk and are essential for supporting risk-based
decision-making.

Each class groups a range of risk scores and gives them a human-readable meaning — for example: *Low*,
*Medium*, or *High*. These labels are later used throughout the ISMS process to guide mitigation
priorities, reporting, and compliance evaluations.

To access and manage Risk Classes, navigate to **Toolbox -> Configure ISMS Settings -> Risk Classes**.

.. figure:: img/isms/isms_risk_classes_overview.png
    :width: 600

    Picture: ISMS risk classes overview

| 

**Minimum and Maximum Limits**

- A minimum of **three (3)** risk classes is required to enable the ISMS risk evaluation process
- A maximum of **six (6)** risk classes can be defined to keep evaluations consistent and manageable

| 

**Risk class fields**

Each Risk Class includes the following fields:

.. list-table:: Table: Fields for Risk Classes
   :width: 80%
   :widths: 30 70
   :align: center

   * - **name**
     - The name or title of the Risk Class (e.g., *Low*, *Moderate*, *Critical*)
   * - **Color**
     - A visual color indicator used in risk matrices and tables for intuitive representation
   * - **Description**
     - The description of the risk class


.. figure:: img/isms/isms_risk_classes_create.png
    :width: 600

    Picture: ISMS risk classes create form

| 

=======================================================================================================================

| 

Likelihoods
-----------

.. _isms-likelihood-anchor:

| 

Likelihoods represent the probability that a specific risk scenario will occur. Within the ISMS framework, likelihood
is one of the two primary dimensions (alongside impact) used to calculate overall risk severity. Proper definition
of likelihood levels ensures consistent and repeatable risk assessments across the organization.

To manage **Likelihoods**, navigate to **Toolbox -> Configure ISMS Settings -> Likelihoods**.

.. figure:: img/isms/isms_likelihood_overview.png
    :width: 600

    Picture: ISMS likelihoods overview

| 

**Minimum and Maximum Limits**

- A minimum of **three (3)** likelihood levels is required for the risk matrix to function correctly
- A maximum of **six (6)** likelihood levels can be defined

| 

**Likelihood fields**

Each **Likelihood** includes the following fields:

.. list-table:: Table: Fields for Likelihoods
   :width: 80%
   :widths: 30 70
   :align: center

   * - **Name**
     - The name of the Likelihood level (e.g., *Unlikely*, *Possible*, *Very Likely*)
   * - **Description**
     - The description of the **Likelihood**
   * - **Calculation Basis**
     - A numeric value representing the likelihood's weight; used in risk score calculations

.. figure:: img/isms/isms_likelihood_create.png
    :width: 600

    Picture: ISMS likelihood create form

| 

.. note::
   **Likelihoods** are used in combination with :ref:`Impacts <isms-impact-anchor>` to determine a total risk score,
   which is then categorized using the defined :ref:`Risk Classes <isms-risk-class-anchor>`

| 

=======================================================================================================================

| 

Impacts
-------

.. _isms-impact-anchor:

| 

Impacts represent the severity of consequences that would result if a given risk scenario occurs. Together with
:ref:`Likelihoods <isms-likelihood-anchor>`, impacts form the basis of risk evaluation and define how critical a risk
is to your organization. Well-defined impact levels help ensure a consistent and objective assessment process.

To manage **Impacts**, navigate to **Toolbox -> Configure ISMS Settings -> Impacts**.

.. figure:: img/isms/isms_impact_overview.png
    :width: 600

    Picture: ISMS impacts overview

| 

**Minimum and Maximum Limits**

- A minimum of **three (3)** impact levels is required for the risk matrix to function correctly
- A maximum of **six (6)** impact levels can be defined

| 

**Impact fields**

Each **Impact** includes the following fields:

.. list-table:: Table: Fields for Impacts
   :width: 80%
   :widths: 30 70
   :align: center

   * - **Name**
     - The name of the Impact level (e.g., *Low*, *Moderate*, *Critical*)
   * - **Description**
     - A brief explanation of the potential consequence or damage for this impact level
   * - **Calculation Basis**
     - A numeric value representing the severity of the impact; used in risk score calculations

.. figure:: img/isms/isms_impact_create.png
    :width: 600

    Picture: ISMS impact create form

| 

.. note::
   **Impacts** are used in combination with :ref:`Likelihoods <isms-likelihood-anchor>` to determine the overall risk
   score, which is then classified using defined :ref:`Risk Classes <isms-risk-class-anchor>`

| 

=======================================================================================================================

| 

Impact Categories
-----------------

| 

**Impact Categories** allow organizations to group different dimensions of potential impact for use in risk assessments.
They provide context to the selected **Impact levels** by defining what a certain severity means in specific areas —
such as financial damage, regulatory consequences, or business continuity.

To manage **Impact Categories**, navigate to **Toolbox -> Configure ISMS Settings -> Impact Categories**.

.. figure:: img/isms/isms_impact_categories_overview.png
    :width: 600

    Picture: ISMS impact categories overview

| 

**Impact Category fields**

Each **Impact Category** consists of the following fields:

.. list-table:: Table: Fields for Impact Categories
   :width: 90%
   :widths: 30 70
   :align: center

   * - **Impact Category Name**
     - The name of the category (e.g., *Financial*, *Legal*, *Operational*)
   * - **Impact Descriptions**
     - A list of descriptions for each defined :ref:`Impact <isms-impact-anchor>`, describing what each level
       means within this category's context

.. figure:: img/isms/isms_impact_categories_create.png
    :width: 600

    Picture: ISMS impact categories create form

| 

.. note::
   Each **Impact Category** can provide a textual description for every existing **Impact**, allowing
   risk assessors to understand the consequences within that category's scope.

| 

=======================================================================================================================

| 

Protection Goals
----------------

|

**Protection Goals** define the core security objectives your organization aims to uphold when managing risks.
These goals serve as key pillars in risk analysis and help determine the impact of specific threats on critical
information assets.

In DataGerry's ISMS module, three **Protection Goals** are predefined:

- **Confidentiality** - Ensuring that sensitive information is accessible only to authorized parties.
- **Integrity** - Ensuring the accuracy and reliability of information and systems.
- **Availability** - Ensuring that systems and data are accessible when needed.

You may also define additional custom Protection Goals to reflect your organization's specific requirements
(e.g., *Authenticity*, *Traceability*, *Resilience*).

To manage **Protection Goals**, navigate to: **Toolbox -> Configure ISMS Settings -> Protection Goals**

.. figure:: img/isms/isms_protection_goal_overview.png
    :width: 600

    Picture: ISMS protection goal overview

| 

.. note::
    Each **Protection Goal** consists of a single field (name)

| 

=======================================================================================================================

| 

Risk Matrix
-----------

| 

The **Risk Matrix** is the core mechanism used in the ISMS module to determine the severity of risks by evaluating
the :ref:`Likelihood <isms-likelihood-anchor>` of an event occurring against its potential
:ref:`Impact <isms-impact-anchor>`. The result is a :ref:`Risk Class <isms-risk-class-anchor>` that reflects
the criticality of the risk and guides appropriate mitigation measures.

|

To configure the Risk Matrix, navigate to: **Toolbox -> Configure ISMS Settings -> Risk Calculation**

.. figure:: img/isms/isms_risk_matrix_overview.png
    :width: 600

    Picture: ISMS risk matrix overview

|

**Matrix Configuration**

A 2-dimensional matrix is displayed with:

- :ref:`Likelihoods <isms-likelihood-anchor>` on the Y-axis
- :ref:`Impacts <isms-impact-anchor>` on the X-axis

Each cell in the matrix represents a possible combination of Likelihood and Impact. The user simply selects a **Risk Class**
for each combination — the structure of the matrix and the scoring logic are calculated automatically by the system.

This visual structure enables quick assessment and classification of risks based on their severity, using predefined logic.

| 

.. note::
   The number of rows and columns in the matrix is determined by the number of Likelihoods and Impacts defined
   in your ISMS configuration. Make sure you have at least 3 entries for each.

   The **Risk Matrix** is dynamically generated based on the configured Likelihoods and Impacts.
   The user is only responsible for assigning appropriate **Risk Classes** to each cell.

| 

**Risk Level Unit**

An optional setting allows you to define a **Risk Level Unit**, which is displayed in the matrix cells:

- **None** - No unit displayed
- **€** - Euro symbol
- **$** - Dollar symbol

This setting is purely visual and does not affect the actual calculation or classification logic.

| 

=======================================================================================================================

| 

=======================================================================================================================

| 

