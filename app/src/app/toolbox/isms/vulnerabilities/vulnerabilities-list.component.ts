/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2025 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { FilterBuilderService } from 'src/app/core/services/filter-builder.service';
import { CoreDeleteConfirmationModalComponent } from 'src/app/core/components/dialog/delete-dialog/core-delete-confirmation-modal.component';



import { Column, Sort, SortDirection } from 'src/app/layout/table/table.types';
import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { OptionType } from 'src/app/toolbox/isms/models/option-type.enum';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';
import { Vulnerability } from '../models/vulnerability.model';
import { VulnerabilityService } from '../services/vulnerability.service';

@Component({
    selector: 'app-vulnerabilities-list',
    templateUrl: './vulnerabilities-list.component.html',
    styleUrls: ['./vulnerabilities-list.component.scss']
})
export class VulnerabilitiesListComponent implements OnInit {

    @ViewChild('actionTemplate', { static: true }) actionTemplate: TemplateRef<any>;
    @ViewChild('sourceTemplate', { static: true }) sourceTemplate: TemplateRef<any>;

    public threats: Vulnerability[] = [];
    public totalThreats = 0;
    public page = 1;
    public limit = 10;
    public loading = false;
    public filter = '';
    public sort: Sort = { name: 'public_id', order: SortDirection.DESCENDING };

    // Table columns
    public columns: Column[] = [];
    public initialVisibleColumns: string[] = [];

    // For showing source names
    public sourceOptions: ExtendableOption[] = [];

    /* --------------------------------------------------- LIFECYCLE MEHTODS --------------------------------------------------- */

    constructor(
        private router: Router,
        private toast: ToastService,
        private loaderService: LoaderService,
        private vulnerabilityService: VulnerabilityService,
        private modalService: NgbModal,
        private filterBuilderService: FilterBuilderService,
        private extendableOptionService: ExtendableOptionService
    ) { }

    ngOnInit(): void {
        this.setupColumns();
        this.loadSourceOptions();
        this.loadThreats();
    }

    /* --------------------------------------------------- INIT --------------------------------------------------- */

    /* 
    * Define table columns and templates
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
                style: { width: 'auto'},
                cssClasses: ['text-center'],
            },
            {
                display: 'Identifier',
                name: 'identifier',
                data: 'identifier',
                searchable: true,
                sortable: true,
                style: { width: '180px', 'text-align': 'center' }
            },
            {
                display: 'Source',
                name: 'source',
                data: 'source',
                searchable: true,
                sortable: false,
                template: this.sourceTemplate,
                style: { width: 'auto'},
                cssClasses: ['text-center'],
            },
            {
                display: 'Actions',
                name: 'actions',
                data: 'public_id',
                searchable: false,
                sortable: false,
                fixed: true,
                template: this.actionTemplate,
                style: { width: '80px', 'text-align': 'center' }
            }
        ];
        this.initialVisibleColumns = this.columns.map(c => c.name);
    }


    /* --------------------------------------------------- API CALLS --------------------------------------------------- */

    /*
    * Load the source options
    */
    loadSourceOptions(): void {
        this.loaderService.show();
        this.extendableOptionService.getExtendableOptionsByType(OptionType.THREAT_VULNERABILITY)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
                next: (res) => {
                    this.sourceOptions = res.results;
                },
                error: (err) => this.toast.error(err?.error?.message)
            });
    }

    /*
    * Load the threats from the backend
    */
    loadThreats(): void {
        this.loading = true;
        this.loaderService.show();

        const filterQuery = this.filterBuilderService.buildFilter(
            this.filter,
            [{ name: 'public_id' }, { name: 'name' }, { name: 'identifier' }]
        );

        const params: CollectionParameters = {
            filter: filterQuery,
            limit: this.limit,
            page: this.page,
            sort: this.sort.name,
            order: this.sort.order
        };

        this.vulnerabilityService.getVulnerabilities(params)
            .pipe(finalize(() => {
                this.loading = false;
                this.loaderService.hide();
            }))
            .subscribe({
                next: (resp) => {
                    this.threats = resp.results;
                    this.totalThreats = resp.total;
                },
                error: (err) => {
                    this.toast.error(err?.error?.message);
                }
            });
    }

    /* --------------------------------------------------- ACTIONS--------------------------------------------------- */

    /*
    * Add a new Vulnerability
    */
    onAddNew(): void {
        this.router.navigate(['/isms/vulnerabilities/add']);
    }

    /*
    * Edit a vulnerability
    */

    public onEdit(vulnerability: Vulnerability): void {
        // Directly pass the entire object in router state
        this.router.navigate(
            ['/isms/vulnerabilities/edit'],
            { state: { vulnerability } }
        );
    }


    /*
    * View a vulnerability
    */
    public onView(vulnerability: Vulnerability): void {
        this.router.navigate(
          ['/isms/vulnerabilities/view'],
          { state: { vulnerability } }
        );
      }
      


    /*
    * Delete a vulnerability
    */
    onDelete(vulnerability: Vulnerability): void {
        const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
        modalRef.componentInstance.title = 'Delete Vulnerability';
        modalRef.componentInstance.item = vulnerability;
        modalRef.componentInstance.itemType = 'Vulnerability';
        modalRef.componentInstance.itemName = vulnerability.name;

        modalRef.result.then(
            (result) => {
                if (result === 'confirmed' && vulnerability.public_id) {
                    this.loaderService.show();
                    this.vulnerabilityService.deleteVulnerability(vulnerability.public_id)
                        .pipe(finalize(() => this.loaderService.hide()))
                        .subscribe({
                            next: () => {
                                this.toast.success('Vulnerability deleted successfully.');
                                this.loadThreats();
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


    /* --------------------------------------------------- Pagination, sorting, and search handlers --------------------------------------------------- */


    onPageChange(page: number): void {
        this.page = page;
        this.loadThreats();
    }

    onPageSizeChange(limit: number): void {
        this.limit = limit;
        this.page = 1;
        this.loadThreats();
    }

    onSortChange(sort: Sort): void {
        this.sort = sort;
        this.loadThreats();
    }

    onSearchChange(search: string): void {
        this.filter = search;
        this.page = 1;
        this.loadThreats();
    }

    /*
  * Get the source name by its public_id
  */
    getSourceNames(sourceIds: number): string {
        const option = this.sourceOptions.find(opt => opt.public_id === sourceIds);
        return option?.value;
    }
}
