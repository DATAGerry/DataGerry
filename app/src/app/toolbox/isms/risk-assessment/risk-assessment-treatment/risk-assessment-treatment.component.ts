import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-risk-assessment-treatment',
  templateUrl: './risk-assessment-treatment.component.html',
  styleUrls: ['./risk-assessment-treatment.component.scss']
})
export class RiskAssessmentTreatmentComponent {
  @Input() parentForm!: FormGroup;
  @Input() allPersons: any[] = [];
  @Input() allPersonGroups: any[] = [];
  @Input() implementationStates: any[] = [];

  public riskTreatmentOptions = [
    { label: 'Avoid', value: 'AVOID' },
    { label: 'Accept', value: 'ACCEPT' },
    { label: 'Reduce', value: 'REDUCE' },
    { label: 'Transfer/Share', value: 'TRANSFER_SHARE' },
  ];

  public personRefTypes = [
    { label: 'Person', value: 'PERSON' },
    { label: 'Person Group', value: 'PERSON_GROUP' },
  ];

  public priorityOptions = [
    { label: 'Low', value: 1 },
    { label: 'Medium', value: 2 },
    { label: 'High', value: 3 },
    { label: 'Very High', value: 4 }
  ];
}
