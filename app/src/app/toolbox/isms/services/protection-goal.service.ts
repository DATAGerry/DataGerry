import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ApiServicePrefix, resp, ApiCallService } from 'src/app/services/api-call.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import {
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from 'src/app/services/models/api-response';
import { ProtectionGoal } from '../models/protection-goal.model';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Injectable({
  providedIn: 'root'
})
export class ProtectionGoalService<T = any> implements ApiServicePrefix {
  public servicePrefix: string = 'isms/protection_goals';

  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService, private toast: ToastService) { }


  /**
   * Get all protection goals with filters, pagination, and sorting.
   */
  public getProtectionGoals(params: CollectionParameters = {
    filter: '',
    limit: 10,
    sort: 'name',
    order: 1,
    page: 1
  }): Observable<APIGetMultiResponse<ProtectionGoal>> {
    const options = { ...this.options };
    let httpParams = new HttpParams();
    if (params.filter !== undefined) {
      const filter = JSON.stringify(params.filter);
      httpParams = httpParams.set('filter', filter);
    }
    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    options.params = httpParams;
    return this.api.callGet<APIGetMultiResponse<ProtectionGoal>>(`${this.servicePrefix}/`, options)
      .pipe(
        map((res: HttpResponse<APIGetMultiResponse<ProtectionGoal>>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }


  /**
   * Create a new protection goal.
   */
  public createProtectionGoal(data: Partial<ProtectionGoal>): Observable<APIInsertSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPost<APIInsertSingleResponse<T>>(`${this.servicePrefix}/`, data, options)
      .pipe(
        map((res: HttpResponse<APIInsertSingleResponse<T>>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }


  /**
   * Update protection goal by ID.
   */
  public updateProtectionGoal(public_id: number, data: Partial<ProtectionGoal>): Observable<APIUpdateSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPut<APIUpdateSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, data, options)
      .pipe(
        map((res: HttpResponse<APIUpdateSingleResponse<T>>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }

  /**
   * Delete protection goal by ID.
   */
  public deleteProtectionGoal(public_id: number): Observable<APIDeleteSingleResponse<T>> {
    const options = { ...this.options };
    options.params = new HttpParams();
    return this.api.callDelete<APIDeleteSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, options)
      .pipe(
        map((res: HttpResponse<APIDeleteSingleResponse<T>>) => res.body),
        catchError((error) => {
          this.toast.error(error?.error?.message);
          throw error;
        })
      );
  }
}
