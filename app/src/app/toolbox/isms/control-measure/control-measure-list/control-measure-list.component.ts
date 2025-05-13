// src/app/toolbox/isms/control-measures/control-measures-list.component.ts

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


import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';
import { ControlMeasure } from '../../models/control-measure.model';
import { ControlMeasureService } from '../../services/control-measure.service';
@Component({
    selector: 'app-control-measures-list',
    templateUrl: './control-measures-list.component.html',
    styleUrls: ['./control-measures-list.component.scss']
})
export class ControlmeasuresListComponent implements OnInit {
    @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

    public controlMeasures: ControlMeasure[] = [];
    public totalControlMeasures = 0;

    // Table config
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
        private controlmeasureservice: ControlMeasureService
    ) { }

    ngOnInit(): void {
        this.setupColumns();
        this.loadControlMeasures();
    }

    /**
     * Define columns for cmdb-table
     */
    private setupColumns(): void {
        this.columns = [
            {
                display: 'ID',
                name: 'public_id',
                data: 'public_id',
                searchable: false,
                sortable: true,
                style: { width: '80px', 'text-align': 'center' }
            },
            {
                display: 'Title',
                name: 'title',
                data: 'title',
                searchable: true,
                sortable: true,
                style: { width: '200px' }
            },
            {
                display: 'Type',
                name: 'control_measure_type',
                data: 'control_measure_type',
                searchable: true,
                sortable: true,
                style: { width: '150px', 'text-align': 'center' }
            },
            {
                display: 'Source',
                name: 'source',
                data: 'source',
                searchable: false,
                sortable: false,
                style: { width: '100px', 'text-align': 'center' }
            },
            {
                display: 'Actions',
                name: 'actions',
                data: 'public_id',
                searchable: false,
                sortable: false,
                fixed: true,
                template: this.actionTemplate,
                style: { width: '100px', 'text-align': 'center' }
            }
        ];
        this.initialVisibleColumns = this.columns.map((c) => c.name);
    }

    /**
     * Load data from backend
     */
    private loadControlMeasures(): void {
        this.loading = true;
        this.loaderService.show();

        const filterQuery = this.filterBuilderService.buildFilter(
            this.filter,
            [
                { name: 'title' },
                { name: 'control_measure_type' }
            ]
        );

        const params: CollectionParameters = {
            filter: filterQuery,
            limit: this.limit,
            page: this.page,
            sort: this.sort.name,
            order: this.sort.order
        };

        this.controlmeasureservice.getControlMeasures(params)
            .pipe(finalize(() => {
                this.loading = false;
                this.loaderService.hide();
            }))
            .subscribe({
                next: (resp) => {
                    this.controlMeasures = resp.results;
                    this.totalControlMeasures = resp.total;
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
    }


    /**
     * Navigate to add new control/measure page
     * @returns {void}
     */
    public onAddNew(): void {
        this.router.navigate(['/isms/control-measures/add']);
    }

    /**
     * Navigate to view control/measure page
     * @param item - The control/measure to view
     * @returns {void}
     */
    public onView(item: ControlMeasure): void {
        this.router.navigate(['/isms/control-measures/view'], { state: { controlMeasure: item, mode: 'view' } });
    }


    /**
     * Navigate to edit control/measure page
     * @param item - The control/measure to edit
     * @returns {void}
     */
    public onEdit(item: ControlMeasure): void {
        this.router.navigate(['/isms/control-measures/edit'], { state: { controlMeasure: item } });
    }


    /**
     * Delete control/measure
     * @param item - The control/measure to delete
     * @returns {void}
     */
    public onDelete(item: ControlMeasure): void {
        if (!item.public_id) {
            return;
        }
        const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
        modalRef.componentInstance.title = 'Delete Control/Measure';
        modalRef.componentInstance.item = item;
        modalRef.componentInstance.itemType = 'Control/Measure';
        modalRef.componentInstance.itemName = item.title;

        modalRef.result.then(
            (result) => {
                if (result === 'confirmed') {
                    this.loaderService.show();
                    this.controlmeasureservice.deleteControlMeasure(item.public_id)
                        .pipe(finalize(() => this.loaderService.hide()))
                        .subscribe({
                            next: () => {
                                this.toast.success('Control/Measure deleted successfully.');
                                this.loadControlMeasures();
                            },
                            error: (err) => {
                                this.toast.error(err?.error?.message);
                            }
                        });
                }
            },
            () => { /* dismissed */ }
        );
    }


    /* ------------------------------------------------------------------
    * Pagination, sorting, and search functionality
    * ------------------------------------------------------------------ */
    public onPageChange(page: number): void {
        this.page = page;
        this.loadControlMeasures();
    }

    public onPageSizeChange(limit: number): void {
        this.limit = limit;
        this.page = 1;
        this.loadControlMeasures();
    }

    public onSortChange(sort: Sort): void {
        this.sort = sort;
        this.loadControlMeasures();
    }

    public onSearchChange(search: string): void {
        this.filter = search;
        this.page = 1;
        this.loadControlMeasures();
    }
}
