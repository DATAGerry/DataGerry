import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';


import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { FilterBuilderService } from 'src/app/core/services/filter-builder.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { SoaService } from '../../services/soa.service';
import { ControlMeasure } from '../../models/control-measure.model';

@Component({
  selector: 'app-soa',
  templateUrl: './soa.component.html'})
export class SoaComponent implements OnInit {

  /* ===== Table data ===== */
  public controls: ControlMeasure[] = [];
  public totalControls = 0;

  /* ===== Table state ===== */
  public page  = 1;
  public limit = 10;
  public loading = false;
  public filter = '';
  public sort: Sort = { name: 'identifier', order: SortDirection.ASCENDING };

  /* ===== Column definitions ===== */
  public columns: Column[] = [];
  public initialVisibleColumns: string[] = [];

  constructor(
    private readonly soaService: SoaService,
    private readonly loader: LoaderService,
    private readonly toast: ToastService,
    private readonly filterBuilder: FilterBuilderService,
  ) {}

  ngOnInit(): void {
    this.setupColumns();
    this.loadControls();
  }

  /* ---------------------------------- Columns ---------------------------------- */
  private setupColumns(): void {
    this.columns = [
      { display: 'Identifier', name: 'identifier', data: 'identifier', searchable: false, sortable: true, style: { width: '100px', 'text-align': 'center' } },
      { display: 'Title',      name: 'title',      data: 'title',      searchable: true,  sortable: true },
      { display: 'Chapter',    name: 'chapter',    data: 'chapter',    searchable: true,  sortable: true },
      { display: 'Applicable', name: 'is_applicable', data: 'is_applicable', searchable: false, sortable: true, style: { width: '120px', 'text-align': 'center' } },
      { display: 'Reason',     name: 'reason',     data: 'reason',     searchable: true,  sortable: false },
      { display: 'State',      name: 'implementation_state', data: 'implementation_state', searchable: false, sortable: true, style: { width: '150px' } }
    ];
    // this.initialVisibleColumns = this.columns.map(c => c.name);
  }

  /* ---------------------------------- Data ---------------------------------- */
  private loadControls(): void {
    this.loading = true;
    this.loader.show();

    /* full-text filter against several fields */
    const filterQuery = this.filterBuilder.buildFilter(
      this.filter,
      [
        { name: 'title' },
        { name: 'chapter' },
        { name: 'reason' }
      ]
    );

    const params: CollectionParameters = {
      page:  this.page,
      limit: this.limit,
      sort:  'public_id',
      order: this.sort.order,
      filter: filterQuery,
    };

    this.soaService.getSoaList()
      .pipe(finalize(() => {
        this.loading = false;
        this.loader.hide();
      }))
      .subscribe({
        next: (resp) => {
          /* backend returns { results, total } */
          this.controls      = resp.results;
          this.totalControls = resp.total;
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  /* ---------------------------------- Events ---------------------------------- */
  public onPageChange(page: number): void {
    this.page = page;
    this.loadControls();
  }

  public onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.page  = 1;
    this.loadControls();
  }

  public onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadControls();
  }

  public onSearchChange(search: string): void {
    this.filter = search;
    this.page   = 1;
    this.loadControls();
  }

  /* ---------------------------------- Export ---------------------------------- */
//   exportCsv():  void { this.exportService.exportCsv ('soa', this.controls); }
//   exportXlsx(): void { this.exportService.exportXlsx('soa', this.controls); }
//   exportPdf():  void { this.exportService.exportPdf ('soa', this.controls); }
}
