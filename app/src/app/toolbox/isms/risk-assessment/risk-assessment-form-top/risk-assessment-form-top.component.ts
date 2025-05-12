// import { Component, Input, OnInit } from '@angular/core';
// import { FormGroup } from '@angular/forms';
// import { ActivatedRoute, Router } from '@angular/router';

// @Component({
//   selector: 'app-risk-assessment-form-top',
//   templateUrl: './risk-assessment-form-top.component.html',
//   styleUrls: ['./risk-assessment-form-top.component.scss']
// })
// export class RiskAssessmentFormTopComponent implements OnInit {
//   @Input() parentForm!: FormGroup;
//   @Input() fromRisk = false;
//   @Input() fromObject = false;
//   @Input() fromObjectGroup = false;
//   @Input() risks: any[] = [];
//   @Input() objects: any[] = [];
//   @Input() objectGroups: any[] = [];
//   @Input() objectSummary: string | null = null; 
//   @Input() riskSummaryLine: string | null = null;


//   public objectRefTypes = [
//     { label: 'Object', value: 'OBJECT' },
//     { label: 'Object Group', value: 'OBJECT_GROUP' }
//   ];

//   ngOnInit(): void {

//     console.log('objectss', this.objects);

//     const state = history.state as { objectSummary?: string };
//     if (state?.objectSummary) {
//       this.objectSummary = state.objectSummary;
//     }


//     if (this.fromObject || this.fromObjectGroup) {
//       this.parentForm.get('object_id_ref_type')?.disable();
//     }
//     console.log('fromRisk:', this.fromRisk)
//     console.log('fromObject:', this.fromObject);
//   }
// }



import { Component, inject, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { TypeService } from 'src/app/framework/services/type.service';
import { ObjectService } from 'src/app/framework/services/object.service';
import { RenderResult } from 'src/app/framework/models/cmdb-render';

/* Minimal CMDB typings */
interface CmdbType   { public_id: number; }
interface CmdbObject { public_id: number; type_id: number; name: string; }

@Component({
  selector: 'app-risk-assessment-form-top',
  templateUrl: './risk-assessment-form-top.component.html',
  styleUrls: ['./risk-assessment-form-top.component.scss']
})
export class RiskAssessmentFormTopComponent implements OnInit {

  /* ──────── Inputs ──────── */
  @Input() parentForm!: FormGroup;

  @Input() fromRisk        = false;
  @Input() fromObject      = false;
  @Input() fromObjectGroup = false;

  @Input() risks:        any[]        = [];
  @Input() objects:      CmdbObject[] = [];
  @Input() objectGroups: any[]        = [];

  @Input() objectSummary:   string | null = null;
  @Input() riskSummaryLine: string | null = null;
  @Input() mode: 'EDIT' | 'VIEW' = 'EDIT';

  /* ──────── Services ──────── */
  private readonly typeService   = inject(TypeService);
  private readonly loader        = inject(LoaderService);
  private readonly toast         = inject(ToastService);
  private readonly objectService = inject(ObjectService);

  /* ──────── State ──────── */
  public riskName: string | null = null;
  public selectedObjectRenderResult: RenderResult | null = null;
  public isObjectLoading = false;

  public allTypeIds: number[] = [];
  public typesLoaded = false;

  public objectRefTypes = [
    { label: 'Object',       value: 'OBJECT' },
    { label: 'Object Group', value: 'OBJECT_GROUP' }
  ];

  private static cachedTypes: CmdbType[] | null = null;

  /* ══════════════════════════════════════ */
  ngOnInit(): void {

    console.log('fromRisk:', this.fromRisk);
    console.log('fromObject:', this.fromObject);
    console.log('fromObjectGroup:', this.fromObjectGroup);
    const objectId = this.parentForm.get('object_id')?.value;

    if (this.fromRisk) {
      const riskId = +this.parentForm.get('risk_id')!.value;
      this.riskName =
        this.risks.find(r => r.public_id === riskId)?.name
        ?? this.riskSummaryLine
        ?? null;

      this.loadTypesIfNeeded();
    }

    console.log('from topppp objectId:', objectId, 'mode', this.mode);
    

    if (this.fromObject || this.fromObjectGroup) {
      this.parentForm.get('object_id_ref_type')?.disable();
    }

    if ((this.fromObject || (this.fromRisk && this.mode === 'VIEW')) && objectId) {        
      this.loadSelectedObjectRenderResult(objectId);
    }
  }

  public onObjectSelected(ids: number[]): void {
    this.parentForm.get('object_id')?.setValue(ids?.[0] ?? null);
  }

  private loadTypesIfNeeded(): void {
    if (RiskAssessmentFormTopComponent.cachedTypes) {
      this.allTypeIds = RiskAssessmentFormTopComponent.cachedTypes.map(t => t.public_id);
      this.typesLoaded = true;
      return;
    }

    this.loader.show();
    const params = { filter: '', limit: 0, sort: 'sort', order: 1, page: 1 };

    this.typeService.getTypes(params)
      .pipe(finalize(() => this.loader.hide()))
      .subscribe({
        next: (resp) => {
          const types = resp.results as CmdbType[];
          RiskAssessmentFormTopComponent.cachedTypes = types;
          this.allTypeIds = types.map(t => t.public_id);
          this.typesLoaded = true;
        },
        error: (err) => {
          this.toast.error(err?.error?.message ?? 'Failed to load types');
        }
      });
  }

  private loadSelectedObjectRenderResult(objectId: number): void {
    console.log('loadSelectedObjectRenderResult called with objectId:', objectId);
    if (!objectId) return;

    this.isObjectLoading = true;
    const params = {
      filter: { public_id: objectId },
      limit: 1,
      sort: '',
      order: 1,
      page: 1
    };

    this.objectService.getObjects(params)
      .pipe(finalize(() => (this.isObjectLoading = false)))
      .subscribe({
        next: (resp) => {
          const result = resp?.results?.[0];
          if (result?.object_information) {
            this.selectedObjectRenderResult = result as RenderResult;
          }
        },
        error: (err) => {
          this.toast.error(err?.error?.message ?? 'Failed to load object');
        }
      });
  }
}
