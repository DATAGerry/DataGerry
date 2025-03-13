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

import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { finalize } from 'rxjs/operators';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { Likelihood } from 'src/app/toolbox/isms/models/likelihood.model';
import { LikelihoodService } from 'src/app/toolbox/isms/services/likelihood.service';
import { uniqueCalculationBasisValidator } from 'src/app/toolbox/isms/utils/isms-utils';

@Component({
  selector: 'app-likelihood-modal',
  templateUrl: './likelihood-modal.component.html',
  styleUrls: ['./likelihood-modal.component.scss']
})
export class LikelihoodModalComponent implements OnInit {
  @Input() likelihood?: Likelihood; // Provided => Edit mode
  @Input() existingCalculationBases: number[] = []; // For duplicate checking

  public form: FormGroup;
  public isSubmitting = false;
  public isEditMode = false;

  constructor(
    public activeModal: NgbActiveModal,
    private fb: FormBuilder,
    private likelihoodService: LikelihoodService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.isEditMode = !!this.likelihood;
    this.buildForm();
    if (this.isEditMode) {
      this.patchForm();
    }
  }

  /**
   * Build the form.
   * - Name: required
   * - Description: required
   * - Calculation Basis: required
   */
  private buildForm(): void {
    const currentBasis = this.isEditMode && this.likelihood ? this.likelihood.calculation_basis : undefined;
    this.form = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      calculation_basis: [
        '',
        [
          Validators.required,
          Validators.pattern(/^\d+\.\d{1}$/),
          uniqueCalculationBasisValidator(this.existingCalculationBases, currentBasis)
        ]
      ]
    });
  }
  

  /**
   * Patch the form with existing data in edit mode.
   * Uses toFixed(1) to ensure the trailing zero is preserved.
   */
  private patchForm(): void {
    if (!this.likelihood) return;
    const basisString = this.likelihood.calculation_basis.toFixed(1);
    this.form.patchValue({
      name: this.likelihood.name,
      description: this.likelihood.description,
      calculation_basis: basisString
    });
  }

  /**
   * Handle form submission for Add or Edit.
   */
  public onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.isSubmitting = true;
    const formValue = this.form.value;
    const payload: Partial<Likelihood> = {
      name: formValue.name,
      description: formValue.description,
      calculation_basis: formValue.calculation_basis,
      sort: 0
    };

    if (!this.isEditMode) {
      // Add mode
      this.likelihoodService.createLikelihood(payload)
        .pipe(finalize(() => (this.isSubmitting = false)))
        .subscribe({
          next: () => {
            this.toast.success('Likelihood created successfully!');
            this.activeModal.close('saved');
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    } else {
      // Edit mode
      const publicId = this.likelihood?.public_id;
      if (!publicId) {
        this.toast.error('No valid ID found for editing.');
        this.isSubmitting = false;
        return;
      }
      this.likelihoodService.updateLikelihood(publicId, payload)
        .pipe(finalize(() => (this.isSubmitting = false)))
        .subscribe({
          next: () => {
            this.toast.success('Likelihood updated successfully!');
            this.activeModal.close('saved');
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    }
  }

  public onCancel(): void {
    this.activeModal.dismiss('cancel');
  }
}
