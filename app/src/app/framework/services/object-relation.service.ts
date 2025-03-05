import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { ApiCallService, ApiServicePrefix, resp } from '../../services/api-call.service';
import {
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';

export interface CmdbObjectRelationCreateDto {
  relation_id: number;
  relation_parent_id: number;
  relation_child_id: number;
  author_id: number;
  field_values: Array<{ name: string; value: any }>;
  relation_parent_type_id?: number;
  relation_child_type_id?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ObjectRelationService implements ApiServicePrefix {
  public servicePrefix: string = 'object_relations';
  private options = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    params: {},
    observe: resp
  };

  constructor(private api: ApiCallService) { }

  // Get list of object relations
  public getObjectRelations(
    params: CollectionParameters = {
      filter: undefined,
      limit: 10,
      sort: 'public_id',
      order: 1,
      page: 1
    }
  ): Observable<APIGetMultiResponse<any>> {
    const options = { ...this.options };
    let httpParams = new HttpParams();

    if (params.filter) {
      httpParams = httpParams.set('filter', JSON.stringify(params.filter));
    }
    if (params.projection) {
      httpParams = httpParams.set('projection', JSON.stringify(params.projection));
    }
    httpParams = httpParams
      .set('limit', params.limit.toString())
      .set('sort', params.sort)
      .set('order', params.order.toString())
      .set('page', params.page.toString());

    options.params = httpParams;
    return this.api.callGet<any>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<any>>) => apiResponse.body)
    );
  }

  
  // Get single object relation by ID
  public getObjectRelation(publicID: number): Observable<any> {
    const options = { ...this.options, params: new HttpParams() };
    return this.api.callGet<any>(`${this.servicePrefix}/${publicID}`, options).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<any>>) =>
        apiResponse.body.result
      )
    );
  }


  // Create new object relation
  public postObjectRelation(dto: CmdbObjectRelationCreateDto): Observable<any> {
    const options = { ...this.options };
    return this.api.callPost<any>(this.servicePrefix + '/', dto, options).pipe(
      map((httpResp: HttpResponse<APIInsertSingleResponse<any>>) =>
        httpResp.body.raw
      )
    );
  }

  // Update existing object relation
  public putObjectRelation(
    publicID: number,
    dto: Partial<CmdbObjectRelationCreateDto>
  ): Observable<any> {
    const options = { ...this.options };
    return this.api.callPut<any>(
      `${this.servicePrefix}/${publicID}`,
      dto,
      options
    ).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<any>>) =>
        apiResponse.body.result
      )
    );
  }

  // Delete object relation by ID
  public deleteObjectRelation(publicID: number): Observable<any> {
    const options = { ...this.options };
    return this.api.callDelete<any>(
      `${this.servicePrefix}/${publicID}`,
      options
    ).pipe(
      map((apiResponse: HttpResponse<APIDeleteSingleResponse<any>>) =>
        apiResponse.body.raw
      )
    );
  }
}