import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
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
    LikelihoodModalComponent
  ],
  imports: [
    CommonModule,
    LayoutModule,
    IsmsRoutingModule,
    ArchwizardModule,
    ReactiveFormsModule,
    NgSelectModule,
    FontAwesomeModule,
    AuthModule,
    CoreModule,
    TableModule
  ]
})
export class ISMSModule {}
