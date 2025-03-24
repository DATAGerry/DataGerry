import { Injectable } from '@angular/core';
import { HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { ApiCallService, ApiServicePrefix, resp } from 'src/app/services/api-call.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

import { IsmsConfigValidation } from '../models/isms-config-validation.model';

@Injectable({
  providedIn: 'root'
})
export class ISMSService<T = any> implements ApiServicePrefix {
  public servicePrefix: string = 'isms/config/status';

  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService, private toast: ToastService) { }

  /**
   * Fetch the ISMS settings Validation Status
   */
  public getIsmsValidationStatus(): Observable<IsmsConfigValidation> {
    const options = { ...this.options };
    return this.api.callGet<IsmsConfigValidation>(`${this.servicePrefix}`, options)
      .pipe(
        map((res: HttpResponse<IsmsConfigValidation>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }
}
