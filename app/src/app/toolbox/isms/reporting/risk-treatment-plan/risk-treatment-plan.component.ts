import { Component, OnInit } from '@angular/core';
import { RiskTreatmentPlanService } from '../../services/risk-treatment-plan.service';

@Component({
  selector: 'app-risk-treatment-plan',
  templateUrl: './risk-treatment-plan.component.html',
})
export class RiskTreatmentPlanComponent implements OnInit {

  constructor(private riskTreatmentPlanService: RiskTreatmentPlanService) { }

  ngOnInit(): void {
    this.riskTreatmentPlanService.getRiskTreatmentPlanList().subscribe({
        next: (data) => {
            console.log(data);
        },
        error: (err) => {
            console.log(err);
        }
    });
  }

}
