import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { ApiServicePrefix, resp, ApiCallService } from 'src/app/services/api-call.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import {
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse,
  APIGetSingleResponse
} from 'src/app/services/models/api-response';
import { ObjectGroup } from '../models/object-group.model';


@Injectable({
  providedIn: 'root'
})
export class ObjectGroupService<T = any> implements ApiServicePrefix {
  public servicePrefix: string = 'object_groups';
  public options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(
    private api: ApiCallService ) {}

  public getObjectGroups(
    params: CollectionParameters = { filter: '', limit: 10, page: 1, sort: 'name', order: 1 }
  ): Observable<APIGetMultiResponse<ObjectGroup>> {
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

    return this.api.callGet<APIGetMultiResponse<ObjectGroup>>(`${this.servicePrefix}/`, options).pipe(
      map((res: HttpResponse<APIGetMultiResponse<ObjectGroup>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  public createObjectGroup(
    data: Partial<ObjectGroup>
  ): Observable<APIInsertSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPost<APIInsertSingleResponse<T>>(`${this.servicePrefix}/`, data, options).pipe(
      map((res: HttpResponse<APIInsertSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  public updateObjectGroup(
    public_id: number,
    data: Partial<ObjectGroup>
  ): Observable<APIUpdateSingleResponse<T>> {
    const options = { ...this.options };
    return this.api.callPut<APIUpdateSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, data, options).pipe(
      map((res: HttpResponse<APIUpdateSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  public deleteObjectGroup(
    public_id: number
  ): Observable<APIDeleteSingleResponse<T>> {
    const options = { ...this.options };
    options.params = new HttpParams();

    return this.api.callDelete<APIDeleteSingleResponse<T>>(`${this.servicePrefix}/${public_id}`, options).pipe(
      map((res: HttpResponse<APIDeleteSingleResponse<T>>) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }

  public getObjectGroupById(
    public_id: number
  ): Observable<APIGetSingleResponse<ObjectGroup>> {
    const options = { ...this.options };
    return this.api.callGet<APIGetSingleResponse<ObjectGroup>>(`${this.servicePrefix}/${public_id}`, options).pipe(
      map((res) => res.body),
      catchError((error) => {
        throw error;
      })
    );
  }
}
