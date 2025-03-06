import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  ApiCallService,
  ApiServicePrefix,
  resp 
} from '../../services/api-call.service';
import { CollectionParameters } from '../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../services/models/api-response';


export interface RelationLog {
  public_id: number;
  creation_time?: { $date?: number };
  log_time?: any;
  action?: string;
  author_name?: string;
  changes?: any;
}

@Injectable({
  providedIn: 'root'
})
export class RelationLogService<T = RelationLog> implements ApiServicePrefix {

  public servicePrefix: string = 'object_relation_logs';

  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp 
  };

  constructor(private api: ApiCallService) {}

  /**
   * Retreiving all of the object relation logs
   */
  public getLogsAll(
    params: CollectionParameters = { filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1 }
  ): Observable<APIGetMultiResponse<T>> {
    const options = { ...this.options };
    let httpParams: HttpParams = new HttpParams();

    // If there's a filter, convert it to JSON and set in query param
    if (params.filter !== undefined) {
      const filterStr = JSON.stringify(params.filter);
      httpParams = httpParams.set('filter', filterStr);
    }

    // If there's a projection, similarly set it
    if (params.projection !== undefined) {
      const projStr = JSON.stringify(params.projection);
      httpParams = httpParams.set('projection', projStr);
    }

    // Limit, sort, order, page
    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());

    options.params = httpParams;

    return this.api.callGet<Array<T>>(`${this.servicePrefix}/`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body; 
      })
    );
  }

  /**
   * Retrieve a single log by public_id
   */
  public getLog(publicID: number): Observable<T> {
    const options = { ...this.options };
    options.params = {};
    return this.api.callGet<T>(`${this.servicePrefix}/${publicID}`, options).pipe(
      map(apiResponse => apiResponse.body)
    );
  }

  /**
   * Delete a single log
   */
  public deleteLog(publicID: number): Observable<any> {
    const options = { ...this.options };
    options.params = {};
    return this.api.callDelete<any>(`${this.servicePrefix}/${publicID}`, options).pipe(
      map(apiResponse => apiResponse.body)
    );
  }
}
