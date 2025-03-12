import { Component, Input, OnInit } from '@angular/core';
import { IsmsConfig } from '../../../models/isms-config.model';

@Component({
  selector: 'app-isms-likelihood',
  templateUrl: './likelihood.component.html',
  styleUrls: ['./likelihood.component.scss']
})
export class LikelihoodComponent implements OnInit {
    @Input() config: IsmsConfig;

  constructor() { }

  ngOnInit(): void {
    // Setup form or data for likelihood entries
  }
}
