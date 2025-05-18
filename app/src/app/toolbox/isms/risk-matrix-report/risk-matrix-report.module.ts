import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModalModule } from '@ng-bootstrap/ng-bootstrap';

import { RiskMatrixReportComponent } from './risk-matrix-report.component';

@NgModule({
  declarations: [
    RiskMatrixReportComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModalModule
  ]
})
export class RiskMatrixReportModule { }