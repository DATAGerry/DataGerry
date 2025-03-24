/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2025 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit, ViewChild, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { WizardComponent } from '@rg-software/angular-archwizard';
import { IsmsConfig } from '../models/isms-config.model';
import { ISMSService } from '../services/isms.service';
import { IsmsConfigValidation } from '../models/isms-config-validation.model';

@Component({
  selector: 'app-isms-configure',
  templateUrl: './configure.component.html',
  styleUrls: ['./configure.component.scss']
})
export class ConfigureComponent  {
  public ismsConfig: IsmsConfig;
  public totalSteps: number = 6; // Total number of steps in the wizard
  public validationStatus: IsmsConfigValidation = {
    impact_categories: true,
    impacts: true,
    likelihoods: true,
    risk_classes: true,
    risk_matrix: true
};  

  @ViewChild('wizard') wizard!: WizardComponent; // Reference to the wizard component

  constructor(
    private ismsService: ISMSService,
    private cdRef: ChangeDetectorRef
  ) {
    this.ismsConfig = {
      riskClasses: [],
      likelihoodEntries: [],
      impactEntries: [],
      impactCategories: [],
      protectionGoals: [],
      riskMatrix: null
    };
  }



  nextStep(): void {
    const nextIndex = this.wizard.currentStepIndex + 1;
    if (nextIndex < this.totalSteps) {
      this.wizard.goToStep(nextIndex);
    }
  }

  previousStep(): void {
    const prevIndex = this.wizard.currentStepIndex - 1;
    if (prevIndex >= 0) {
      this.wizard.goToStep(prevIndex);
    }
  }
}