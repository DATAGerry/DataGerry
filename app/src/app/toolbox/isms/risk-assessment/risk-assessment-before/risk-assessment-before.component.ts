// import { Component, Input, OnInit, ChangeDetectionStrategy } from '@angular/core';
// import { FormArray, FormGroup } from '@angular/forms';
// import { RiskMatrixService } from '../../services/risk-matrix.service';
// import { RiskClassService } from '../../services/risk-class.service';
// import { RiskClass } from '../../models/risk-class.model';
// import { ToastService } from 'src/app/layout/toast/toast.service';

// @Component({
//   selector: 'app-risk-assessment-before',
//   templateUrl: './risk-assessment-before.component.html',
//   styleUrls: ['./risk-assessment-before.component.scss'],
// })
// export class RiskAssessmentBeforeComponent implements OnInit {
//   @Input() parentForm!: FormGroup;
//   @Input() impacts: any[] = [];
//   @Input() likelihoods: any[] = [];
//   @Input() impactCategories: any[] = [];
//   @Input() allPersons: any[] = [];
//   @Input() allPersonGroups: any[] = [];

//   /** labels for the single header row (exclude “Not rated”) */
//   public impactScaleLabels: string[] = [];
//   public likelihoodScaleLabels: string[] = [];

//   private riskMatrix: any;
//   public riskClasses: RiskClass[] = [];
//   public calcRiskBgColor: string = '#f5f5f5';  // new property to hold the risk color



//   constructor(
//     private riskAssessmentService: RiskMatrixService,
//     private riskClassService: RiskClassService,
//     private toastService: ToastService
//   ) {
//   }

//   ngOnInit(): void {
//     if (!this.parentForm) { throw new Error('parentForm missing'); }

//     this.impactScaleLabels = this.impacts.map(i => i.name);
//     this.likelihoodScaleLabels = this.likelihoods.map(l => l.name);

//     this.riskAssessmentService.getRiskMatrix(1).subscribe({
//       next: (riskMatrix) => {
//         console.log('Risk Matrix:', riskMatrix);
//         this.riskMatrix = riskMatrix;
//       }
//     })
//   }

//   /*  getters ---------------------------------------------------- */
//   get beforeGroup(): FormGroup {
//     return this.parentForm.get('risk_calculation_before') as FormGroup;
//   }
//   get impactsArray(): FormArray {
//     return this.beforeGroup.get('impacts') as FormArray;
//   }

//   /* slider handlers -------------------------------------------------------- */
//   onImpactChanged(catIndex: number, newImpactId: number | null): void {
//     this.impactsArray.at(catIndex).get('impact_id')?.setValue(newImpactId);
//     this.recalculateRisk();
//   }
//   onLikelihoodChanged(newLhId: number | null): void {
//     this.beforeGroup.get('likelihood_id')?.setValue(newLhId);
//     console.log('New Likelihood ID:', newLhId);
//     this.recalculateRisk();
//   }



//   private recalculateRisk(): void {
//     // Select the impact with the maximum calculation_basis.
//     const selectedImpact = this.impactsArray.controls.reduce((prev: any, ctrl) => {
//       const id = ctrl.get('impact_id')?.value;
//       const imp = this.impacts.find(i => i.public_id === +id);
//       if (!imp) {
//         return prev;
//       }
//       if (!prev) {
//         return imp;
//       }
//       return imp.calculation_basis > prev.calculation_basis ? imp : prev;
//     }, null);

//     // Get the likelihood selection by public_id.
//     const lhId = this.beforeGroup.get('likelihood_id')?.value;
//     const selectedLikelihood = this.likelihoods.find(l => l.public_id === +lhId);

//     // Fallback values if no item is selected.
//     const impactPublicId = selectedImpact ? selectedImpact.public_id : 0;
//     const impactBasis = selectedImpact ? selectedImpact.calculation_basis : 0;
//     const likelihoodPublicId = selectedLikelihood ? selectedLikelihood.public_id : 0;
//     const likelihoodBasis = selectedLikelihood ? selectedLikelihood.calculation_basis : 0;

//     // Compute risk using the original calculation basis.
//     const risk = impactBasis * likelihoodBasis;

//     // Update form controls.
//     this.beforeGroup.patchValue({
//       likelihood_value: likelihoodBasis,
//       maximum_impact_value: impactBasis,
//       risk_level_value: risk
//     }, { emitEvent: false });

//     console.log('impactPublicId:', impactPublicId);
//     console.log('likelihoodPublicId:', likelihoodPublicId);
//     // Pass the public id of the impact and likelihood to getRiskColor.
//     this.calcRiskBgColor = this.getRiskColor(impactPublicId, likelihoodPublicId);
//   }

//   private getRiskColor(impactID: number, likelihoodID: number): string {

//     const riskColor = this.riskMatrix.result.risk_matrix.find((risk) => risk.impact_id === impactID && risk.likelihood_id === likelihoodID);
//     console.log('Risk Color:', riskColor);

//     return this.getCellColor(riskColor?.risk_class_id);

//   }


//   public getCellColor(riskClassID: number): string {

//     console.log('Risk Class ID:', riskClassID);

//     this.riskClassService.getRiskClasses({
//       filter: '',
//       limit: 0,
//       page: 1,
//       sort: '',
//       order: 1
//     }).subscribe({
//       next: (rcResp) => {
//         this.riskClasses = rcResp.results;
//       },
//       error: (err) => this.toastService.error(err)
//     });

//     const rc = this.riskClasses.find(r => r.public_id === riskClassID);
//     console.log('risk color:', rc?.color);
//     return rc?.color || '#f5f5f5';
//   }
// }


// import {
//   ChangeDetectionStrategy,
//   Component,
//   DestroyRef,
//   Input,
//   OnInit,
// } from '@angular/core';
// import { FormArray, FormGroup } from '@angular/forms';
// import {
//   combineLatest,
//   startWith,
// } from 'rxjs';
// import { takeUntilDestroyed } from '@angular/core/rxjs-interop';


// import { RiskClass } from '../../models/risk-class.model';
// import { ToastService } from 'src/app/layout/toast/toast.service';
// import { Impact } from '../../models/impact.model';
// import { Likelihood } from '../../models/likelihood.model';
// import { RiskMatrixCell } from '../../models/risk-matrix.model';
// import { RiskClassService } from '../../services/risk-class.service';

// const FALLBACK_GREY = '#f5f5f5';

// @Component({
//   selector: 'app-risk-assessment-before',
//   templateUrl: './risk-assessment-before.component.html',
//   styleUrls: ['./risk-assessment-before.component.scss'],
//   changeDetection: ChangeDetectionStrategy.OnPush,
// })
// export class RiskAssessmentBeforeComponent implements OnInit {
//   @Input({ required: true }) parentForm!: FormGroup;

//   @Input() impacts: Impact[] = [];
//   @Input() likelihoods: Likelihood[] = [];
//   @Input() impactCategories: { name: string }[] = [];

//   @Input() allPersons: any[] = [];
//   @Input() allPersonGroups: any[] = [];

//   @Input() riskMatrix: any;
// @Input() riskClasses: RiskClass[];

//   /** single header rows (excluding “Not rated”) */
//   impactScaleLabels: string[] = [];
//   likelihoodScaleLabels: string[] = [];

//   /** computed live */
//   calcRiskBgColor = FALLBACK_GREY;

//   // private riskMatrix: any | null = null;
//   private riskClassMap = new Map<number, RiskClass>();

//   constructor(
//     // private readonly riskMatrixService: RiskMatrixService,
//     // private readonly riskClassService: RiskClassService,
//     private readonly toast: ToastService,
//     private readonly destroyRef: DestroyRef
//   ) { }

//   // ───────────────────────────────────────────── lifecycle ──────────
//   // ngOnInit(): void {
//   //   this.impactScaleLabels = this.impacts.map((i) => i.name);
//   //   this.likelihoodScaleLabels = this.likelihoods.map((l) => l.name);

//   //   this.loadStaticData();
//   //   this.bindRecalculation();
//   // }

//   ngOnInit(): void {
//     this.impactScaleLabels = this.impacts.map((i) => i.name);
//     this.likelihoodScaleLabels = this.likelihoods.map((l) => l.name);
//     // Build the map if riskClasses input is provided.
//     if (this.riskClasses) {
//       this.riskClassMap = new Map(this.riskClasses.map((rc) => [rc.public_id, rc]));
//     }
//     this.bindRecalculation();

//     console.log('Risk Classes:', this.riskClasses);
//     console.log('risk matrix:', this.riskMatrix);

//   }

//   // ───────────────────────────────────────── getters ────────────────
//   get beforeGroup(): FormGroup {
//     return this.parentForm.get('risk_calculation_before') as FormGroup;
//   }
//   get impactsArray(): FormArray {
//     return this.beforeGroup.get('impacts') as FormArray;
//   }

//   // ───────────────────────────────────────── private helpers ────────
//   /** static data that never changes for this component instance */
//   // private loadStaticData(): void {
//   //   forkJoin({
//   //     matrix: this.riskMatrixService.getRiskMatrix(1),
//   //     classes: this.riskClassService.getRiskClasses({
//   //       filter: '',
//   //       limit: 0,
//   //       page: 1,
//   //       sort: '',
//   //       order: 1,
//   //     }),
//   //   })
//   //     .pipe(takeUntilDestroyed(this.destroyRef))
//   //     .subscribe({
//   //       next: ({ matrix, classes }) => {
//   //         this.riskMatrix = matrix;
//   //         console.log('Risk Matrix:', this.riskMatrix);
//   //         this.riskClassMap = new Map(
//   //           classes.results.map((rc) => [rc.public_id, rc])
//   //         );
//   //         // trigger initial computation once everything is ready
//   //         this.recalculateRisk();
//   //       },
//   //       error: (err) => this.toast.error(err),
//   //     });
//   // }

//   /** wires form valueChanges → risk recomputation */
//   private bindRecalculation(): void {
//     combineLatest([
//       this.impactsArray.valueChanges.pipe(startWith(this.impactsArray.value)),
//       this.beforeGroup
//         .get('likelihood_id')!
//         .valueChanges.pipe(startWith(this.beforeGroup.get('likelihood_id')!.value)),
//     ])
//       .pipe(takeUntilDestroyed(this.destroyRef))
//       .subscribe(() => this.recalculateRisk());
//   }

//   // ───────────────────────────────────────── calculation ────────────
//   private recalculateRisk(): void {
//     if (!this.riskMatrix) {
//       // wait until static look-ups are loaded
//       return;
//     }

//     // 1️ highest impact basis across all categories
//     const selectedImpact = this.impactsArray.controls
//       .map((ctrl) =>
//         this.impacts.find((i) => i.public_id === +ctrl.get('impact_id')!.value)
//       )
//       .filter(Boolean)
//       .sort((a, b) => (b!.calculation_basis - a!.calculation_basis))[0] ?? null;

//     // 2️ chosen likelihood
//     const lhId = this.beforeGroup.get('likelihood_id')!.value;
//     const selectedLikelihood =
//       this.likelihoods.find((l) => l.public_id === +lhId) ?? null;

//     const impactBasis = selectedImpact?.calculation_basis ?? 0;
//     const likelihoodBasis = selectedLikelihood?.calculation_basis ?? 0;
//     const risk = impactBasis * likelihoodBasis;

//     this.beforeGroup.patchValue(
//       {
//         likelihood_value: likelihoodBasis,
//         maximum_impact_value: impactBasis,
//         risk_level_value: risk,
//       },
//       { emitEvent: false }
//     );

//     this.calcRiskBgColor = this.getRiskColor(
//       selectedImpact?.public_id ?? 0,
//       selectedLikelihood?.public_id ?? 0
//     );
//   }

//   private getRiskColor(
//     impactId: number,
//     likelihoodId: number
//   ): string {
//     const cell: RiskMatrixCell | undefined =
//       this.riskMatrix!.result.risk_matrix.find(
//         (c) => c.impact_id === impactId && c.likelihood_id === likelihoodId
//       );

//     const cls = cell ? this.riskClassMap.get(cell.risk_class_id) : undefined;
//     return cls?.color ?? FALLBACK_GREY;
//   }

//   // ───────────────────────────────────────── template helpers ───────
//   trackByIndex = (_: number, i: any) => i;
// }

import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  Input,
  OnInit,
} from '@angular/core';
import { FormArray, FormGroup } from '@angular/forms';
import {
  combineLatest,
  startWith,
} from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { RiskClass } from '../../models/risk-class.model';
import { Impact } from '../../models/impact.model';
import { Likelihood } from '../../models/likelihood.model';
import { RiskMatrixCell } from '../../models/risk-matrix.model';

const FALLBACK_GREY = '#f5f5f5';

@Component({
  selector: 'app-risk-assessment-before',
  templateUrl: './risk-assessment-before.component.html',
  styleUrls: ['./risk-assessment-before.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RiskAssessmentBeforeComponent implements OnInit {
  @Input({ required: true }) parentForm!: FormGroup;

  @Input() impacts: Impact[] = [];
  @Input() likelihoods: Likelihood[] = [];
  @Input() impactCategories: { name: string }[] = [];

  @Input() allPersons: any[] = [];
  @Input() allPersonGroups: any[] = [];

  @Input() riskMatrix: any;
  @Input() riskClasses: RiskClass[] = [];

  /** single header rows (including "Not rated") */
  impactScaleLabels: string[] = [];
  likelihoodScaleLabels: string[] = [];

  /** computed live */
  calcRiskBgColor = FALLBACK_GREY;

  private riskClassMap = new Map<number, RiskClass>();

  constructor(
    private readonly destroyRef: DestroyRef
  ) { }

  ngOnInit(): void {
    // Include "Not rated" in the labels
    this.impactScaleLabels = ['Not rated', ...this.impacts.map((i) => i.name)];
    this.likelihoodScaleLabels = ['Not rated', ...this.likelihoods.map((l) => l.name)];

    // Build the map if riskClasses input is provided
    if (this.riskClasses && this.riskClasses.length) {
      this.riskClassMap = new Map(this.riskClasses.map((rc) => [rc.public_id, rc]));
    }

    this.bindRecalculation();
  }


  /*
  * Returns the FormGroup of the beforeGroup.
  * @returns {FormGroup}
  */
  get beforeGroup(): FormGroup {
    return this.parentForm.get('risk_calculation_before') as FormGroup;
  }

  /*
  * Returns the FormArray of impacts from the beforeGroup.
  * @returns {FormArray} The FormArray of impacts.
  */
  get impactsArray(): FormArray {
    return this.beforeGroup.get('impacts') as FormArray;
  }


  /*
  * Binds the recalculation of risk to the form value changes.
  * @returns {void}
  */
  private bindRecalculation(): void {
    combineLatest([
      this.impactsArray.valueChanges.pipe(startWith(this.impactsArray.value)),
      this.beforeGroup
        .get('likelihood_id')!
        .valueChanges.pipe(startWith(this.beforeGroup.get('likelihood_id')!.value)),
    ])
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.recalculateRisk());
  }


  /*
    * Recalculates the risk based on the selected impacts and likelihood.
    * 1️ - highest impact basis across all categories
    * 2️ - chosen likelihood
    * Updates the form values and background color accordingly.
    * @returns {void}
    */
  private recalculateRisk(): void {
    if (!this.riskMatrix) {
      return;
    }

    // 1 - highest impact basis across all categories
    const selectedImpact = this.impactsArray.controls
      .map((ctrl) =>
        this.impacts.find((i) => i.public_id === +ctrl.get('impact_id')!.value)
      )
      .filter(Boolean)
      .sort((a, b) => (b!.calculation_basis - a!.calculation_basis))[0] ?? null;

    // 2 - chosen likelihood
    const lhId = this.beforeGroup.get('likelihood_id')!.value;
    const selectedLikelihood =
      this.likelihoods.find((l) => l.public_id === +lhId) ?? null;

    const impactBasis = selectedImpact?.calculation_basis ?? 0;
    const likelihoodBasis = selectedLikelihood?.calculation_basis ?? 0;
    const risk = impactBasis * likelihoodBasis;

    this.beforeGroup.patchValue(
      {
        likelihood_value: likelihoodBasis,
        maximum_impact_value: impactBasis,
        risk_level_value: risk,
      },
      { emitEvent: false }
    );

    this.calcRiskBgColor = this.getRiskColor(
      selectedImpact?.public_id ?? 0,
      selectedLikelihood?.public_id ?? 0
    );
  }

  private getRiskColor(impactId: number, likelihoodId: number): string {
    const cell: RiskMatrixCell | undefined =
      this.riskMatrix?.result?.risk_matrix.find(
        (c) => c.impact_id === impactId && c.likelihood_id === likelihoodId
      );

    const cls = cell ? this.riskClassMap.get(cell.risk_class_id) : undefined;
    return cls?.color ?? FALLBACK_GREY;
  }

  // Template helper
  trackByIndex = (_: number, i: any) => i;
}