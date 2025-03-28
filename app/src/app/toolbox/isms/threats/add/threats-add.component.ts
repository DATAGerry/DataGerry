import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

import { ThreatService } from '../../services/threat.service';
import { Threat } from '../../models/threat.model';

import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';
import { OptionType } from 'src/app/toolbox/isms/models/option-type.enum';

@Component({
  selector: 'app-threats-add',
  templateUrl: './threats-add.component.html',
  styleUrls: ['./threats-add.component.scss']
})
export class ThreatsAddComponent implements OnInit {
  public isEditMode = false;
  public threatId?: number;
  public isLoading$ = this.loaderService.isLoading$;

  public sourceOptions: ExtendableOption[] = [];

  public threatForm: FormGroup;

  public threat: Threat = {
    name: '',
    source: [],
    identifier: '',
    description: ''
  };

  public showSourceManager = false;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private threatService: ThreatService,
    private loaderService: LoaderService,
    private toast: ToastService,
    private extendableOptionService: ExtendableOptionService
  ) {}

  ngOnInit(): void {
    this.threatId = +this.route.snapshot.paramMap.get('id');
    this.isEditMode = !!this.threatId;

    this.initForm();

    // Load the dropdown options
    this.loadSourceOptions();

    // If editing, fetch data from the server and patch the form
    if (this.isEditMode && this.threatId) {
      this.loadThreatToEdit(this.threatId);
    }
  }

  /** Create the FormGroup with default values and validators */
  private initForm(): void {
    this.threatForm = this.fb.group({
      name: ['', Validators.required],
      identifier: [''], // optional
      source: [null, Validators.required],
      description: ['']
    });
  }

  /** Load the source (extendable options) data */
  private loadSourceOptions(): void {
    this.loaderService.show();
    this.extendableOptionService.getExtendableOptionsByType(OptionType.THREAT)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (res) => {
          this.sourceOptions = res.results;
        },
        error: (err) => this.toast.error(err?.error?.message)
      });
  }

  /** If editing an existing threat, fetch and patch the form controls */
  private loadThreatToEdit(id: number): void {
    this.loaderService.show();
    this.threatService.getThreatById(id)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (resp) => {
          const item = resp.result;
          this.threat = {
            public_id: item.public_id,
            name: item.name,
            source: item.source,
            identifier: item.identifier,
            description: item.description
          };
          // Patch form values so user sees them
          this.threatForm.patchValue({
            name: this.threat.name,
            identifier: this.threat.identifier,
            source: this.threat.source,
            description: this.threat.description
          });
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
          this.router.navigate(['/isms/threats']);
        }
      });
  }

  /** On form submission, create or update the threat */
  public onSave(): void {
    // If form is invalid, just return
    if (this.threatForm.invalid) {
      // Optionally mark all controls as touched to show errors
      this.threatForm.markAllAsTouched();
      return;
    }

    const formValue = this.threatForm.value as Threat;
    // If editing, we keep the existing public_id if present
    if (this.isEditMode && this.threat.public_id) {
      this.updateThreat(this.threat.public_id, formValue);
    } else {
      this.createThreat(formValue);
    }
  }

  private createThreat(newThreat: Threat): void {
    this.loaderService.show();
    this.threatService.createThreat(newThreat)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Threat created successfully');
          this.router.navigate(['/isms/threats']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }x

  private updateThreat(id: number, updatedThreat: Threat): void {
    this.loaderService.show();
    this.threatService.updateThreat(id, updatedThreat)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: () => {
          this.toast.success('Threat updated successfully');
          this.router.navigate(['/isms/threats']);
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  public onCancel(): void {
    this.router.navigate(['/isms/threats']);
  }

  // Open/close the Source Manager (ExtendableOptionManager) for "Threat Source"
  public openSourceManager(): void {
    this.showSourceManager = true;
  }

  public closeSourceManager(): void {
    this.showSourceManager = false;
    // Refresh the local source list after closing manager
    this.loadSourceOptions();
  }

  /** Helper for easier template access */
  public hasError(controlName: string, error: string): boolean {
    const control = this.threatForm.get(controlName);
    return (
      !!control &&
      control.hasError(error) &&
      (control.dirty || control.touched)
    );
  }
}
