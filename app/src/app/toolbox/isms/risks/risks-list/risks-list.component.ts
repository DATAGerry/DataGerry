import {
  Component,
  OnInit,
  TemplateRef,
  ViewChild
} from '@angular/core';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { finalize } from 'rxjs/operators';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { FilterBuilderService } from 'src/app/core/services/filter-builder.service';
import { CoreDeleteConfirmationModalComponent } from 'src/app/core/components/dialog/delete-dialog/core-delete-confirmation-modal.component';

import { Risk } from 'src/app/toolbox/isms/models/risk.model';
import { RiskService } from 'src/app/toolbox/isms/services/risk.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';

@Component({
  selector: 'app-risks-list',
  templateUrl: './risks-list.component.html',
  styleUrls: ['./risks-list.component.scss']
})
export class RisksListComponent implements OnInit {
  // Template references for the cmdb-table
  @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;
  @ViewChild('riskTypeTemplate', { static: true }) riskTypeTemplate: TemplateRef<any>;

  // Data
  public risks: Risk[] = [];
  public totalRisks = 0;

  // Table options
  public page = 1;
  public limit = 10;
  public loading = false;
  public filter = '';
  public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING };
  public columns: Column[] = [];
  public initialVisibleColumns: string[] = [];

  constructor(
    private router: Router,
    private toast: ToastService,
    private loaderService: LoaderService,
    private modalService: NgbModal,
    private filterBuilderService: FilterBuilderService,
    private riskService: RiskService
  ) { }

  ngOnInit(): void {
    this.setupColumns();
    this.loadRisks();
  }

  /**
   * Define our table columns
   */
  setupColumns(): void {
    this.columns = [
      {
        display: 'Public ID',
        name: 'public_id',
        data: 'public_id',
        searchable: false,
        sortable: true,
        style: { width: '120px', 'text-align': 'center' }
      },
      {
        display: 'Name',
        name: 'name',
        data: 'name',
        searchable: true,
        sortable: true,
        style: { width: 'auto', 'text-align': 'center' }
      },
      {
        display: 'Identifier',
        name: 'identifier',
        data: 'identifier',
        searchable: true,
        sortable: true,
        style: { width: '150px', 'text-align': 'center' }
      },
      {
        display: 'Risk Type',
        name: 'risk_type',
        data: 'risk_type',
        searchable: true,
        sortable: true,
        template: this.riskTypeTemplate,
        style: { width: '150px', 'text-align': 'center' }
      },
      {
        display: 'Actions',
        name: 'actions',
        data: 'public_id',
        searchable: false,
        sortable: false,
        fixed: true,
        template: this.actionTemplate,
        style: { width: '120px', 'text-align': 'center' }
      }
    ];
    this.initialVisibleColumns = this.columns.map((c) => c.name);
  }


  /**
   * Load the data from backend
   */
  loadRisks(): void {
    this.loading = true;
    this.loaderService.show();

    const filterQuery = this.filterBuilderService.buildFilter(
      this.filter,
      [{ name: 'public_id' }, { name: 'name' }, { name: 'identifier' }, { name: 'risk_type' }]
    );

    const params: CollectionParameters = {
      filter: filterQuery,
      limit: this.limit,
      page: this.page,
      sort: this.sort.name,
      order: this.sort.order
    };

    this.riskService.getRisks(params)
      .pipe(finalize(() => {
        this.loading = false;
        this.loaderService.hide();
      }))
      .subscribe({
        next: (resp) => {
          this.risks = resp.results;
          this.totalRisks = resp.total;
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }


  /**
   * Create a new Risk
   */
  onAddNew(): void {
    this.router.navigate(['/isms/risks/add']);
  }


  /**
   * Edit Risk
   */
  onEdit(risk: Risk): void {
    this.router.navigate(
      ['/isms/risks/edit'],
      { state: { risk } }
    );
  }


  /**
   * Delete Risk (show confirmation modal)
   */
  onDelete(risk: Risk): void {
    if (!risk.public_id) {
      return;
    }
    const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
    modalRef.componentInstance.title = 'Delete Risk';
    modalRef.componentInstance.item = risk;
    modalRef.componentInstance.itemType = 'Risk';
    modalRef.componentInstance.itemName = risk.name;

    modalRef.result.then(
      (result) => {
        if (result === 'confirmed') {
          this.loaderService.show();
          this.riskService.deleteRisk(risk.public_id)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
              next: () => {
                this.toast.success('Risk deleted successfully.');
                this.loadRisks();
              },
              error: (err) => {
                this.toast.error(err?.error?.message);
              }
            });
        }
      },
      () => { }
    );
  }


  /* ------------------------------------------------------------
   * Pagination, sorting, search handlers
   * ------------------------------------------------------------
   */

  onPageChange(page: number): void {
    this.page = page;
    this.loadRisks();
  }

  onPageSizeChange(limit: number): void {
    this.limit = limit;
    this.page = 1;
    this.loadRisks();
  }

  onSortChange(sort: Sort): void {
    this.sort = sort;
    this.loadRisks();
  }

  onSearchChange(search: string): void {
    this.filter = search;
    this.page = 1;
    this.loadRisks();
  }
}
