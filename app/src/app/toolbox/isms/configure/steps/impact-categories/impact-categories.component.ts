import { Component, Input, OnInit } from '@angular/core';
import { IsmsConfig } from '../../../models/isms-config.model';

@Component({
  selector: 'app-isms-impact-categories',
  templateUrl: './impact-categories.component.html',
  styleUrls: ['./impact-categories.component.scss']
})
export class ImpactCategoriesComponent implements OnInit {
    @Input() config: IsmsConfig;

  constructor() { }

  ngOnInit(): void {
    // Setup form or data for impact categories
  }
}
