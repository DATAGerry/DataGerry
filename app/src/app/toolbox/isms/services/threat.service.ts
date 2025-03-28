import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { ApiServicePrefix, resp, ApiCallService } from 'src/app/services/api-call.service';
import {
  APIGetSingleResponse,
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from 'src/app/services/models/api-response';

import { Threat } from '../models/threat.model';
import { CollectionParameters } from 'src/app/services/models/api-parameter';

@Injectable({
  providedIn: 'root'
})
export class ThreatService<T = any> implements ApiServicePrefix {
  public servicePrefix: string = 'isms/threats';

  // Default HTTP options
  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService) {}

  /**
   * Get list of threats, possibly with pagination, filtering, and sorting
   */
  public getThreats(params: CollectionParameters): Observable<APIGetMultiResponse<Threat>> {
    let httpParams = new HttpParams()
      .set('limit', params.limit)
      .set('page', params.page)
      .set('sort', params.sort)
      .set('order', params.order);

      if (params.filter !== undefined) {
        const filter = JSON.stringify(params.filter);
        httpParams = httpParams.set('filter', filter);
      }

    const options = { ...this.options };
    options.params = httpParams;

    return this.api.callGet<APIGetMultiResponse<Threat>>(`${this.servicePrefix}/`, options).pipe(
      map((res: HttpResponse<APIGetMultiResponse<Threat>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  /**
   * Get a single threat by ID
   */
  public getThreatById(public_id: number): Observable<APIGetSingleResponse<Threat>> {
    return this.api.callGet<APIGetSingleResponse<Threat>>(`${this.servicePrefix}/${public_id}`, this.options)
      .pipe(
        map((res: HttpResponse<APIGetSingleResponse<Threat>>) => res.body),
        catchError((error) => {
          throw error;
        })
      );
  }

  /**
   * Create a new threat
   */
  public createThreat(threat: Threat): Observable<APIInsertSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPost<APIInsertSingleResponse<T>>(`${this.servicePrefix}/`, threat, options)
      .pipe(
        map((res: HttpResponse<APIInsertSingleResponse<T>>) => res.body),
        catchError((error) => {
          throw error;
        })
      );
  }

  /**
   * Update an existing threat
   */
  public updateThreat(public_id: number, data: Threat): Observable<APIUpdateSingleResponse<T>> {
    const options = { ...this.options };
    const payload = { ...data, public_id }; // Include public_id in the payload
    return this.api.callPut<APIUpdateSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, payload, options)
      .pipe(
        map((res: HttpResponse<APIUpdateSingleResponse<T>>) => res.body),
        catchError((error) => {
          throw error;
        })
      );
  }

  /**
   * Delete a threat by ID
   */
  public deleteThreat(public_id: number): Observable<APIDeleteSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callDelete<APIDeleteSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, options)
      .pipe(
        map((res: HttpResponse<APIDeleteSingleResponse<T>>) => res.body),
        catchError((error) => {
          throw error;
        })
      );
  }
}
