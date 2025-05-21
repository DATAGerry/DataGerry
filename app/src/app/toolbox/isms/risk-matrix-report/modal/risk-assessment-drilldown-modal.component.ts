import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-risk-assessment-drilldown-modal',
  templateUrl: './risk-assessment-drilldown-modal.component.html',
  styleUrls: ['./risk-assessment-drilldown-modal.component.scss']

})
export class RiskAssessmentDrilldownModalComponent {
  @Input() assessmentIds: number[] = [];
  constructor(public activeModal: NgbActiveModal) {}
}
