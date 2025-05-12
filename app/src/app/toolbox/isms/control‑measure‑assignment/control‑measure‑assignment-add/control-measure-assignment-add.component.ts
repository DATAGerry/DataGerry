import { Component, Input, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { finalize } from 'rxjs/operators';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService }  from 'src/app/layout/toast/toast.service';


import { RiskAssessmentService }           from '../../services/risk-assessment.service';
import { ExtendableOptionService }         from 'src/app/toolbox/isms/services/extendable-option.service';
import { PersonService }                   from '../../services/person.service';
import { PersonGroupService }              from '../../services/person-group.service';

import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { SortDirection } from 'src/app/layout/table/table.types';
import { ControlMeasureAssignment } from '../../models/control‑measure‑assignment.model';
import { ControlMeasureAssignmentService } from '../../services/control‑measure‑assignment.service';
import { ControlMeasureService } from '../../services/control-measure.service';
import { Location } from '@angular/common';

@Component({
  selector   : 'app-control-measure-assignment-add',
  templateUrl: './control-measure-assignment-add.component.html',
  styleUrls  : ['./control-measure-assignment-add.component.scss']
})
export class ControlMeasureAssignmentAddComponent implements OnInit {

  @Input() controlMeasureName?: string;
  @Input() riskAssessmentName?: string;

  /* ── inject ── */
  private readonly fb      = inject(FormBuilder);
  private readonly route   = inject(ActivatedRoute);
  private readonly loader  = inject(LoaderService);
  private readonly toast   = inject(ToastService);

  private readonly srvAssign = inject(ControlMeasureAssignmentService);
  private readonly srvCM     = inject(ControlMeasureService);
  private readonly srvRA     = inject(RiskAssessmentService);
  private readonly srvExtOpt = inject(ExtendableOptionService);
  private readonly srvPerson = inject(PersonService);
  private readonly srvPGroup = inject(PersonGroupService);

  /* ── reactive form ── */
  form!: FormGroup;
  isSaving   = false;
  isLoading$ = this.loader.isLoading$;

  /* ── context (risk or CM) ── */
  private fromRisk = false;
  private fromControlMeasure = false;
  private contextId = 0;

  /* ── reference data ── */
  allControlMeasures: any[] = [];
  allRiskAssessments: any[] = [];
  implementationStates: any[] = [];
  allPersons: any[] = [];
  allPersonGroups: any[] = [];
  responsiblePersonOptions: any[] = [];

  priorityOptions = [
    { label: 'Low', value: 1 },
    { label: 'Medium', value: 2 },
    { label: 'High', value: 3 },
    { label: 'Very High', value: 4 }
  ];

  /* ══════════════════════════════ */

  constructor(private location: Location) {}

  // ngOnInit(): void {
  //   const rId = this.route.snapshot.paramMap.get('riskId');
  //   const cmId = this.route.snapshot.paramMap.get('cmId');
  //   this.fromRisk           = !!rId;
  //   this.fromControlMeasure = !!cmId;
  //   this.contextId          = +(rId ?? cmId ?? 0);

  //   this.buildForm();
  //   this.prefillContext();
  //   this.loadReferenceData();
  // }


  ngOnInit(): void {
    // Capture incoming state from parent
    const state = history.state;
    if (state.riskAssessmentName) {
      this.riskAssessmentName = state.riskAssessmentName;
      this.fromRisk = true;
      // Optionally set contextId if available (or use an appropriate value)
      const rId = this.route.snapshot.paramMap.get('riskId');
      this.contextId = +(rId ?? 0);
    } else if (state.controlMeasureName) {
      this.controlMeasureName = state.controlMeasureName;
      this.fromControlMeasure = true;
      // Optionally set contextId if available (or use an appropriate value)
      const cmId = this.route.snapshot.paramMap.get('cmId');
      this.contextId = +(cmId ?? 0);
    } else {
      // Fallback if no state is passed
      const rId = this.route.snapshot.paramMap.get('riskId');
      const cmId = this.route.snapshot.paramMap.get('cmId');
      this.fromRisk = !!rId;
      this.fromControlMeasure = !!cmId;
      this.contextId = +(rId ?? cmId ?? 0);
    }
  
    this.buildForm();
    this.prefillContext();
    this.loadReferenceData();
  }

  /* ───────────────────────────────────────────── */
  private buildForm(): void {
    this.form = this.fb.group({
      control_measure_id:            [null, Validators.required],
      risk_assessment_id:            [null, Validators.required],
      planned_implementation_date:   null,
      implementation_status:         [null, Validators.required],
      finished_implementation_date:  null,
      priority:                      null,
      responsible_for_implementation_id_ref_type: ['PERSON'],
      responsible_for_implementation_id:          [null, Validators.required]
    });
  }

  private prefillContext(): void {
    if (this.fromRisk) {
      this.form.patchValue({ risk_assessment_id: this.contextId });
      this.form.get('risk_assessment_id')?.disable();
    } else if (this.fromControlMeasure) {
      this.form.patchValue({ control_measure_id: this.contextId });
      this.form.get('control_measure_id')?.disable();
    }
  }

  /* ───────────────────────────────────────────── */
  // private loadReferenceData(): void {
  //   const base: CollectionParameters = {
  //     filter: '',
  //     limit : 0,
  //     page  : 1,
  //     sort  : 'public_id',
  //     order : SortDirection.ASCENDING
  //   };

  //   this.loader.show();
  //   forkJoin({
  //     cms   : this.srvCM.getControlMeasures(base),
  //     ras   : this.srvRA.getRiskAssessments(base),
  //     impls : this.srvExtOpt.getExtendableOptionsByType('IMPLEMENTATION_STATE'),
  //     pers  : this.srvPerson.getPersons(base),
  //     pgrps : this.srvPGroup.getPersonGroups(base)
  //   }).pipe(finalize(() => this.loader.hide()))
  //     .subscribe({
  //       next : (res: any) => {
  //         this.allControlMeasures   = res.cms.results;
  //         this.allRiskAssessments   = res.ras.results;
  //         this.implementationStates = res.impls.results;
  //         this.allPersons           = res.pers.results;
  //         this.allPersonGroups      = res.pgrps.results;
  //         this.buildResponsibleOptions();
  //       },
  //       error: (err) => this.toast.error(err?.error?.message ?? 'Failed to load data')
  //     });
  // }

  // Example update in loadReferenceData():
private loadReferenceData(): void {
  const base: CollectionParameters = {
    filter: '',
    limit : 0,
    page  : 1,
    sort  : 'public_id',
    order : SortDirection.ASCENDING
  };

  const requests: any = {
    impls: this.srvExtOpt.getExtendableOptionsByType('IMPLEMENTATION_STATE'),
    pers : this.srvPerson.getPersons(base),
    pgrps: this.srvPGroup.getPersonGroups(base)
  };

  // Only load control measures if not coming from control measure (i.e. field unlocked)
  if (!this.fromControlMeasure) {
    requests.cms = this.srvCM.getControlMeasures(base);
  }

  // Only load risk assessments if not coming from risk
  if (!this.fromRisk) {
    requests.ras = this.srvRA.getRiskAssessments(base);
  }

  this.loader.show();
  forkJoin(requests)
    .pipe(finalize(() => this.loader.hide()))
    .subscribe({
      next: (res: any) => {
        this.allControlMeasures = res.cms ? res.cms.results : [];
        this.allRiskAssessments = res.ras ? res.ras.results : [];
        this.implementationStates = res.impls.results;
        this.allPersons = res.pers.results;
        this.allPersonGroups = res.pgrps.results;
        this.buildResponsibleOptions();

        console.log('allRiskAssessments', this.allRiskAssessments);
      },
      error: (err) => this.toast.error(err?.error?.message ?? 'Failed to load data')
    });
}

  private buildResponsibleOptions(): void {
    this.responsiblePersonOptions = [
      ...this.allPersonGroups.map(pg => ({
        public_id: pg.public_id,
        display_name: pg.name,
        group: 'Person groups',
        type: 'PERSON_GROUP'
      })),
      ...this.allPersons.map(p => ({
        public_id: p.public_id,
        display_name: p.display_name,
        group: 'Persons',
        type: 'PERSON'
      }))
    ];
  }

  /* ───────────────────────────────────────────── */
  onResponsibleSelected(item: any): void {
    if (!item) return;
    this.form.patchValue({
      responsible_for_implementation_id_ref_type: item.type
    }, { emitEvent: false });
  }

  /* ───────────────────────────────────────────── */
  onSave(): void {
    if (this.form.invalid) {
      this.toast.error('Please fill all mandatory fields.');
      this.form.markAllAsTouched();
      return;
    }

    const payload: ControlMeasureAssignment = {
      ...this.form.getRawValue(),
      ...(this.fromRisk           ? { risk_assessment_id: this.contextId } :
        this.fromControlMeasure   ? { control_measure_id:  this.contextId } : {})
    };

    this.isSaving = true; this.loader.show();
    this.srvAssign.createAssignment(payload)
      .pipe(finalize(() => { this.isSaving = false; this.loader.hide(); }))
      .subscribe({
        next : () => {
          this.toast.success('Control/Measure Assignment created');
          this.goBack();
        },
        error: (err) => this.toast.error(err?.error?.message ?? 'Create failed')
      });
  }

  private goBack(): void {
    this.location.back();

  }

  onCancel(): void { this.goBack(); }
}
