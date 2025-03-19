import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { ApiCallService, ApiServicePrefix, resp } from 'src/app/services/api-call.service';
import { IsmsRiskMatrix } from '../models/risk-matrix.model';
import { ToastService } from 'src/app/layout/toast/toast.service';
import {
  APIUpdateSingleResponse
} from 'src/app/services/models/api-response';

@Injectable({
  providedIn: 'root'
})
export class RiskMatrixService<T = any> implements ApiServicePrefix {
  public servicePrefix: string = 'isms/risk_matrix';

  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService, private toast: ToastService) { }

  /**
   * Fetch the single RiskMatrix record (we assume only one).
   */
  public getRiskMatrix(publicId: number): Observable<IsmsRiskMatrix> {
    const options = { ...this.options };
    return this.api.callGet<IsmsRiskMatrix>(`${this.servicePrefix}/${publicId}`, options)
      .pipe(
        map((res: HttpResponse<IsmsRiskMatrix>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }


  /**
   * Update the single RiskMatrix record.
   */
  public updateRiskMatrix(data: IsmsRiskMatrix): Observable<APIUpdateSingleResponse<T>> {
    const options = { ...this.options };
    // If there's a known public_id, use it; otherwise assume "1"
    const matrixId = data.public_id || 1;
    return this.api.callPut<APIUpdateSingleResponse<T>>(`${this.servicePrefix}/${matrixId}`, data, options)
      .pipe(
        map((res: HttpResponse<APIUpdateSingleResponse<T>>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }
}
