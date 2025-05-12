import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

import { RiskService } from '../../services/risk.service';
import { ThreatService } from '../../services/threat.service';
import { VulnerabilityService } from '../../services/vulnerability.service';
import { ProtectionGoalService } from '../../services/protection-goal.service';

import { Risk } from '../../models/risk.model';
import { Threat } from '../../models/threat.model';
import { Vulnerability } from '../../models/vulnerability.model';
import { ProtectionGoal } from '../../models/protection-goal.model';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { SortDirection } from 'src/app/layout/table/table.types';

@Component({
    selector: 'app-risk-add',
    templateUrl: './risk-add.component.html',
    styleUrls: ['./risk-add.component.scss']
})
export class RiskAddComponent implements OnInit {
    public isEditMode = false;
    public isViewMode = false;
    public isLoading$ = this.loaderService.isLoading$;

    // Main Reactive Form
    public riskForm: FormGroup;
    public risk: Risk = {
        name: '',
        identifier: '',
        risk_type: 'THREAT_X_VULNERABILITY',
        threats: [],
        vulnerabilities: [],
        protection_goals: [],
        description: '',
        consequences: '',

    };

    // Data fetched from other services for multi-select or checkboxes
    public threatOptions: Threat[] = [];
    public vulnerabilityOptions: Vulnerability[] = [];
    public protectionGoalOptions: ProtectionGoal[] = [];

    private params: CollectionParameters = {
        filter: '',
        limit: 0,
        page: 0,
        sort: 'sort',
        order: SortDirection.DESCENDING
    };

    constructor(
        private fb: FormBuilder,
        private router: Router,
        private loaderService: LoaderService,
        private toast: ToastService,
        private riskService: RiskService,
        private threatService: ThreatService,
        private vulnerabilityService: VulnerabilityService,
        private protectionGoalService: ProtectionGoalService
    ) {
        // Check navigation state to see if we're editing an existing risk
        // const navState = this.router.getCurrentNavigation()?.extras?.state;
        // if (navState && navState['risk']) {
        //     this.isEditMode = true;
        //     this.risk = navState['risk'] as Risk;
        // }
        const navState = this.router.getCurrentNavigation()?.extras?.state;

        if (navState && navState['risk']) {
            this.risk = navState['risk'] as Risk;
        
            if (this.router.url.includes('/view')) {
              this.isViewMode = true;
            } else {
              this.isEditMode = true;
            }
          }
    }

    ngOnInit(): void {
        this.initForm();
        if (this.isEditMode || this.isViewMode && this.risk.public_id) {
            this.patchRiskForm(this.risk);
        }

        if(this.isViewMode) {
            this.riskForm.disable();
        }

        // Load references: Threats, Vulnerabilities, and Protection Goals
        this.loadThreats();
        this.loadVulnerabilities();
        this.loadProtectionGoals();
    }

    /* --------------------------------------------------------------
     *  FORM INITIALIZATION
     * -------------------------------------------------------------- */

    private initForm(): void {
        this.riskForm = this.fb.group({
            name: ['', Validators.required],
            identifier: [''],
            risk_type: ['THREAT_X_VULNERABILITY', Validators.required],
            threats: [[]],             // multi-select
            vulnerabilities: [[]],     // multi-select
            description: [''],
            consequences: [''],
            protection_goals: [[], Validators.required]
        });
    }

    private patchRiskForm(data: Risk): void {
        // Patch the form with existing risk data
        this.riskForm.patchValue({
            name: data.name,
            identifier: data.identifier,
            risk_type: data.risk_type,
            threats: data.threats || [],
            vulnerabilities: data.vulnerabilities || [],
            description: data.description,
            consequences: data.consequences,
            protection_goals: data.protection_goals || []
        });
    }

    /* --------------------------------------------------------------
     *  LOADING REFERENCE DATA
     * -------------------------------------------------------------- */

    private loadThreats(): void {
        this.loaderService.show();
        this.threatService.getThreats(this.params)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: (resp) => {
                    this.threatOptions = resp.results;
                },
                error: (err) => this.toast.error(err?.error?.message)
            });
    }

    private loadVulnerabilities(): void {
        this.loaderService.show();
        this.vulnerabilityService.getVulnerabilities(this.params)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: (resp) => {
                    this.vulnerabilityOptions = resp.results;
                },
                error: (err) => this.toast.error(err?.error?.message)
            });
    }

    private loadProtectionGoals(): void {
        this.loaderService.show();
        this.protectionGoalService.getProtectionGoals()
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: (resp) => {
                    this.protectionGoalOptions = resp.results;
                },
                error: (err) => this.toast.error(err?.error?.message)
            });
    }

    /* --------------------------------------------------------------
     *  ADD / UPDATE
     * -------------------------------------------------------------- */

    public onSave(): void {
        // Validate the form
        if (this.riskForm.invalid) {
            this.riskForm.markAllAsTouched();
            return;
        }

        // Gather all data from the form
        const formValue = this.riskForm.value as Risk;
        // We also have to combine the selected protection goal IDs (checkboxes)
        formValue.protection_goals = [...this.selectedProtectionGoals];

        switch (formValue.risk_type) {
            case 'THREAT_X_VULNERABILITY':
                formValue.consequences = '';
                break;
            case 'THREAT':
                formValue.vulnerabilities = [];
                formValue.consequences = '';
                break;
            case 'EVENT':
                formValue.threats = [];
                formValue.vulnerabilities = [];
                break;
        }

        if (this.isEditMode && this.risk.public_id) {
            this.updateRisk(this.risk.public_id, formValue);
        } else {
            this.createRisk(formValue);
        }
    }


    private createRisk(newRisk: Risk): void {
        this.loaderService.show();
        this.riskService.createRisk(newRisk)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: () => {
                    this.toast.success('Risk created successfully');
                    this.router.navigate(['/isms/risks']);
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
    }


    private updateRisk(id: number, updatedData: Risk): void {
        this.loaderService.show();
        this.riskService.updateRisk(id, { ...updatedData, public_id: id })
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: () => {
                    this.toast.success('Risk updated successfully');
                    this.router.navigate(['/isms/risks']);
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
    }


    public onCancel(): void {
        this.router.navigate(['/isms/risks']);
    }

    /* --------------------------------------------------------------
     *  PROTECTION GOALS CHECKBOX LOGIC
     * -------------------------------------------------------------- */

    // We keep a local array that tracks which IDs are checked
    public get selectedProtectionGoals(): number[] {
        return this.riskForm.get('protection_goals')?.value || [];
    }


    public onProtectionGoalChange(pgId: number, checked: boolean): void {
        const currentGoals = this.risk.protection_goals || [];
        if (checked && !currentGoals.includes(pgId)) {
            currentGoals.push(pgId);
        } else if (!checked && currentGoals.includes(pgId)) {
            const index = currentGoals.indexOf(pgId);
            currentGoals.splice(index, 1);
        }
        // Assign back
        // this.risk.protection_goals = [...currentGoals];
        this.riskForm.get('protection_goals')?.setValue([...currentGoals]);
        this.riskForm.get('protection_goals')?.updateValueAndValidity();
    }

    /* --------------------------------------------------------------
     *  CONDITIONAL FIELD DISPLAY
     * -------------------------------------------------------------- */


    // Show/hide multi-select Threat
    public showThreats(): boolean {
        const rt = this.riskForm.get('risk_type')?.value;
        return rt === 'THREAT_X_VULNERABILITY' || rt === 'THREAT';
    }


    // Show/hide multi-select Vulnerability
    public showVulnerabilities(): boolean {
        const rt = this.riskForm.get('risk_type')?.value;
        return rt === 'THREAT_X_VULNERABILITY';
    }

    // Show/hide Consequences textarea
    public showConsequences(): boolean {
        const rt = this.riskForm.get('risk_type')?.value;
        return rt === 'EVENT';
    }

    /* --------------------------------------------------------------
     *  HELPER FOR TEMPLATE FORM ERRORS
     * -------------------------------------------------------------- */


    public hasError(controlName: string, error: string): boolean {
        const control = this.riskForm.get(controlName);
        return !!(control?.hasError(error) && (control.dirty || control.touched));
    }
}
