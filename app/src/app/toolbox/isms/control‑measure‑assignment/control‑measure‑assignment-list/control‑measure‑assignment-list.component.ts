import {
  Component, Input, OnInit, OnChanges, SimpleChanges,
  TemplateRef, ViewChild
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { LoaderService }  from 'src/app/core/services/loader.service';
import { ToastService }   from 'src/app/layout/toast/toast.service';
import { FilterBuilderService } from 'src/app/core/services/filter-builder.service';

import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { ControlMeasureAssignment } from '../../models/control‑measure‑assignment.model';
import { ControlMeasureAssignmentService } from '../../services/control‑measure‑assignment.service';



@Component({
  selector   : 'app-control-measure-assignment-list',
  templateUrl: './control-measure-assignment-list.component.html',
  styleUrls  : ['./control-measure-assignment-list.component.scss']
})
export class ControlMeasureAssignmentListComponent
        implements OnInit, OnChanges {

  /* ───── optional context IDs (for embedded use) ───── */
  @Input() riskId?: number;
  @Input() controlMeasureId?: number;
  @Input() hideHeader = false;
  @Input() controlMeasureName?: string;
  @Input() riskAssessmentName?: string;


  /* ───── action‑cell template ───── */
  @ViewChild('actionTemplate', { static: true }) actionTemplate!: TemplateRef<any>;

  /* ───── data & table config ───── */
  public assignments: ControlMeasureAssignment[] = [];
  public totalAssignments = 0;

  public page  = 1;
  public limit = 10;
  public loading = false;
  public filter = '';
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING };

  public columns: Column[] = [];
  public initialVisibleColumns: string[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private assignmentSrv: ControlMeasureAssignmentService,
    private loaderService: LoaderService,
    private toast: ToastService,
    private filterBuilder: FilterBuilderService
  ) {}

  /* ═════════ life‑cycle ═════════ */
  ngOnInit(): void {
    /* when routed directly (IDs come from params) */
    if (!this.riskId && !this.controlMeasureId) {
      const rId = this.route.snapshot.paramMap.get('riskId');
      const cm  = this.route.snapshot.paramMap.get('cmId');
      if (rId) this.riskId           = +rId;
      if (cm)  this.controlMeasureId = +cm;
    }

    this.setupColumns();
    this.loadAssignments();
  }

  ngOnChanges(ch: SimpleChanges): void {
    if (ch['riskId'] || ch['controlMeasureId']) {
      this.page = 1;
      this.loadAssignments();
    }
  }

  /* ═════════ columns ═════════ */
  private setupColumns(): void {
    this.columns = [
      { display: 'ID', name: 'public_id', data: 'public_id',
        searchable: false, sortable: true,
        style: { width:'80px','text-align':'center' } },

      { display: 'Control / Measure ID', name: 'control_measure_id',
        data:'control_measure_id', searchable:false, sortable:true },

      { display: 'Risk Assessment ID', name:'risk_assessment_id',
        data:'risk_assessment_id', searchable:false, sortable:true },

      { display: 'Responsible ID', name:'responsible_for_implementation_id',
        data:'responsible_for_implementation_id', searchable:false, sortable:false },

      { display: 'Priority', name:'priority', data:'priority',
        searchable:false, sortable:true,
        style:{ width:'100px','text-align':'center' } },

      { display: 'Implementation Status', name:'implementation_status',
        data:'implementation_status', searchable:false, sortable:true,
        style:{ width:'160px' } },

      { display: 'Actions', name:'actions', data:'public_id',
        template:this.actionTemplate, searchable:false, sortable:false,
        fixed:true, style:{ width:'100px','text-align':'center' } }
    ];
    this.initialVisibleColumns = this.columns.map(c => c.name);
  }

  /* ═════════ data load ═════════ */
  private loadAssignments(): void {
    this.loading = true;
    this.loaderService.show();

    /* free‑text search (IDs only, keep minimal) */
    const searchFilter = this.filter
      ? this.filterBuilder.buildFilter(this.filter, [{ name:'public_id' }])
      : '';

    const ctxFilter =
      this.riskId ? { risk_assessment_id: this.riskId } :
      this.controlMeasureId ? { control_measure_id: this.controlMeasureId } : '';

    const finalFilter = searchFilter && ctxFilter
      ? { $and:[searchFilter, ctxFilter] }
      : (searchFilter || ctxFilter);

    const params: CollectionParameters = {
      filter: finalFilter,
      limit : this.limit,
      page  : this.page,
      sort  : this.sort.name,
      order : this.sort.order
    };

    this.assignmentSrv.getAssignments(params)
      .pipe(finalize(() => {
        this.loading = false;
        this.loaderService.hide();
      }))
      .subscribe({
        next : resp => {
          this.assignments       = resp.results ?? [];
          this.totalAssignments  = resp.total   ?? this.assignments.length;
        },
        error: err => this.toast.error(err?.error?.message ?? 'Failed to load assignments')
      });
  }

  /* ═════════ toolbar & actions ═════════ */
  // public onAddNew(): void {
  //   if (this.riskId) {
  //     this.router.navigate(['/isms/risk_assessments', this.riskId,
  //                           'control_measure_assignments','add']);
  //   } else if (this.controlMeasureId) {
  //     this.router.navigate(['/isms/control_measures', this.controlMeasureId,
  //                           'control_measure_assignments','add']);
  //   }
  // }

  public onAddNew(): void {
    if (this.riskId) {
      // Pass only riskAssessmentName from risk context
      this.router.navigate(
        ['/isms/risk_assessments', this.riskId, 'control_measure_assignments', 'add'],
        { state: { riskAssessmentName: this.riskAssessmentName } }
      );
    } else if (this.controlMeasureId) {
      // Pass only controlMeasureName from control context
      this.router.navigate(
        ['/isms/control_measures', this.controlMeasureId, 'control_measure_assignments', 'add'],
        { state: { controlMeasureName: this.controlMeasureName } }
      );
    }
  }

  public onView(item: ControlMeasureAssignment): void {
    this.router.navigate(
      ['/isms/control-measure-assignments/edit'],
      { state:{ assignment:item, mode:'view' } }
    );
  }

  /* ═════════ cmdb‑table events ═════════ */
  public onPageChange(v:number): void { this.page  = v; this.loadAssignments(); }
  public onPageSizeChange(v:number):void{ this.limit = v; this.page=1; this.loadAssignments(); }
  public onSortChange(s:Sort):void      { this.sort  = s; this.loadAssignments(); }
  public onSearchChange(q:string):void   { this.filter = q; this.page=1; this.loadAssignments(); }
}
