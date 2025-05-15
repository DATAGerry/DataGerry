import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { OptionType } from 'src/app/toolbox/isms/models/option-type.enum';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';

import { Vulnerability } from '../../models/vulnerability.model';
import { VulnerabilityService } from '../../services/vulnerability.service';

@Component({
  selector: 'app-vulnerabilities-add',
  templateUrl: './vulnerabilities-add.component.html',
  styleUrls: ['./vulnerabilities-add.component.scss']
})
export class VulnerabilitiesAddComponent implements OnInit {
  public isEditMode = false;
  public isLoading$ = this.loaderService.isLoading$;

  public sourceOptions: ExtendableOption[] = [];
  public showSourceManager = false;

  public vulnerabilityForm: FormGroup;
  public vulnerability: Vulnerability = {
    name: '',
    source: [],
    identifier: '',
    description: ''
  };

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private vulnerabilityService: VulnerabilityService,
    private loaderService: LoaderService,
    private toast: ToastService,
    private extendableOptionService: ExtendableOptionService
  ) {
    // Retrieve the navigation state in the constructor
    const navState = this.router.getCurrentNavigation()?.extras?.state;
    if (navState && navState['vulnerability']) {
      this.isEditMode = true;
      this.vulnerability = navState['vulnerability'] as Vulnerability;
    }

    console.log('Vulnerability:', this.vulnerability);
  }

  ngOnInit(): void {

    this.initForm();

    // If we already have vulnerability data, patch the form
    if (this.isEditMode && this.vulnerability.public_id) {
      this.patchVulnerabilityForm(this.vulnerability);
    }

    // Load the extendable options for "source"
    this.loadSourceOptions();
  }

  /** Initialize the Reactive Form */
  private initForm(): void {
    this.vulnerabilityForm = this.fb.group({
      name: ['', Validators.required],
      identifier: [''], // optional
      source: [null],
      description: ['']
    });
  }

  /** Patch the form with vulnerability data */
  private patchVulnerabilityForm(data: Vulnerability): void {
    this.vulnerabilityForm.patchValue({
      name: data.name,
      identifier: data.identifier,
      source: data.source,
      description: data.description
    });
  }

  /** Load "source" (extendable options) from the server */
  private loadSourceOptions(): void {
    this.loaderService.show();
    this.extendableOptionService.getExtendableOptionsByType(OptionType.VULNERABILITY)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (res) => {
          this.sourceOptions = res.results;
        },
        error: (err) => this.toast.error(err?.error?.message)
      });
  }

  /** Handles Save: create or update the Vulnerability */
  public onSave(): void {
    // If the form is invalid, mark everything touched to show errors
    if (this.vulnerabilityForm.invalid) {
      this.vulnerabilityForm.markAllAsTouched();
      return;
    }

    const formValue = this.vulnerabilityForm.value as Vulnerability;

    // If we have an existing vulnerability (edit mode), update
    if (this.isEditMode && this.vulnerability.public_id) {
      this.updateVulnerability(this.vulnerability.public_id, formValue);
    } else {
      this.createVulnerability(formValue);
    }
  }

  /** Create a new vulnerability via service */
  private createVulnerability(newVulnerability: Vulnerability): void {
    this.loaderService.show();
    this.vulnerabilityService.createVulnerability(newVulnerability)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Vulnerability created successfully');
          this.router.navigate(['/isms/vulnerabilities']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  /** Update an existing vulnerability via service */
  private updateVulnerability(id: number, updatedData: Vulnerability): void {
    this.loaderService.show();
    this.vulnerabilityService.updateVulnerability(id, updatedData)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Vulnerability updated successfully');
          this.router.navigate(['/isms/vulnerabilities']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  /** Cancel and go back to the list */
  public onCancel(): void {
    this.router.navigate(['/isms/vulnerabilities']);
  }

  /** Open the Source Manager (ExtendableOptionManager) for "source" */
  public openSourceManager(): void {
    this.showSourceManager = true;
  }

  /** Close the Source Manager and refresh the local source list */
  public closeSourceManager(): void {
    this.showSourceManager = false;
    this.loadSourceOptions();
  }

  /** Helper for the template to show form errors */
  public hasError(controlName: string, error: string): boolean {
    const control = this.vulnerabilityForm.get(controlName);
    return (
      !!control &&
      control.hasError(error) &&
      (control.dirty || control.touched)
    );
  }
}
