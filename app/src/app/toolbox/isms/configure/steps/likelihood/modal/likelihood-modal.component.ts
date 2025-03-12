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
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { finalize } from 'rxjs/operators';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { Likelihood } from 'src/app/toolbox/isms/models/likelihood.model';
import { LikelihoodService } from 'src/app/toolbox/isms/services/likelihood.service';

@Component({
  selector: 'app-likelihood-modal',
  templateUrl: './likelihood-modal.component.html',
  styleUrls: ['./likelihood-modal.component.scss']
})
export class LikelihoodModalComponent implements OnInit {
  @Input() likelihood?: Likelihood; // If provided, we're in "Edit" mode

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
   * Build the reactive form.
   * The calculation_basis field is validated with a pattern that requires a decimal value.
   */
  private buildForm(): void {
    this.form = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      // Pattern: one or more digits, a dot, and one or more digits.
      calculation_basis: [
        '',
        [Validators.required, Validators.pattern(/^\d+\.\d+$/)]
      ]
    });
  }

  /**
   * Patch the form with existing likelihood data if in edit mode.
   */
  private patchForm(): void {
    if (!this.likelihood) return;
    this.form.patchValue({
      name: this.likelihood.name,
      description: this.likelihood.description,
      calculation_basis: this.likelihood.calculation_basis.toString()
    });
  }

  /**
   * Handle form submission for Add or Edit.
   * The calculation_basis value is parsed as a float.
   */
  public onSubmit(): void {
    if (this.form.invalid) {
      // Mark all controls as touched so errors are displayed immediately.
      this.form.markAllAsTouched();
      return;
    }
    this.isSubmitting = true;

    const formValue = this.form.value;
    const formData: Likelihood = {
      ...formValue,
      calculation_basis: parseFloat(formValue.calculation_basis)
    };

    if (!this.isEditMode) {
      // Add mode
      this.likelihoodService.createLikelihood(formData)
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
      this.likelihoodService.updateLikelihood(publicId, formData)
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

  /**
   * Dismiss the modal.
   */
  public onCancel(): void {
    this.activeModal.dismiss('cancel');
  }
}
