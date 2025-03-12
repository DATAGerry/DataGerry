import {
  Component,
  Input,
  OnInit,
  TemplateRef,
  ViewChild
} from '@angular/core';
import { finalize } from 'rxjs/operators';

import { ToastService } from 'src/app/layout/toast/toast.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoaderService } from 'src/app/core/services/loader.service';

import { RiskClass } from '../../../models/risk-class.model';
import { RiskClassService } from '../../../services/risk-class.service';
import { IsmsConfig } from '../../../models/isms-config.model';
import { CoreDeleteConfirmationModalComponent } from 'src/app/core/components/dialog/delete-dialog/core-delete-confirmation-modal.component';
import { RiskClassModalComponent } from './modal/add-risk-class-modal.component';

@Component({
  selector: 'app-isms-risk-classes',
  templateUrl: './risk-classes.component.html',
  styleUrls: ['./risk-classes.component.scss']
})
export class RiskClassesComponent implements OnInit {
  public riskClasses: RiskClass[] = [];
  public totalRiskClasses: number = 0;
  public page = 1;
  public limit = 10;
  public loading = false;

  // Table column templates
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;
  @ViewChild('colorTemplate', { static: true }) colorTemplate: TemplateRef<any>;

  //  pass a config from the wizard container
  @Input() config: IsmsConfig;

  public columns: Array<any>;

  constructor(
    private riskClassService: RiskClassService,
    private toast: ToastService,
    private modalService: NgbModal,
    private loaderService: LoaderService
  ) { }


  ngOnInit(): void {


    this.columns = [
      {
        display: 'Public ID',
        name: 'publicId',
        data: 'public_id',
        searchable: false,
        sortable: false,
        style: { width: '90px', 'text-align': 'center' }
      },
      {
        display: 'Color',
        name: 'color',
        data: 'color',
        template: this.colorTemplate,
        sortable: false,
        style: { width: '120px', 'text-align': 'center' }
      },
      {
        display: 'Label',
        name: 'label',
        data: 'name',
        sortable: false,
        style: { 'text-align': 'center' }
      },
      {
        display: 'Description',
        name: 'description',
        data: 'description',
        sortable: false,
        style: { width: 'auto', 'text-align': 'center' }
      },
      {
        display: 'Actions',
        name: 'actions',
        template: this.actionsTemplate,
        sortable: false,
        style: { width: '100px', 'text-align': 'center' }
      }
    ];

    this.loadRiskClasses();
  }


  /**
   * Loads Risk Classes from the server with pagination.
   */
  private loadRiskClasses(): void {
    this.loading = true;
    this.loaderService.show();

    this.riskClassService
      .getRiskClasses({
        filter: '',
        limit: this.limit,
        page: this.page,
        sort: '',
        order: 1
      })
      .pipe(
        finalize(() => {
          this.loaderService.hide();
          this.loading = false;
        })
      )
      .subscribe({
        next: (data) => {
          this.riskClasses = data.results;
          this.totalRiskClasses = data.total;
        },
        error: (err) => {
          this.riskClasses = [];
          this.totalRiskClasses = 0;
          this.toast.error(err?.error?.message);
        }
      });
  }

  /**
   * Opens modal to ADD a new Risk Class.
   */
  public addRiskClass(): void {

    const modalRef = this.modalService.open(RiskClassModalComponent, { size: 'lg' });
    // No input => the modal knows it's creating a new record
    modalRef.result.then(
      (result) => {
        if (result === 'saved') {
          this.loadRiskClasses();
        }
      },
      () => {
        // Modal dismissed
      }
    );
  }


  /**
   * Opens modal to EDIT an existing Risk Class.
   */
  public editRiskClass(item: RiskClass): void {
    console.log('edir riskClass', item)
    const modalRef = this.modalService.open(RiskClassModalComponent, { size: 'lg' });
    // Pass existing item => the modal is in edit mode
    modalRef.componentInstance.riskClass = { ...item };
    modalRef.result.then(
      (result) => {
        console.log('edit result', result)
        if (result === 'saved') {
          this.loadRiskClasses();
        }
      },
      () => {
        // Modal dismissed
      }
    );
  }


  /**
   * Deletes a Risk Class after user confirms in CoreDeleteConfirmationModalComponent.
   */
  public onDeleteRiskClass(item: RiskClass): void {
    console.log('item', item)
    const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
    modalRef.componentInstance.title = 'Delete Risk Class';
    modalRef.componentInstance.item = item;
    modalRef.componentInstance.itemType = 'Risk Class';
    modalRef.componentInstance.itemName = item.name;

    modalRef.result.then(
      (result) => {
        if (result === 'confirmed') {
          this.loaderService.show();
          this.riskClassService
            .deleteRiskClass(item?.public_id!)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
              next: () => {
                this.toast.success('Risk Class deleted successfully.');
                this.loadRiskClasses();
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


  /**
   * Handle table pagination page change.
   */
  public onPageChange(newPage: number): void {
    this.page = newPage;
    this.loadRiskClasses();
  }


  /**
   * Handle table page size (limit) change.
   */
  public onPageSizeChange(newLimit: number): void {
    this.limit = newLimit;
    this.page = 1;
    this.loadRiskClasses();
  }


  /**
    * handle row reordering
    */
  public onOrderChange(newItems: RiskClass[]): void {
    this.riskClasses = newItems;
  }
}
