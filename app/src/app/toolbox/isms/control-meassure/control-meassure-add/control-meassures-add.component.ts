import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

// Service & model for ControlMeassure
import { ControlMeassure } from '../../models/control-meassure.model';
import { ControlMeassureService } from '../../services/control-meassure.service';

// Extendable Option
import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';

export const CONTROL_MEASSURE = 'CONTROL_MEASSURE';
export const IMPLEMENTATION_STATE = 'IMPLEMENTATION_STATE';

@Component({
  selector: 'app-control-meassures-add',
  templateUrl: './control-meassures-add.component.html',
  styleUrls: ['./control-meassures-add.component.scss']
})
export class ControlMeassuresAddComponent implements OnInit {

  public isEditMode = false;
  public isLoading$ = this.loaderService.isLoading$;

  public controlMeassureForm: FormGroup;
  public controlMeassure: ControlMeassure = {
    title: '',
    control_meassure_type: 'CONTROL',  // or 'REQUIREMENT' | 'MEASURE'
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
    private controlMeassureService: ControlMeassureService,
    private extendableOptionService: ExtendableOptionService
  ) {
    // Check if editing existing control/measure via router state
    const navState = this.router.getCurrentNavigation()?.extras?.state;
    if (navState && navState['controlMeassure']) {
      this.isEditMode = true;
      this.controlMeassure = navState['controlMeassure'] as ControlMeassure;
    }
  }

  ngOnInit(): void {
    this.initForm();

    if (this.isEditMode && this.controlMeassure.public_id) {
      this.patchForm(this.controlMeassure);
    }

    // Load dropdown data from ExtendableOptions
    this.loadSourceOptions();
    this.loadImplementationStateOptions();
  }

  /**
   * Initializes the form with default values and validators.
   */
  private initForm(): void {
    this.controlMeassureForm = this.fb.group({
      title: ['', Validators.required],
      control_meassure_type: ['CONTROL', Validators.required],
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
   * @param cm - The ControlMeassure object to patch the form with.
   */
  private patchForm(cm: ControlMeassure): void {
    this.controlMeassureForm.patchValue({
      title: cm.title,
      control_meassure_type: cm.control_meassure_type,
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
    this.extendableOptionService.getExtendableOptionsByType(CONTROL_MEASSURE)
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
    if (this.controlMeassureForm.invalid) {
      this.controlMeassureForm.markAllAsTouched();
      return;
    }

    const formValue = this.controlMeassureForm.value as ControlMeassure;

    if (this.isEditMode && this.controlMeassure.public_id) {
      this.updateControlMeassure(this.controlMeassure.public_id, formValue);
    } else {
      this.createControlMeassure(formValue);
    }
  }


  /**
   * Creates a new control/measure.
   * @param cm - The ControlMeassure object to create.
   */
  private createControlMeassure(cm: ControlMeassure): void {
    this.loaderService.show();
    this.controlMeassureService.createControlMeassure(cm)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Control/Measure created successfully');
          this.router.navigate(['/isms/control-meassures']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }


  /**
   * Updates an existing control/measure.
   * @param id - The public_id of the control/measure to update.
   * @param cm - The ControlMeassure object with updated data.
   * @returns void
   * @throws Error if the update fails.
   */
  private updateControlMeassure(id: number, cm: ControlMeassure): void {
    this.loaderService.show();
    this.controlMeassureService.updateControlMeassure(id, { ...cm, public_id: id })
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Control/Measure updated successfully');
          this.router.navigate(['/isms/control-meassures']);
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
    this.router.navigate(['/isms/control-meassures']);
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
    const ctrl = this.controlMeassureForm.get(controlName);
    return !!(ctrl && ctrl.hasError(error) && (ctrl.dirty || ctrl.touched));
  }
}
