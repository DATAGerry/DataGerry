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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit } from '@angular/core';
import { forkJoin } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';


import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { Impact } from '../models/impact.model';
import { Likelihood } from '../models/likelihood.model';
import { RiskClass } from '../models/risk-class.model';
import { ReportRiskMatrix } from '../models/risk-matrix-report.model';
import { ImpactService } from '../services/impact.service';
import { LikelihoodService } from '../services/likelihood.service';
import { RiskClassService } from '../services/risk-class.service';
import { RiskMatrixReportService } from '../services/risk-matrix-report.service';
import { RiskAssessmentDrilldownModalComponent } from './modal/risk-assessment-drilldown-modal.component';



@Component({
  selector: 'app-risk-matrix-report',
  templateUrl: './risk-matrix-report.component.html',
  styleUrls: ['./risk-matrix-report.component.scss']
})
export class RiskMatrixReportComponent implements OnInit {

  impacts: Impact[] = [];
  likelihoods: Likelihood[] = [];
  riskClasses: RiskClass[] = [];

  before:  any[] = [];
  current: any[] = [];
  after:   any[] = [];

  loading = false;

  constructor(
    private readonly reportSrv: RiskMatrixReportService,
    private readonly impactSrv: ImpactService,
    private readonly lhSrv: LikelihoodService,
    private readonly rcSrv: RiskClassService,
    private readonly loader: LoaderService,
    private readonly toast: ToastService,
    private readonly modal: NgbModal
  ) { }

  ngOnInit(): void { this.loadAll(); }

  /** -------------------------------------------------- */

  private loadAll(): void {
    this.loading = true; this.loader.show();

    forkJoin({
      impacts: this.impactSrv.getImpacts({ filter:'', limit:10, page:1, sort:'calculation_basis', order:1 }),
      likelihoods: this.lhSrv.getLikelihoods({ filter:'', limit:0, page:1, sort:'calculation_basis', order:1 }),
      riskClasses: this.rcSrv.getRiskClasses({ filter:'', limit:0, page:1, sort:'sort', order:1 }),
      report: this.reportSrv.getReport1()
    }).pipe(finalize(() => { this.loading = false; this.loader.hide(); }))
      .subscribe({
        next: res => this.handleData(
            res.report, 
            res.impacts.results,             
            res.likelihoods.results, 
            res.riskClasses.results
        ),
        error: err => this.toast.error(err?.error?.message || 'Load failed')
      });
  }

  /** keep axes sorted ascending by calculation_basis */
  private handleData(mat: ReportRiskMatrix,
                     imp: Impact[], lh: Likelihood[], rc: RiskClass[]): void {

    this.impacts = [...imp].sort((a,b)=>a.calculation_basis-b.calculation_basis);
    this.likelihoods = [...lh].sort((a,b)=>b.calculation_basis-a.calculation_basis); // rows top→bottom high→low
    this.riskClasses = rc;

    this.before  = mat.risk_matrix_before_treatment;
    this.current = mat.risk_matrix_current_state;
    this.after   = mat.risk_matrix_after_treatment;
  }

  /** open drill-down list */
  onCell(ids: number[]): void {
    if (!ids?.length) { return; }
    const ref = this.modal.open(RiskAssessmentDrilldownModalComponent, { size:'xl' });
    ref.componentInstance.assessmentIds = ids;
  }
}
