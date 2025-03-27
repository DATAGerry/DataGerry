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
import { Component, OnInit, ViewChild, AfterViewChecked, ChangeDetectorRef, ElementRef, AfterViewInit } from '@angular/core';
import { WizardComponent } from '@rg-software/angular-archwizard';
import { IsmsConfig } from '../models/isms-config.model';
import { ISMSService } from '../services/isms.service';
import { IsmsConfigValidation } from '../models/isms-config-validation.model';

@Component({
  selector: 'app-isms-configure',
  templateUrl: './configure.component.html',
  styleUrls: ['./configure.component.scss']
})
export class ConfigureComponent implements OnInit, AfterViewInit {
  public ismsConfig: IsmsConfig;
  public totalSteps: number = 6; // Total number of steps in the wizard
  public riskClassesCount: number = 0;
  public likelihoodCount: number = 0;
  public impactCount: number = 0;
  public impactCategoriesCount: number = 0;
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
    private cdRef: ChangeDetectorRef,
    private elRef: ElementRef
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
  ngOnInit(): void {
    // Existing code...
    this.updateStepIndicatorColors();
  }

  ngAfterViewInit(): void {
    if (!this.wizard) {
      return;
    }
  }

  /**
 * Validates the current step based on the number of items.
 */
  isStepValid(): boolean {
    if (!this.wizard) {
      return false;
    }

    switch (this.wizard.currentStepIndex) {
      case 0: // Risk Classes
        return this.riskClassesCount >= 3;
      case 1: // Likelihood
        return this.likelihoodCount >= 3;
      case 2: // Impact
        return this.impactCount >= 3;
      case 3: // Impact Categories
        return this.impactCategoriesCount >= 1;
      case 4: // Protection Goals
        return true; // Always valid
      default:
        return true;
    }
  }

  /**
 * Updates the step-indicator color based on validation.
 */
  updateStepIndicatorColors(): void {
    const steps = this.elRef.nativeElement.querySelectorAll('.steps-indicator li');
    steps.forEach((step: HTMLElement, index: number) => {
      const isValid = this.validateStep(index);
      if (isValid) {
        step.classList.add('valid-step'); // Add green color class
        step.classList.remove('invalid-step'); // Remove red color class
      } else {
        step.classList.add('invalid-step'); // Add red color class
        step.classList.remove('valid-step'); // Remove green color class
      }
    });
  }



  /**
   * Validates a specific step.
   */
  private validateStep(stepIndex: number): boolean {
    switch (stepIndex) {
      case 0: // Risk Classes
        return this.riskClassesCount >= 3;
      case 1: // Likelihood
        return this.likelihoodCount >= 3;
      case 2: // Impact
        return this.impactCount >= 3;
      case 3: // Impact Categories
        return this.impactCategoriesCount >= 1;
      case 4: // Protection Goals
        return true; // Always valid
      default:
        return true;
    }
  }


  // nextStep(): void {
  //   const nextIndex = this.wizard.currentStepIndex + 1;
  //   if (nextIndex < this.totalSteps) {
  //     this.wizard.goToStep(nextIndex);
  //   }
  // }

  // previousStep(): void {
  //   const prevIndex = this.wizard.currentStepIndex - 1;
  //   if (prevIndex >= 0) {
  //     this.wizard.goToStep(prevIndex);
  //   }
  // }

  nextStep(): void {
    if (this.isStepValid()) {
      const nextIndex = this.wizard.currentStepIndex + 1;
      if (nextIndex < this.totalSteps) {
        this.wizard.goToStep(nextIndex);
      }
    }
    this.updateStepIndicatorColors();
  }

  previousStep(): void {
    const prevIndex = this.wizard.currentStepIndex - 1;
    if (prevIndex >= 0) {
      this.wizard.goToStep(prevIndex);
    }
    this.updateStepIndicatorColors();
  }

  public onConfigChange(updatedConfig: IsmsConfig): void {
    this.ismsConfig = updatedConfig;
    this.updateStepIndicatorColors();
  }

  public onRiskClassesCountChange(count: number): void {
    this.riskClassesCount = count;
  }

  public onLikelihoodCountChange(count: number): void {
    this.likelihoodCount = count;
  }

  public onImpactCountChange(count: number): void {
    this.impactCount = count;
  }

  public onImpactCategoriesCountChange(count: number): void {
    this.impactCategoriesCount = count;
  }
}