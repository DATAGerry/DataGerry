import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-risk-assessment-audit',
  templateUrl: './risk-assessment-audit.component.html',
  styleUrls: ['./risk-assessment-audit.component.scss']
})
export class RiskAssessmentAuditComponent {
  @Input() parentForm!: FormGroup;
  @Input() allPersons: any[] = [];
  @Input() allPersonGroups: any[] = [];

  public personRefTypes = [
    { label: 'Person', value: 'PERSON' },
    { label: 'Person Group', value: 'PERSON_GROUP' }
  ];
}
