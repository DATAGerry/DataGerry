import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

// Service & model for ControlMeasure
import { ControlMeasure } from '../../models/control-measure.model';

// Extendable Option
import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';
import { ControlMeasureService } from '../../services/control-measure.service';

export const CONTROL_MEASURE = 'CONTROL_MEASURE';
export const IMPLEMENTATION_STATE = 'IMPLEMENTATION_STATE';

@Component({
  selector: 'app-control-measures-add',
  templateUrl: './control-measures-add.component.html',
  styleUrls: ['./control-measures-add.component.scss']
})
export class ControlMeasuresAddComponent implements OnInit {

  public isEditMode = false;
  public isLoading$ = this.loaderService.isLoading$;

  public controlMeasureForm: FormGroup;
  public controlMeasure: ControlMeasure = {
    title: '',
    control_measure_type: 'CONTROL',  // or 'REQUIREMENT' | 'MEASURE'
    source: null,                      // store the public_id from the extendable option
    implementation_state: null,        // store the public_id from the extendable option
    identifier: '',
    chapter: '',
    description: '',
    is_applicable: false,
    reason: ''
  };

  // Dropdown data
  public sourceOptions: ExtendableOption[] = [];
  public implementationStateOptions: ExtendableOption[] = [];

  // Manage modals
  public showSourceManager = false;
  public showImplementationStateManager = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private loaderService: LoaderService,
    private toast: ToastService,
    private controlMeasureService: ControlMeasureService,
    private extendableOptionService: ExtendableOptionService
  ) {
    // Check if editing existing control/measure via router state
    const navState = this.router.getCurrentNavigation()?.extras?.state;
    if (navState && navState['controlMeasure']) {
      this.isEditMode = true;
      this.controlMeasure = navState['controlMeasure'] as ControlMeasure;
    }
  }

  ngOnInit(): void {
    this.initForm();

    if (this.isEditMode && this.controlMeasure.public_id) {
      console.log('editing control measure:', this.controlMeasure);
      this.patchForm(this.controlMeasure);
    }

    // Load dropdown data from ExtendableOptions
    this.loadSourceOptions();
    this.loadImplementationStateOptions();
  }

  /**
   * Initializes the form with default values and validators.
   */
  private initForm(): void {
    this.controlMeasureForm = this.fb.group({
      title: ['', Validators.required],
      control_measure_type: ['CONTROL', Validators.required],
      source: [null, Validators.required],
      implementation_state: [null, Validators.required],
      identifier: [''],
      chapter: [''],
      description: [''],
      is_applicable: [false],
      reason: ['']
    });
  }


  /**
   * Patches the form with existing control/measure data.
   * @param cm - The ControlMeasure object to patch the form with.
   */
  private patchForm(cm: ControlMeasure): void {
    this.controlMeasureForm.patchValue({
      title: cm.title,
      control_measure_type: cm.control_measure_type,
      source: cm.source,
      implementation_state: cm.implementation_state,
      identifier: cm.identifier,
      chapter: cm.chapter,
      description: cm.description,
      is_applicable: cm.is_applicable,
      reason: cm.reason
    });
  }

  /* ------------------------------------------------------------------
   * Load Extendable Options for Source & Implementation State
   * ------------------------------------------------------------------ */

  /**
   * Loads the source options from the ExtendableOptionService.
   */
  private loadSourceOptions(): void {
    this.loaderService.show();
    this.extendableOptionService.getExtendableOptionsByType(CONTROL_MEASURE)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (res) => {
          this.sourceOptions = res.results || [];
        },
        error: (err) => this.toast.error(err?.error?.message)
      });
  }


  /**
   * Loads the implementation state options from the ExtendableOptionService.
   */
  private loadImplementationStateOptions(): void {
    this.loaderService.show();
    this.extendableOptionService.getExtendableOptionsByType(IMPLEMENTATION_STATE)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (res) => {
          this.implementationStateOptions = res.results || [];
        },
        error: (err) => this.toast.error(err?.error?.message)
      });
  }

  /* ------------------------------------------------------------------
   * CREATE or UPDATE
   * ------------------------------------------------------------------ */

  /**
   * Handles the form submission for creating or updating a control/measure.
   */
  public onSave(): void {
    if (this.controlMeasureForm.invalid) {
      this.controlMeasureForm.markAllAsTouched();
      return;
    }

    const formValue = this.controlMeasureForm.value as ControlMeasure;

    if (this.isEditMode && this.controlMeasure.public_id) {
      this.updateControlMeasure(this.controlMeasure.public_id, formValue);
    } else {
      this.createControlMeasure(formValue);
    }
  }


  /**
   * Creates a new control/measure.
   * @param cm - The ControlMeasure object to create.
   */
  private createControlMeasure(cm: ControlMeasure): void {
    this.loaderService.show();
    this.controlMeasureService.createControlMeasure(cm)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Control/Measure created successfully');
          this.router.navigate(['/isms/control-measures']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }


  /**
   * Updates an existing control/measure.
   * @param id - The public_id of the control/measure to update.
   * @param cm - The ControlMeasure object with updated data.
   * @returns void
   * @throws Error if the update fails.
   */
  private updateControlMeasure(id: number, cm: ControlMeasure): void {
    this.loaderService.show();
    this.controlMeasureService.updateControlMeasure(id, { ...cm, public_id: id })
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Control/Measure updated successfully');
          this.router.navigate(['/isms/control-measures']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }


  /**
   * Handles the cancel action, navigating back to the control/measure list.
   * @returns void
   */
  public onCancel(): void {
    this.router.navigate(['/isms/control-measures']);
  }

  /* ------------------------------------------------------------------
   * Manage Extendable Option Modals
   * ------------------------------------------------------------------ */
  public openSourceManager(): void {
    this.showSourceManager = true;
  }
  public closeSourceManager(): void {
    this.showSourceManager = false;
    this.loadSourceOptions();
  }

  public openImplementationStateManager(): void {
    this.showImplementationStateManager = true;
  }
  public closeImplementationStateManager(): void {
    this.showImplementationStateManager = false;
    this.loadImplementationStateOptions();
  }

  /* ------------------------------------------------------------------
   * Error Checking
   * ------------------------------------------------------------------ */
  /**
   * Checks if a form control has a specific error.
   * @param controlName - The name of the form control.
   * @param error - The error type to check for.
   */
  public hasError(controlName: string, error: string): boolean {
    const ctrl = this.controlMeasureForm.get(controlName);
    return !!(ctrl && ctrl.hasError(error) && (ctrl.dirty || ctrl.touched));
  }
}
