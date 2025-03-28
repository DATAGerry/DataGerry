import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { ApiServicePrefix, resp, ApiCallService } from 'src/app/services/api-call.service';

import {
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIDeleteSingleResponse,
  APIUpdateSingleResponse
} from 'src/app/services/models/api-response';
import { ExtendableOption } from 'src/app/framework/models/object-group.model';

@Injectable({
  providedIn: 'root'
})
export class ExtendableOptionService<T = any> implements ApiServicePrefix {

  public servicePrefix: string = 'extendable_options';
  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(
    private api: ApiCallService  ) {}

  /**
   * Get extendable options
   */
  public getExtendableOptionsByType(
    optionType: string
  ): Observable<APIGetMultiResponse<ExtendableOption>> {
    const options = { ...this.options };
    let httpParams = new HttpParams();

    const filterObj = { option_type: optionType };
    const filter = JSON.stringify(filterObj);
    httpParams = httpParams.set('filter', filter);
    options.params = httpParams;

    return this.api.callGet<APIGetMultiResponse<ExtendableOption>>(`${this.servicePrefix}/`, options)
      .pipe(
        map((res: HttpResponse<APIGetMultiResponse<ExtendableOption>>) => res.body),
        catchError((error) => {
          throw error;
        })
      );
  }

  /**
   * Create a new extendable option
   */
  public createExtendableOption(
    value: string,
    optionType: string,
    predefined: boolean
  ): Observable<APIInsertSingleResponse<T>> {
    const options = { ...this.options };
    const payload = { value, option_type: optionType, predefined };

    return this.api.callPost<APIInsertSingleResponse<T>>(
      `${this.servicePrefix}/`,
      payload,
      options
    ).pipe(
      map((res: HttpResponse<APIInsertSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  /**
   * Update an existing extendable option by ID
   */
  public updateExtendableOption(
    public_id: number,
    data: Partial<ExtendableOption>
    ): Observable<APIUpdateSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPut<APIUpdateSingleResponse<T>>(
      `${this.servicePrefix}/${public_id}`,
      data,
      options
    ).pipe(
      map((res: HttpResponse<APIUpdateSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  /**
   * Delete an extendable option by ID
   */
  public deleteExtendableOption(
    public_id: number
  ): Observable<APIDeleteSingleResponse<T>> {
    const options = { ...this.options };
    options.params = new HttpParams();

    return this.api.callDelete<APIDeleteSingleResponse<T>>(
      `${this.servicePrefix}/${public_id}`,
      options
    ).pipe(
      map((res: HttpResponse<APIDeleteSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }
}
