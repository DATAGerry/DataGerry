import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ArchwizardModule } from '@rg-software/angular-archwizard';
import { CoreModule } from 'src/app/core/core.module';
import { LayoutModule } from 'src/app/layout/layout.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { IsmsRoutingModule } from './isms-routing.module';

import { IsmsComponent } from './isms.component';
import { OverviewComponent } from './overview/overview.component';
import { ConfigureComponent } from './configure/configure.component';

// Step components under configure/steps
import { RiskClassesComponent } from './configure/steps/risk-classes/risk-classes.component';
import { LikelihoodsComponent } from './configure/steps/likelihood/likelihood.component';
import { ImpactComponent } from './configure/steps/impact/impact.component';
import { ImpactCategoriesComponent } from './configure/steps/impact-categories/impact-categories.component';
import { ProtectionGoalsComponent } from './configure/steps/protection-goals/protection-goals.component';
import { RiskCalculationComponent } from './configure/steps/risk-calculation/risk-calculation.component';
import { TableModule } from 'src/app/layout/table/table.module';
import { RiskClassModalComponent } from './configure/steps/risk-classes/modal/add-risk-class-modal.component';
import { LikelihoodModalComponent } from './configure/steps/likelihood/modal/likelihood-modal.component';
import { ImpactModalComponent } from './configure/steps/impact/modal/impact-modal.component';
import { ImpactCategoryModalComponent } from './configure/steps/impact-categories/modal/impact-category-modal.component';
import { ProtectionGoalModalComponent } from './configure/steps/protection-goals/modal/protection-goal-modal.component';
import { ThreatsListComponent } from './threats/threats-list.component';
import { ThreatsAddComponent } from './threats/add/threats-add.component';
import { VulnerabilitiesListComponent } from './vulnerabilities/vulnerabilities-list.component';
import { VulnerabilitiesAddComponent } from './vulnerabilities/add/vulnerabilities-add.component';
import { RiskAddComponent } from './risks/risks-add/risks-add.component';
import { RisksListComponent } from './risks/risks-list/risks-list.component';
import { PersonListComponent } from './person/person-list/person-list.component';
import { PersonAddEditComponent } from './person/person-add/person-add-edit.component';
import { PersonRoutingModule } from './person/person-routing.module';
// import { RiskAssessmentModule } from './risk-assessment/risk-assesment.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ControlmeasuresListComponent } from './control-measure/control-measure-list/control-measure-list.component';
import { ControlMeasuresAddComponent } from './control-measure/control-measure-add/control-measures-add.component';

@NgModule({
  declarations: [
    IsmsComponent,
    OverviewComponent,
    ConfigureComponent,
    RiskClassesComponent,
    LikelihoodsComponent,
    ImpactComponent,
    ImpactCategoriesComponent,
    ProtectionGoalsComponent,
    RiskCalculationComponent,
    RiskClassModalComponent,
    LikelihoodModalComponent,
    ImpactModalComponent,
    ImpactCategoryModalComponent,
    ProtectionGoalModalComponent,
    ThreatsListComponent,
    ThreatsAddComponent,
    VulnerabilitiesListComponent,
    VulnerabilitiesAddComponent,
    RiskAddComponent,
    RisksListComponent,
    ControlmeasuresListComponent,
    ControlMeasuresAddComponent,
    PersonListComponent,
    PersonAddEditComponent
  ],
  imports: [
    CommonModule,
    LayoutModule,
    IsmsRoutingModule,
    PersonRoutingModule,
    // RiskAssessmentModule,
    ArchwizardModule,
    ReactiveFormsModule,
    NgSelectModule,
    FontAwesomeModule,
    AuthModule,
    CoreModule,
    TableModule,
    FormsModule,
    NgbModule
  ]
})
export class ISMSModule {}
