// src/app/toolbox/isms/control-meassures/control-meassures-list.component.ts

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
import { ControlMeassure } from '../../models/control-meassure.model';
import { ControlMeassureService } from '../../services/control-meassure.service';

@Component({
    selector: 'app-control-meassures-list',
    templateUrl: './control-meassures-list.component.html',
    styleUrls: ['./control-meassures-list.component.scss']
})
export class ControlMeassuresListComponent implements OnInit {
    @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;

    public controlMeassures: ControlMeassure[] = [];
    public totalControlMeassures = 0;

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
        private controlMeassureService: ControlMeassureService
    ) { }

    ngOnInit(): void {
        this.setupColumns();
        this.loadControlMeassures();
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
                name: 'control_meassure_type',
                data: 'control_meassure_type',
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
    private loadControlMeassures(): void {
        this.loading = true;
        this.loaderService.show();

        const filterQuery = this.filterBuilderService.buildFilter(
            this.filter,
            [
                { name: 'title' },
                { name: 'control_meassure_type' }
            ]
        );

        const params: CollectionParameters = {
            filter: filterQuery,
            limit: this.limit,
            page: this.page,
            sort: this.sort.name,
            order: this.sort.order
        };

        this.controlMeassureService.getControlMeassures(params)
            .pipe(finalize(() => {
                this.loading = false;
                this.loaderService.hide();
            }))
            .subscribe({
                next: (resp) => {
                    this.controlMeassures = resp.results;
                    this.totalControlMeassures = resp.total;
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
    }

    /**
     * Navigate to add new control/meassure page
     * @returns {void}
     */
    public onAddNew(): void {
        this.router.navigate(['/isms/control-meassures/add']);
    }

    /**
     * Navigate to edit control/meassure page
     * @param item - The control/meassure to edit
     * @returns {void}
     */
    public onEdit(item: ControlMeassure): void {
        this.router.navigate(['/isms/control-meassures/edit'], { state: { controlMeassure: item } });
    }

    /**
     * Delete control/meassure
     * @param item - The control/meassure to delete
     * @returns {void}
     */
    public onDelete(item: ControlMeassure): void {
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
                    this.controlMeassureService.deleteControlMeassure(item.public_id)
                        .pipe(finalize(() => this.loaderService.hide()))
                        .subscribe({
                            next: () => {
                                this.toast.success('Control/Measure deleted successfully.');
                                this.loadControlMeassures();
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
        this.loadControlMeassures();
    }

    public onPageSizeChange(limit: number): void {
        this.limit = limit;
        this.page = 1;
        this.loadControlMeassures();
    }

    public onSortChange(sort: Sort): void {
        this.sort = sort;
        this.loadControlMeassures();
    }

    public onSearchChange(search: string): void {
        this.filter = search;
        this.page = 1;
        this.loadControlMeassures();
    }
}
