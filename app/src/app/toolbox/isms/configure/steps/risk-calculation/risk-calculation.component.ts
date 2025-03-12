import { Component, Input, OnInit } from '@angular/core';
import { IsmsConfig } from '../../../models/isms-config.model';

@Component({
  selector: 'app-isms-risk-calculation',
  templateUrl: './risk-calculation.component.html',
  styleUrls: ['./risk-calculation.component.scss']
})
export class RiskCalculationComponent implements OnInit {

    @Input() config: IsmsConfig;

  constructor() { }

  ngOnInit(): void {
    // Setup or calculate the risk matrix
  }
}
