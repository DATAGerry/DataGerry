/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2025 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
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
import { RiskAssessmentFooterComponent } from './risk-assessment-footer/risk-assessment-footer.component';
import { ISMSModule } from '../isms.module';
import { ControlMeasureAssignmentModule } from '../control‑measure‑assignment/control-measure-assignment.module';

@NgModule({
  declarations: [
    RiskAssessmentAddComponent,
    RiskAssessmentAfterComponent,
    RiskAssessmentAuditComponent,
    RiskAssessmentBeforeComponent,
    RiskAssessmentFormTopComponent,
    RiskAssessmentTreatmentComponent,
    RiskAssessmentListComponent,
    RiskAssessmentFooterComponent,  ],
  imports: [
    CommonModule,
    RiskAssessmentRoutingModule,
    TableModule,
    AuthModule,
    CoreModule,
    ReactiveFormsModule,
    CoreModule,
    ControlMeasureAssignmentModule
  ],
  exports: [
    RiskAssessmentListComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RiskAssessmentModule { }
