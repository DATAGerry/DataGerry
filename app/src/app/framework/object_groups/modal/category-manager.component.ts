import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { finalize } from 'rxjs/operators';

import { ExtendableOptionService } from 'src/app/toolbox/isms/services/extendable-option.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { ExtendableOption } from '../../models/object-group.model';
import { OptionType } from 'src/app/toolbox/isms/models/option-type.enum';
import { CoreDeleteConfirmationModalComponent } from 'src/app/core/components/dialog/delete-dialog/core-delete-confirmation-modal.component';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-category-manager',
  templateUrl: './category-manager.component.html',
  styleUrls: ['./category-manager.component.scss']
})
export class CategoryManagerComponent implements OnInit {
  /** The current category list passed in from the parent */
  @Input() categoryOptions: ExtendableOption[] = [];

  /** Fires when user closes the manager */
  @Output() close = new EventEmitter<void>();

  // Internal copy for local edits
  public localCategoryOptions: ExtendableOption[] = [];
  public newCategoryName = '';
  public editingCategoryId?: number;
  public editingCategoryValue = '';

  constructor(
    private extendableOptionService: ExtendableOptionService,
    private toast: ToastService,
    private loaderService: LoaderService,
    private modalService: NgbModal
  ) { }

  ngOnInit(): void {
    // Make a local copy of the passed categories so user can edit them
    this.localCategoryOptions = JSON.parse(JSON.stringify(this.categoryOptions));
  }

  /** 
   * Close (emit event so parent can do any refreshes if needed) 
   */
  public closeCategoryManager(): void {
    this.close.emit();
  }

  /** Create a new category and add it to the local list */
  public onAddNewCategory(): void {
    const val = this.newCategoryName.trim();
    if (!val) { return; }

    this.loaderService.show();
    this.extendableOptionService.createExtendableOption(val, OptionType.OBJECT_GROUP)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (res) => {
          const created = (res as any).result || (res as any).raw;
          if (created?.public_id) {
            this.localCategoryOptions.push(created);
            this.toast.success(`Category "${val}" created`);
            this.newCategoryName = '';
          }
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  /** Begin editing an existing category */
  public onEditCategory(cat: ExtendableOption): void {
    this.editingCategoryId = cat.public_id;
    this.editingCategoryValue = cat.value;
  }

  /** Cancel inline editing of category */
  public cancelEditCategory(): void {
    this.editingCategoryId = undefined;
    this.editingCategoryValue = '';
  }

  /** Save changes to an existing category */
  public saveEditCategory(cat: ExtendableOption): void {
    const newVal = (this.editingCategoryValue || '').trim();
    if (!newVal) {
      this.toast.warning('Name cannot be empty');
      return;
    }

    this.loaderService.show();
    const payload = {
      public_id: cat.public_id,
      value: newVal,
      option_type: cat.option_type
    };
    this.extendableOptionService.updateExtendableOption(cat.public_id, payload)
      .pipe(finalize(() => this.loaderService.hide()))
      .subscribe({
        next: (resp: any) => {
          const updated = resp.result || resp.raw;
          if (updated?.public_id) {
            const idx = this.localCategoryOptions.findIndex(x => x.public_id === cat.public_id);
            if (idx >= 0) {
              this.localCategoryOptions[idx].value = newVal;
            }
            this.toast.success('Category updated');
            this.editingCategoryId = undefined;
            this.editingCategoryValue = '';
          }
        },
        error: (err: any) => {
          this.toast.error(err?.error?.message);
        }
      });
  }

  /** Delete a category */
  public onDeleteCategory(item: ExtendableOption): void {
    if (!item.public_id) { return; }

    const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
    modalRef.componentInstance.title = 'Delete Category';
    modalRef.componentInstance.item = item;
    modalRef.componentInstance.itemType = 'Category';
    modalRef.componentInstance.itemName = item.value;

    modalRef.result.then(
        (result) => {
          if (result === 'confirmed') {
            this.loaderService.show();
            this.extendableOptionService.deleteExtendableOption(item.public_id)
            .pipe(finalize(() => this.loaderService.hide()))
            .subscribe({
              next: () => {
                this.localCategoryOptions = this.localCategoryOptions.filter(c => c.public_id !== item.public_id);
                this.toast.success('Category deleted');
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
}
