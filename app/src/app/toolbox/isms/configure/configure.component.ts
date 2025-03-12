import { Component, OnInit } from '@angular/core';
import { IsmsConfig } from '../models/isms-config.model';


@Component({
  selector: 'app-isms-configure',
  templateUrl: './configure.component.html',
  styleUrls: ['./configure.component.scss']
})
export class ConfigureComponent implements OnInit {
  public ismsConfig: IsmsConfig;

  constructor() {
    // Initialize the configuration object with empty arrays
    this.ismsConfig = {
      riskClasses: [],
      likelihoodEntries: [],
      impactEntries: [],
      impactCategories: [],
      protectionGoals: [],
      riskMatrix: null 
    };
  }

  ngOnInit(): void {
  }

  saveIsmsConfig(): void {

  }
}
