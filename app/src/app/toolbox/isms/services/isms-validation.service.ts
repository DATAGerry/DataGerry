import { Injectable } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { ISMSService } from './isms.service';
import { CoreWarningModalComponent } from 'src/app/core/components/dialog/core-warning-modal/core-warning-modal.component';
import { IsmsConfigValidation } from '../models/isms-config-validation.model';
import { Observable, of } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { Location } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class IsmsValidationService {
  constructor(
    private ismsService: ISMSService,
    private modalService: NgbModal,
    private router: Router,
    private location: Location
  ) {}

  /**
   * Returns true if config is valid, otherwise opens a modal and navigates
   */
  checkAndHandleInvalidConfig(): Observable<boolean> {
    return this.ismsService.getIsmsValidationStatus().pipe(
      switchMap((status: IsmsConfigValidation) => {
        const isValid =
          status.risk_classes &&
          status.likelihoods &&
          status.impacts &&
          status.impact_categories &&
          status.risk_matrix;

        if (isValid) {
          return of(true);
        }

        const modalRef = this.modalService.open(CoreWarningModalComponent, { centered: true });
        modalRef.componentInstance.title = 'ISMS Configuration Required';
        modalRef.componentInstance.message = 'Your ISMS configuration is incomplete. Please configure your settings before continuing.';
        modalRef.componentInstance.confirmLabel = 'Go to ISMS Settings';
        modalRef.componentInstance.cancelLabel = 'Cancel';
        modalRef.componentInstance.route = '/isms/configure';

        // Listen to modal result
        return modalRef.result.then(
          () => false, // when confirmed
          () => {
            this.location.back(); // go back on cancel
            return false;
          }
        );
      })
    );
  }
  
}
