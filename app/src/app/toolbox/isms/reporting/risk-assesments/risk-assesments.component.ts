import { Component, OnInit } from '@angular/core';
import { RiskTreatmentPlanService } from '../../services/risk-treatment-plan.service';
import { RiskAssesmentsReportService } from '../../services/risk-assessment-report.service';

@Component({
  selector: 'app-assesments',
  styleUrls: ['./risk-assesments.component.scss'],
  templateUrl: './risk-assesments.component.html',
})
export class RiskAssesmentsComponent implements OnInit {

  constructor(private riskAssesmentReportService: RiskAssesmentsReportService) { }

  ngOnInit(): void {
    this.riskAssesmentReportService.getRiskAssesmentsReportList().subscribe({
        next: (data) => {
            console.log(data);
        },
        error: (err) => {
            console.log(err);
        }
    });
  }

}
