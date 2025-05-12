import { Component, Input, SimpleChanges } from '@angular/core';
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

  auditorOptions: any[] = [];

  public personRefTypes = [
    { label: 'Person', value: 'PERSON' },
    { label: 'Person Group', value: 'PERSON_GROUP' }
  ];

    ngOnChanges(ch: SimpleChanges): void {
      if (ch['allPersons'] || ch['allPersonGroups']) {
        this.auditorOptions = [
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
  
    
    onAuditorSelected(item: any): void {
      console.log('Selected Auditor:', item);
      if (!item) return;
    
      this.parentForm.patchValue({
        auditor_id_ref_type : item.type   // PERSON / PERSON_GROUP
      }, { emitEvent: false });
      
    }
}
