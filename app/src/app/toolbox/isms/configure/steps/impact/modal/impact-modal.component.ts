import { Component, Input, OnInit } from '@angular/core';
import {
    FormBuilder,
    FormGroup,
    Validators,
} from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { finalize } from 'rxjs/operators';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { Impact } from 'src/app/toolbox/isms/models/impact.model';
import { ImpactService } from 'src/app/toolbox/isms/services/impact.service';
import { uniqueCalculationBasisValidator } from 'src/app/toolbox/isms/utils/isms-utils';


@Component({
    selector: 'app-impact-modal',
    templateUrl: './impact-modal.component.html',
    styleUrls: ['./impact-modal.component.scss']
})
export class ImpactModalComponent implements OnInit {
    @Input() impact?: Impact;                  // If provided => Edit mode
    @Input() existingCalculationBases: number[] = []; // For checking duplicates

    public form: FormGroup;
    public isSubmitting = false;
    public isEditMode = false;

    constructor(
        public activeModal: NgbActiveModal,
        private fb: FormBuilder,
        private impactService: ImpactService,
        private toast: ToastService
    ) { }

    ngOnInit(): void {
        this.isEditMode = !!this.impact;
        this.buildForm();
        if (this.isEditMode) {
            this.patchForm();
        }
    }

    /**
     * Build the form:
     * - name: required
     * - description: required
     * - calculation_basis: required, must match pattern (^\d+\.\d{1}$), and be unique
     */
    private buildForm(): void {
        // If in edit mode, store the current numeric float value to allow it
        // if the user doesn't change the field
        const currentBasis = this.isEditMode && this.impact
            ? this.impact.calculation_basis
            : undefined;

        this.form = this.fb.group({
            name: ['', Validators.required],
            description: ['', Validators.required],
            calculation_basis: [
                '',
                [
                    Validators.required,
                    Validators.pattern(/^\d+\.\d{2}$/),
                    uniqueCalculationBasisValidator(this.existingCalculationBases, currentBasis)
                ]
            ]
        });
    }

    /**
     * If editing, patch the form with existing data.
     */
    private patchForm(): void {
        if (!this.impact) return;
        // Convert the numeric float to a string with exactly one decimal place
        const basisString = this.impact.calculation_basis;

        this.form.patchValue({
            name: this.impact.name,
            description: this.impact.description,
            calculation_basis: basisString
        });
    }

    /**
     * Submit the form for Add or Edit.
     */
    public onSubmit(): void {
        if (this.form.invalid) {
            this.form.markAllAsTouched(); // Force immediate error display
            return;
        }
        this.isSubmitting = true;

        // Keep the user input as a string
        const formValue = this.form.value;

        const payload: Partial<Impact> = {
            name: formValue.name,
            description: formValue.description,
            calculation_basis: parseFloat(formValue.calculation_basis),
            sort: 0
        };

        if (!this.isEditMode) {
            // ADD
            this.impactService
                .createImpact(payload)
                .pipe(finalize(() => (this.isSubmitting = false)))
                .subscribe({
                    next: () => {
                        this.toast.success('Impact created successfully!');
                        this.activeModal.close('saved');
                    },
                    error: (err) => {
                        this.toast.error(err?.error?.message);
                    }
                });
        } else {
            // EDIT
            const publicId = this.impact?.public_id;
            if (!publicId) {
                this.toast.error('No valid ID found for editing.');
                this.isSubmitting = false;
                return;
            }
            this.impactService
                .updateImpact(publicId, payload)
                .pipe(finalize(() => (this.isSubmitting = false)))
                .subscribe({
                    next: () => {
                        this.toast.success('Impact updated successfully!');
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
