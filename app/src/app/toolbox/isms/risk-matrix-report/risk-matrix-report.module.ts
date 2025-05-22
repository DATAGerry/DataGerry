import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModalModule } from '@ng-bootstrap/ng-bootstrap';

import { RiskMatrixReportComponent } from './risk-matrix-report.component';
import { RiskMatrixGridComponent } from './risk-matrix-grid/risk-matrix-grid.component';
import { RiskAssessmentDrilldownModalComponent } from './modal/risk-assessment-drilldown-modal.component';
import { RiskAssessmentModule } from '../risk-assessment/risk-assesment.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { CoreModule } from 'src/app/core/core.module';

@NgModule({
  declarations: [
    RiskMatrixReportComponent,
    RiskMatrixGridComponent,
    RiskAssessmentDrilldownModalComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModalModule,
    RiskAssessmentModule,
    AuthModule,
    CoreModule
  ]
})
export class RiskMatrixReportModule { }