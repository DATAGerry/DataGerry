import { Component, Input, OnInit } from '@angular/core';
import { IsmsConfig } from '../../../models/isms-config.model';

@Component({
  selector: 'app-isms-impact',
  templateUrl: './impact.component.html',
  styleUrls: ['./impact.component.scss']
})
export class ImpactComponent implements OnInit {

    @Input() config: IsmsConfig;

  constructor() { }

  ngOnInit(): void {
    // Setup form or data for impact entries
  }
}
