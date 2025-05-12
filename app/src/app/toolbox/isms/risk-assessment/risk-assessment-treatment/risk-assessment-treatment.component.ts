import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-risk-assessment-treatment',
  templateUrl: './risk-assessment-treatment.component.html',
  styleUrls: ['./risk-assessment-treatment.component.scss']
})
export class RiskAssessmentTreatmentComponent  {
  @Input() parentForm!: FormGroup;
  @Input() allPersons: any[] = [];
  @Input() allPersonGroups: any[] = [];
  @Input() implementationStates: any[] = [];

  responsiblePersonOptions: any[] = [];

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

  
  ngOnChanges(ch: SimpleChanges): void {
    if (ch['allPersons'] || ch['allPersonGroups']) {
      this.responsiblePersonOptions = [
        ...this.allPersonGroups.map(pg => ({
          public_id   : pg.public_id,
          display_name: pg.name,
          group       : 'Person groups',
          type        : 'PERSON_GROUP'
        })),
        ...this.allPersons.map(p => ({
          public_id   : p.public_id,
          display_name: p.display_name,
          group       : 'Persons',
          type        : 'PERSON'
        }))
      ];
    }
  }

  
  onOwnerSelected(item: any): void {
    if (!item) return;
  
    this.parentForm.patchValue({
      responsible_persons_id_ref_type : item.type   // PERSON / PERSON_GROUP
    }, { emitEvent: false });
    
  }


  onPrioritySelected(selected: any): void {
    this.parentForm.patchValue({ priority: selected.value }, { emitEvent: false });
  }

}
