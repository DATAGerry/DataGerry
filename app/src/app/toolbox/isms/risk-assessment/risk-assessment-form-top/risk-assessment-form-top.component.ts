import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-risk-assessment-form-top',
  templateUrl: './risk-assessment-form-top.component.html',
  styleUrls: ['./risk-assessment-form-top.component.scss']
})
export class RiskAssessmentFormTopComponent implements OnInit {
  @Input() parentForm!: FormGroup;
  @Input() fromRisk = false;
  @Input() fromObject = false;
  @Input() fromObjectGroup = false;
  @Input() risks: any[] = [];
  @Input() objects: any[] = [];
  @Input() objectGroups: any[] = [];

  public objectRefTypes = [
    { label: 'Object', value: 'OBJECT' },
    { label: 'Object Group', value: 'OBJECT_GROUP' }
  ];

  ngOnInit(): void {

    if (this.fromObject || this.fromObjectGroup) {
      this.parentForm.get('object_id_ref_type')?.disable();
    }
    console.log('fromRisk:', this.fromRisk)
    console.log('fromObject:', this.fromObject);
  }
}
