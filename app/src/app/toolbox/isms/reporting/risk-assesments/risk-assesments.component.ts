
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { FileExportService } from 'src/app/core/services/file-export.service';
import { RiskAssesmentsReportService } from '../../services/risk-assessment-report.service';
import { FilterBuilderService } from 'src/app/core/services/filter-builder.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { getTextColorBasedOnBackground, hexToRgb } from 'src/app/core/utils/color-utils';
import { getCurrentDate } from 'src/app/core/utils/date.utils';
import { forkJoin } from 'rxjs';
import { RiskClassService } from '../../services/risk-class.service';

/* helper ───────────────────────────────────────────────────────── */
type RiskRow = any;
type ProcRow = Record<string, any>;
const slug = (s: string) =>
  s.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
/* ---------------------------------------------------------------- */

@Component({
  selector: 'app-assesments',
  templateUrl: './risk-assesments.component.html',
  styleUrls: ['./risk-assesments.component.scss'],
})
export class RiskAssesmentsComponent implements OnInit {

  /* ───────── templates for coloured boxes ───────── */
  @ViewChild('riskBeforeTpl', { static: true }) riskBeforeTpl!: TemplateRef<any>;
  @ViewChild('riskAfterTpl', { static: true }) riskAfterTpl!: TemplateRef<any>;
  @ViewChild('treatmentOptionTpl', { static: true }) treatmentOptionTpl!: TemplateRef<any>;

  /* ───────── data/state ───────── */
  private rawRows: ProcRow[] = [];
  viewRows: ProcRow[] = [];
  totalItems = 0;
  pagedRows: ProcRow[] = [];

/* ─ Risk-class lookup ─ */
private riskClassLookup = new Map<number, { name: string; color: string }>();

private rcName = (id?: number | null) =>
  id == null ? '' : this.riskClassLookup.get(id)?.name ?? '';

private rcId = (name: string) => {
  for (const [id, obj] of this.riskClassLookup) if (obj.name === name) return id;
  return null;
};



  loading = false;
  isLoading$ = this.loader.isLoading$;
  page = 1;
  limit = 10;
  sort: Sort = { name: 'risk_title', order: SortDirection.ASCENDING };

  textSearch = '';

  columns: Column[] = [];
  initialVisibleColumns: string[] = [];

  /* ───────── chip-filters (unchanged) ───────── */
  ui = { selectedProperty: '', selectedValues: [] as string[] };
  private activeFilters = new Map<string, Set<string>>();
  filterDefs = [
    { label: 'Affected protection goals', key: 'prot_goals_arr' },
    { label: 'Risk category', key: 'risk_category' },
    { label: 'Risk class before treatment', key: 'risk_class_before_id' },
    { label: 'Risk assessor', key: 'risk_assessor' },
    { label: 'Risk owner', key: 'risk_owner' },
    { label: 'Risk treatment option', key: 'risk_treatment_option' },
    { label: 'Responsible person', key: 'responsible_person' },
    { label: 'Implementation status', key: 'implementation_status' },
    { label: 'Priority', key: 'priority' },
    { label: 'Risk class after treatment', key: 'risk_class_after_id' },
  ];

  /* ───────── exports ───────── */
  private exportCols: string[] = [];
  private headerMap: Record<string, string> = {};

  /* ───────── ctor ───────── */
  constructor(
    private readonly api: RiskAssesmentsReportService,
    private readonly rcSvc: RiskClassService,
    private readonly fileExp: FileExportService,
    private readonly loader: LoaderService,
    private readonly toast: ToastService,
    private readonly fb: FilterBuilderService,
  ) { }

  ngOnInit(): void {
    this.buildStaticColumns();              // columns that are always present
    this.loadPage();


    // fetch & render first page

  }

  /* =====================================================================
   *  STATIC COLUMNS  (always visible)
   * ===================================================================*/
  // private buildStaticColumns(): void {
  //   this.columns = [
  //     {
  //       display: 'Risk Title', name: 'risk_title', data: 'risk_title',
  //       searchable: true, sortable: true
  //     },
  //     { display: 'Protection Goals', name: 'prot_goals', data: 'prot_goals' },

  //     {
  //       display: 'Category', name: 'risk_category', data: 'risk_category',
  //       searchable: true, sortable: true
  //     },

  //     {
  //       display: 'Object', name: 'assigned_object', data: 'assigned_object',
  //       searchable: true
  //     },

  //     {
  //       display: 'Object Type', name: 'assigned_object_type', data: 'assigned_object_type',
  //       searchable: true
  //     },

  //     { display: 'LH Before', name: 'likelihood_value_before', data: 'likelihood_value_before' },
  //     {
  //       display: 'Risk Before', name: 'risk_before', data: 'risk_before',
  //       template: this.riskBeforeTpl
  //     },
  //     { display: 'Risk Owner', name: 'risk_owner', data: 'risk_owner' },


  //     { display: 'Assessment Date', name: 'ass_date', data: 'ass_date', sortable: true },
  //     { display: 'Planned Impl. Date', name: 'plan_date', data: 'plan_date' },
  //     { display: 'Finished Impl. Date', name: 'fin_date', data: 'fin_date' },
  //     { display: 'Audit Date', name: 'audit_date', data: 'audit_date' },

  //     {
  //       display: 'Risk After', name: 'risk_after', data: 'risk_after',
  //       template: this.riskAfterTpl
  //     },

  //     { display: 'LH After', name: 'likelihood_value_after', data: 'likelihood_value_after' },

  //     { display: 'Treatment Option', name: 'risk_treatment_option', data: 'risk_treatment_option' },
  //     { display: 'Impl. Status', name: 'implementation_status', data: 'implementation_status' },
  //     { display: 'Priority', name: 'priority', data: 'priority' },

  //     { display: 'Responsible', name: 'responsible_person', data: 'responsible_person' },
  //     { display: 'Auditor', name: 'auditor', data: 'auditor' },

  //     { display: 'Additional Info', name: 'additional_info', data: 'additional_info' },
  //     { display: 'Treatment Desc.', name: 'risk_treatment_description', data: 'risk_treatment_description' },
  //     { display: 'Resources', name: 'required_resources', data: 'required_resources' },
  //     { display: 'Cost', name: 'costs_for_implementation', data: 'costs_for_implementation' },
  //     { display: 'Currency', name: 'costs_for_implementation_currency', data: 'costs_for_implementation_currency' },
  //   ];
  //   this.initialVisibleColumns = this.columns.map(c => c.name);
  // }

  /* =====================================================================
 *  STATIC COLUMNS  (always visible, ordered as in spec)
 * ===================================================================*/
  private buildStaticColumns(): void {
    this.columns = [
      /* ───────── Risk attributes ───────── */
      { display: 'Risk Title', name: 'risk_title', data: 'risk_title', searchable: true, sortable: true },
      { display: 'Protection Goals', name: 'prot_goals', data: 'prot_goals' },
      { display: 'Risk Category', name: 'risk_category', data: 'risk_category', searchable: true, sortable: true },

      /* ───────── Assigned object / group ───────── */
      { display: 'Object / Group', name: 'assigned_object', data: 'assigned_object', searchable: true },
      { display: 'Object Type', name: 'assigned_object_type', data: 'assigned_object_type' },

      /* ── «before» impact-category columns will be spliced in here ── */

      { display: 'LH Before', name: 'likelihood_value_before', data: 'likelihood_value_before' },
      { display: 'Risk Before', name: 'risk_before', data: 'risk_before', template: this.riskBeforeTpl },

      /* ───────── Personnel & dates (before) ───────── */
      { display: 'Risk Assessor', name: 'risk_assessor', data: 'risk_assessor' },
      { display: 'Risk Owner', name: 'risk_owner', data: 'risk_owner' },
      { display: 'Interviewed', name: 'interviewed', data: 'interviewed' },
      { display: 'Assessment Date', name: 'ass_date', data: 'ass_date', sortable: true },
      { display: 'Additional Info', name: 'additional_info', data: 'additional_info' },

      /* ───────── Treatment ───────── */
      { display: 'Treatment Option', name: 'risk_treatment_option', data: 'risk_treatment_option', template: this.treatmentOptionTpl },
      { display: 'Responsible', name: 'responsible_person', data: 'responsible_person' },
      { display: 'Treatment Desc.', name: 'risk_treatment_description', data: 'risk_treatment_description' },
      { display: 'Planned Impl. Date', name: 'plan_date', data: 'plan_date' },
      { display: 'Impl. Status', name: 'implementation_status', data: 'implementation_status' },
      { display: 'Finished Impl. Date', name: 'fin_date', data: 'fin_date' },
      { display: 'Resources', name: 'required_resources', data: 'required_resources' },
      { display: 'Cost', name: 'costs_for_implementation', data: 'costs_for_implementation' },
      { display: 'Priority', name: 'priority', data: 'priority' },

      /* ── «after» impact-category columns will be spliced in here ── */

      { display: 'LH After', name: 'likelihood_value_after', data: 'likelihood_value_after' },
      { display: 'Risk After', name: 'risk_after', data: 'risk_after', template: this.riskAfterTpl },

      /* ───────── Audit ───────── */
      { display: 'Audit Date', name: 'audit_date', data: 'audit_date' },
      { display: 'Auditor', name: 'auditor', data: 'auditor' },
      { display: 'Audit Result', name: 'audit_result', data: 'audit_result' },
    ];

    this.initialVisibleColumns = this.columns.map(c => c.name);
  }


  /* =====================================================================
   *  DYNAMIC IMPACT-CATEGORY COLUMNS
   * ===================================================================*/

  // private addImpactColumns(categories: string[]): void {
  //   const already = new Set(this.columns.map(c => c.name));

  //   // First add all (Before) columns
  //   categories.forEach(cat => {
  //     const keyB = `before_${slug(cat)}`;
  //     if (!already.has(keyB)) {
  //       this.columns.push({ display: `${cat} (Before)`, name: keyB, data: keyB });
  //       this.initialVisibleColumns.push(keyB);
  //     }
  //   });

  //   // Then add all (After) columns
  //   categories.forEach(cat => {
  //     const keyA = `after_${slug(cat)}`;
  //     if (!already.has(keyA)) {
  //       this.columns.push({ display: `${cat} (After)`, name: keyA, data: keyA });
  //       this.initialVisibleColumns.push(keyA);
  //     }
  //   });

  //   /* update export columns */
  //   this.exportCols = this.columns.map(c => c.display);
  //   this.headerMap = this.exportCols.reduce(
  //     (m, c) => { m[c] = c; return m; }, {} as Record<string, string>);
  // }

  /* =====================================================================
 *  DYNAMIC IMPACT-CATEGORY COLUMNS  (clean two-step version)
 * ===================================================================*/
  private addImpactColumns(categories: string[]): void {
    this.clearImpactColumns();
    this.addBeforeImpactColumns(categories);
    this.addAfterImpactColumns(categories);

    /* refresh export metadata once, after both inserts */
    this.exportCols = this.columns.map(c => c.display);
    this.headerMap = Object.fromEntries(this.exportCols.map(c => [c, c]));
  }

  /* ---------- helpers ---------- */
  private addBeforeImpactColumns(categories: string[]): void {
    const anchor = this.columns.findIndex(c => c.name === 'likelihood_value_before');
    const cols = categories.map(cat => this.makeImpactCol(cat, 'before'));
    this.columns.splice(anchor, 0, ...cols);
  }

  private addAfterImpactColumns(categories: string[]): void {
    const anchor = this.columns.findIndex(c => c.name === 'likelihood_value_after');
    const cols = categories.map(cat => this.makeImpactCol(cat, 'after'));
    this.columns.splice(anchor, 0, ...cols);
  }

  private makeImpactCol(cat: string, phase: 'before' | 'after'): Column {
    const key = `${phase}_${slug(cat)}`;
    return {
      display: `${cat} (${phase === 'before' ? 'Before' : 'After'})`,
      name: key,
      data: key
    };
  }

  private clearImpactColumns(): void {
    const dynamic = (name: string) => name.startsWith('before_') || name.startsWith('after_');

    /* strip from columns */
    this.columns = this.columns.filter(c => !dynamic(c.name));

    /* strip from visible-columns cache */
    this.initialVisibleColumns =
      this.initialVisibleColumns.filter(name => !dynamic(name));
  }



  /* =====================================================================
   *  DATA LOAD  (pagination + filters → backend)
   * ===================================================================*/
  private buildBackendFilter(): any {
    const nodes: any[] = [];

    if (this.textSearch) {
      nodes.push({
        op: 'or',
        rhs: this.fb.buildFilter(
          this.textSearch,
          [{ name: 'risk_title' }, { name: 'risk_category' }, { name: 'protection_goals' }]
        )
      });
    }
    this.activeFilters.forEach((set, prop) => {
      nodes.push({ op: 'in', lhs: prop, rhs: Array.from(set) });
    });

    if (!nodes.length) return '';
    if (nodes.length === 1) return nodes[0];
    return { op: 'and', rhs: nodes };
  }


  private loadPage(): void {

    this.loading = true;
    this.loader.show();

    forkJoin({
            assessments: this.api.getRiskAssesmentsReportList(),
            classesRes:  this.rcSvc.getRiskClasses()
          })
      .pipe(finalize(() => {
        this.loading = false;
        this.loader.hide();
      }))
      .subscribe({
        next: ({ assessments: list, classesRes }) => {


          this.riskClassLookup.clear();
    (classesRes.results || []).forEach(c =>
      this.riskClassLookup.set(c.public_id, { name: c.name, color: c.color })
    );

          /* ── gather the distinct impact-category names ─────────── */
          const catSet = new Set<string>();
          list.forEach(r => {
            (r.impact_categories_before || []).forEach((ic: any) => catSet.add(ic.impact_category));
            (r.impact_categories_after || []).forEach((ic: any) => catSet.add(ic.impact_category));
          });
          const categories = Array.from(catSet).sort();
          this.addImpactColumns(categories);  // add dynamic columns

          /* ── flatten every row + fill per-category cells ───────── */
          this.rawRows = list.map((r: RiskRow): ProcRow => {

            const beforeId = r.risk_before?.risk_class_id ?? null;
            const afterId  = r.risk_after ?.risk_class_id ?? null;

            const row: ProcRow = {
              ...r,
              ass_date: this.fmtDate(r.risk_assessment_date),
              plan_date: this.fmtDate(r.planned_implementation_date),
              fin_date: this.fmtDate(r.finished_implementation_date),
              audit_date: this.fmtDate(r.audit_done_date),
              prot_goals: (r.protection_goals ?? []).join(', '),
              prot_goals_arr: r.protection_goals ?? [],
              interviewed: (r.interviewed_persons ?? []).join(', '),
              // risk_class_before: r.risk_before?.risk_class?.label ?? '',
              // risk_class_after: r.risk_after?.risk_class?.label ?? '',
              risk_class_before: this.rcName(beforeId),
              risk_class_after : this.rcName(afterId),

              risk_class_before_id: beforeId,
              risk_class_after_id : afterId,


            };

            /* initialise empty cells … */
            categories.forEach(cat => {
              row[`before_${slug(cat)}`] = '';
              row[`after_${slug(cat)}`] = '';
            });
            /* …and fill values that exist */
            (r.impact_categories_before || []).forEach((ic: any) =>
              row[`before_${slug(ic.impact_category)}`] = ic.impact_value ?? '');
            (r.impact_categories_after || []).forEach((ic: any) =>
              row[`after_${slug(ic.impact_category)}`] = ic.impact_value ?? '');

            return row;
          });

          /* ── apply chip-filters and search ─────────────── */
          this.applyAllFilters();
        },

        error: err => this.toast.error(err?.error?.message ?? 'Load failed')
      });
  }

  // private applyAllFilters(): void {

  //   let rows = [...this.rawRows];

  //   /* ── apply chip-filters ───────────── */
  //   this.activeFilters.forEach((set, prop) => {
  //     rows = rows.filter(r => {
  //       const val = r[prop];
  //       if (Array.isArray(val)) return val.some(v => set.has(String(v)));
  //       return set.has(String(val));
  //     });
  //   });

  //   /* ── apply search ───────────── */
  //   if (this.textSearch) {
  //     const search = this.textSearch.toLowerCase();
  //     rows = rows.filter(r =>
  //       (r.risk_title ?? '').toLowerCase().includes(search) ||
  //       (r.risk_category ?? '').toLowerCase().includes(search) ||
  //       (r.prot_goals ?? '').toLowerCase().includes(search)
  //     );
  //   }

  //   /* ── final ───────────── */
  //   this.viewRows = rows;
  //   this.totalItems = rows.length;
  // }

  private applyAllFilters(): void {

    let rows = [...this.rawRows];

    // apply chip-filters
    this.activeFilters.forEach((set, prop) => {
      rows = rows.filter(r => {
        const val = r[prop];
        if (Array.isArray(val)) return val.some(v => set.has(String(v)));
        return set.has(String(val));
      });
    });

    // apply search
    if (this.textSearch) {
      const search = this.textSearch.toLowerCase();
      rows = rows.filter(r =>
        (r.risk_title ?? '').toLowerCase().includes(search) ||
        (r.risk_category ?? '').toLowerCase().includes(search) ||
        (r.prot_goals ?? '').toLowerCase().includes(search)
      );
    }

    // final
    this.viewRows = rows;
    this.totalItems = rows.length;
    this.pagedRows = this.viewRows.slice((this.page - 1) * this.limit, this.page * this.limit);
  }


  private updatePagedRows(): void {
    this.pagedRows = this.viewRows.slice((this.page - 1) * this.limit, this.page * this.limit);
  }



  /* =====================================================================
   *  SMALL HELPERS
   * ===================================================================*/

  private fmtDate(d?: { year: number, month: number, day: number } | null): string {
    if (!d) return '';
    return `${d.year}-${`${d.month}`.padStart(2, '0')}-${`${d.day}`.padStart(2, '0')}`;
  }

  /* =====================================================================
   *  CHIP-FILTER UI 
   * ===================================================================*/
  // getValues(prop: string) {
  //   const s = new Set<string>();

  //   // Always take from rawRows (not viewRows), to see full possible values
  //   this.rawRows.forEach(r => {
  //     const v = r[prop];
  //     if (Array.isArray(v)) v.forEach(x => s.add(String(x)));
  //     else if (v != null && v !== '') s.add(String(v));
  //   });

  //   // Remove already selected values for this property (if any)
  //   const selectedSet = this.activeFilters.get(prop);
  //   if (selectedSet) {
  //     selectedSet.forEach(val => s.delete(val));
  //   }

  //   return [...s].sort();
  // }

  getValues(prop: string) {
    if (prop === 'risk_class_before_id' || prop === 'risk_class_after_id') {
      const names = new Set<string>();
      this.rawRows.forEach(r => names.add(this.rcName(r[prop])));
      this.activeFilters.get(prop)?.forEach(id => names.delete(this.rcName(+id)));
      return [...names].filter(Boolean).sort();
    }
  
    /* default logic (unchanged) */
    const s = new Set<string>();
    this.rawRows.forEach(r => {
      const v = r[prop];
      if (Array.isArray(v)) v.forEach(x => s.add(String(x)));
      else if (v != null && v !== '') s.add(String(v));
    });
    this.activeFilters.get(prop)?.forEach(val => s.delete(val));
    return [...s].sort();
  }
  

  get hasActiveFilters() { return this.activeFilters.size > 0; }
  // get activeFilterChips() {
  //   const out: string[] = [];
  //   this.activeFilters.forEach((set, k) => {
  //     const lbl = this.filterDefs.find(f => f.key === k)?.label;
  //     out.push(...Array.from(set).map(v => `${lbl}: ${v}`));
  //   });
  //   return out;
  // }

  get activeFilterChips() {
    const out: string[] = [];
    this.activeFilters.forEach((set, k) => {
      const lbl = this.filterDefs.find(f => f.key === k)?.label;
      set.forEach(v => {
        const display = (k === 'risk_class_before_id' || k === 'risk_class_after_id')
          ? this.rcName(+v)
          : v;
        out.push(`${lbl}: ${display}`);
      });
    });
    return out;
  }



  // applyFilter() {
  //   const { selectedProperty: p, selectedValues: vals } = this.ui;
  //   if (!p || !vals.length) return;
  //   const set = this.activeFilters.get(p) ?? new Set<string>();
  //   vals.forEach(v => set.add(v));
  //   this.activeFilters.set(p, set);
  //   this.ui.selectedProperty = ''; this.ui.selectedValues = [];
  //   this.page = 1; this.loadPage();
  // }

  applyFilter() {
    const { selectedProperty: p, selectedValues: vals } = this.ui;
    if (!p || !vals.length) return;
  
    const set = this.activeFilters.get(p) ?? new Set<string>();
  
    if (p === 'risk_class_before_id' || p === 'risk_class_after_id') {
      vals.forEach(name => {
        const id = this.rcId(name);
        if (id != null) set.add(String(id));
      });
    } else {
      vals.forEach(v => set.add(v));
    }
  
    this.activeFilters.set(p, set);
    this.ui.selectedProperty = ''; this.ui.selectedValues = [];
    this.page = 1; this.loadPage();
  }
  
  // removeFilter(i: number) {
  //   const [lbl, val] = this.activeFilterChips[i].split(':').map(s => s.trim());
  //   const k = this.filterDefs.find(f => f.label === lbl)?.key; if (!k) return;
  //   const set = this.activeFilters.get(k); if (!set) return;
  //   set.delete(val); if (!set.size) this.activeFilters.delete(k);
  //   this.page = 1; this.loadPage();
  // }
  removeFilter(i: number) {
    const [lbl, val] = this.activeFilterChips[i].split(':').map(s => s.trim());
    const k = this.filterDefs.find(f => f.label === lbl)?.key; if (!k) return;
  
    const set = this.activeFilters.get(k); if (!set) return;
  
    const keyVal =
      (k === 'risk_class_before_id' || k === 'risk_class_after_id')
        ? String(this.rcId(val))
        : val;
  
    set.delete(keyVal);
    if (!set.size) this.activeFilters.delete(k);
    this.page = 1; this.loadPage();
  }
  clearFilters() { this.activeFilters.clear(); this.page = 1; this.loadPage(); }

  /* =====================================================================
   *  TABLE EVENTS
   * ===================================================================*/
  onPageChange(p: number) {
    this.page = p;
    this.updatePagedRows();
  }
  onPageSizeChange(l: number) {
    this.limit = l;
    this.page = 1;
    this.updatePagedRows();
  }
  onSortChange(s: Sort) { this.sort = s; this.loadPage(); }
  onSearchChange(txt: string) { this.textSearch = txt; this.page = 1; this.loadPage(); }

  /* =====================================================================
   *  EXPORTS  – auto-generated from current columns
   * ===================================================================*/

  private exportRows() {
    return this.viewRows.map(r => {
      const o: Record<string, any> = {};

      this.columns.forEach(c => {
        if (c.name === 'risk_before' || c.name === 'risk_after') {
          // Export full object (keep color+value)
          o[c.display] = r[c.name];  // not just value!
        } else {
          o[c.display] = r[c.data] ?? '';
        }
      });

      return o;
    });
  }



  exportCsv() { this.fileExp.exportCsv(`risk-assessments_${getCurrentDate()}`, this.exportRows(), this.exportCols, this.headerMap); }
  exportXlsx() { this.fileExp.exportXlsx(`risk-assessments_${getCurrentDate()}`, this.exportRows(), this.exportCols, this.headerMap); }
  exportPdf(): void {

    /* calculate required width */
    const colMin = 110;
    const tableW = this.exportCols.length * colMin;
    const margins = 40;
    const pageW = Math.max(842, tableW + margins);  // wider if needed

    /* create PDF */
    const pdf = new jsPDF({
      orientation: 'l',
      unit: 'pt',
      format: [pageW, 595]
    });

    /* prepare rows */
    const rows = this.exportRows();

    autoTable(pdf, {
      head: [this.exportCols],
      body: rows.map(r => this.exportCols.map(k => r[k])),

      startY: 30,
      margin: { top: 30, bottom: 20, left: 20, right: 20 },

      styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },

      headStyles: {
        fontSize: 8,
        fillColor: [47, 102, 153],  // blue
        textColor: 255,
        halign: 'left',
        valign: 'middle'
      },

      columnStyles: this.exportCols.reduce((acc, _, idx) => {
        acc[idx] = { cellWidth: 'auto' };
        return acc;
      }, {} as any),

      didParseCell: data => {
        if (data.row.section === 'body') {  // Only process data rows
          const colName = this.columns[data.column.index]?.name;
          if (colName === 'risk_before' || colName === 'risk_after') {
            const rowIndex = data.row.index;
            const rowData = this.viewRows[rowIndex];
            const riskObj = colName === 'risk_before' ? rowData.risk_before : rowData.risk_after;
            const colorHex = riskObj?.color || '#f5f5f5';
            const value = riskObj?.value ?? '0';
            const rgb = hexToRgb(colorHex);
            data.cell.styles.fillColor = rgb;
            data.cell.text = [String(value)];
          }
        }
      },

      /* footer */
      didDrawPage: ({ pageNumber }) => {
        pdf.setFontSize(9);
        pdf.text(
          `Page ${pageNumber} / ${pdf.getNumberOfPages()}`,
          pdf.internal.pageSize.getWidth() - 60,
          pdf.internal.pageSize.getHeight() - 10
        );
      }
    });

    pdf.save(`risk-assessments_${getCurrentDate()}`);
  }

  /**
   * Wrapper for getTextColorBasedOnBackground to make it accessible in the template.
   */
  public getTextColor(color: string): string {
    return getTextColorBasedOnBackground(color);
  }



}
