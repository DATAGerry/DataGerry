import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'core-delete-confirmation-modal',
  templateUrl: './core-delete-confirmation-modal.component.html'
})
export class CoreDeleteConfirmationModalComponent {
  @Input() title: string;
  @Input() item: any;
  @Input() itemType: string;
  @Input() itemName: string;
  @Input() description: string;

  constructor(public activeModal: NgbActiveModal) { }

  confirmDelete(): void {
    this.activeModal.close('confirmed');
  }
}