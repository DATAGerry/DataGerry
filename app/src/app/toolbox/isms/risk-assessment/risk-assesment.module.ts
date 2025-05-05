import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TableModule } from 'src/app/layout/table/table.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { CoreModule } from 'src/app/core/core.module';
import { ReactiveFormsModule } from '@angular/forms';
import { RiskAssessmentRoutingModule } from './risk-assesment-routing.module';
import { RiskAssessmentAddComponent } from './risk-assessment-add/risk-assessment-add.component';
import { RiskAssessmentAfterComponent } from './risk-assessment-after/risk-assessment-after.component';
import { RiskAssessmentAuditComponent } from './risk-assessment-audit/risk-assessment-audit.component';
import { RiskAssessmentBeforeComponent } from './risk-assessment-before/risk-assessment-before.component';
import { RiskAssessmentFormTopComponent } from './risk-assessment-form-top/risk-assessment-form-top.component';
import { RiskAssessmentTreatmentComponent } from './risk-assessment-treatment/risk-assessment-treatment.component';
import { RiskAssessmentListComponent } from './risk-assesment-list/risk-assessment-list.component';

@NgModule({
  declarations: [
    RiskAssessmentAddComponent,
    RiskAssessmentAfterComponent,
    RiskAssessmentAuditComponent,
    RiskAssessmentBeforeComponent,
    RiskAssessmentFormTopComponent,
    RiskAssessmentTreatmentComponent,
    RiskAssessmentListComponent
  ],
  imports: [
    CommonModule,
    RiskAssessmentRoutingModule,
    TableModule,
    AuthModule,
    CoreModule,
    ReactiveFormsModule,
    CoreModule
  ],
  exports: [
    RiskAssessmentListComponent
  ]
})
export class RiskAssessmentModule { }
