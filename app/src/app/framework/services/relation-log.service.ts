import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  ApiCallService,
  ApiServicePrefix,
  httpObserveOptions,
  HttpProtocolHelper,
  resp 
} from '../../services/api-call.service';
import { CollectionParameters } from '../../services/models/api-parameter';
import { APIGetMultiResponse } from '../../services/models/api-response';

/**
 * Minimal interface for a RelationLog item.
 * Adjust fields as per your backend response.
 */
export interface RelationLog {
  public_id: number;
  creation_time?: { $date?: number };
  log_time?: any;
  action?: string;
  author_name?: string;
  changes?: any;
  // add any extra fields your backend returns
}

@Injectable({
  providedIn: 'root'
})
export class RelationLogService<T = RelationLog> implements ApiServicePrefix {
  /**
   * Matches the backend route prefix: e.g. GET /object_relation_logs
   */
  public servicePrefix: string = 'object_relation_logs';

  /**
   * Mirrors the approach in relation.service.ts:
   * - headers
   * - params
   * - observe: resp (which must be a string like 'response')
   */
  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp // must be the same constant as in your relation.service (e.g. 'response')
  };

  constructor(private api: ApiCallService) {}

  /**
   * Loads logs from /object_relation_logs (no ID in path),
   * passing a CollectionParameters object that includes:
   *   filter, limit, sort, order, page.
   * The filter is JSON-stringified and placed in ?filter=...
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

    // e.g. GET /object_relation_logs/?filter=...&limit=10&sort=...
    return this.api.callGet<Array<T>>(`${this.servicePrefix}/`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body; 
      })
    );
  }

  /**
   * If your backend also supports GET /object_relation_logs/:publicID,
   * retrieving logs by a single ID in the path.
   * This is optional; use only if needed by some routes.
   */
  public getLogsByRelation(
    publicID: number,
    params: CollectionParameters
  ): Observable<APIGetMultiResponse<T>> {
    const options = { ...this.options };
    let httpParams: HttpParams = new HttpParams();

    if (params.filter !== undefined) {
      httpParams = httpParams.set('filter', JSON.stringify(params.filter));
    }
    if (params.projection !== undefined) {
      httpParams = httpParams.set('projection', JSON.stringify(params.projection));
    }

    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    options.params = httpParams;

    // GET /object_relation_logs/<publicID>?filter=...
    return this.api.callGet<Array<T>>(`${this.servicePrefix}/${publicID}`, options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => apiResponse.body)
    );
  }

  /**
   * Retrieve a single log by public_id, e.g. /object_relation_logs/<publicID>
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
