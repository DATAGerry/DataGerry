// framework/relation/services/relation.service.ts
import { Injectable } from '@angular/core';
import { UntypedFormControl } from '@angular/forms';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';

import { Observable, timer, catchError, map, switchMap } from 'rxjs';

import {
  ApiCallService,
  ApiServicePrefix,
  HttpProtocolHelper,
  resp
} from '../../services/api-call.service';
import { ValidatorService } from '../../services/validator.service';
import { UserService } from '../../management/services/user.service';
import { SidebarService } from 'src/app/layout/services/sidebar.service';

import {
  APIDeleteSingleResponse,
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse
} from '../../services/models/api-response';
import { CollectionParameters } from '../../services/models/api-parameter';
import { CmdbRelation } from '../models/relation.model';

/* ------------------------------------------------------------------------------------------------------------------ */

/**
 * RelationService is analogous to your TypeService, just changes the prefix
 * to 'relations' and references 'CmdbRelation' instead of 'CmdbType'.
 */
@Injectable({
  providedIn: 'root'
})
export class RelationService<T = CmdbRelation> implements ApiServicePrefix {

  public servicePrefix: string = 'relations';

  public options = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    }),
    params: {},
    observe: resp
  };

  constructor(
    private api: ApiCallService,
    private sideBarService: SidebarService
  ) {}



  /**
   * Get list of relations
   * @param params
   * @param active optionally filter by active?
   */
  public getRelations(
    params: CollectionParameters = { filter: undefined, limit: 10, sort: 'public_id', order: 1, page: 1 },
    // active: boolean = false
  ): Observable<APIGetMultiResponse<T>> {
    const options = this.options;
    let httpParams: HttpParams = new HttpParams();

    if (params.filter !== undefined) {
      const filter = JSON.stringify(params.filter);
      httpParams = httpParams.set('filter', filter);
    }

    if (params.projection !== undefined) {
      const projection = JSON.stringify(params.projection);
      httpParams = httpParams.set('projection', projection);
    }

    httpParams = httpParams.set('limit', params.limit.toString());
    httpParams = httpParams.set('sort', params.sort);
    httpParams = httpParams.set('order', params.order.toString());
    httpParams = httpParams.set('page', params.page.toString());
    // httpParams = httpParams.set('active', JSON.stringify(active));
    options.params = httpParams;

    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        return apiResponse.body;
      })
    );
  }

  /**
   * Get a single relation by public ID
   */
  public getRelation(publicID: number): Observable<T> {
    const options = this.options;
    options.params = new HttpParams();

    return this.api.callGet<T>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse: HttpResponse<APIGetSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }



  /**
   * Finds a single relation by name
   */
  public getRelationByName(name: string): Observable<T> {
    const options = this.options;
    const filter = { name };
    let params: HttpParams = new HttpParams();
    params = params.set('filter', JSON.stringify(filter));
    options.params = params;

    return this.api.callGet<Array<T>>(this.servicePrefix + '/', options).pipe(
      map((apiResponse: HttpResponse<APIGetMultiResponse<T>>) => {
        if (apiResponse.body.count === 0) {
          return null;
        }
        return apiResponse.body.results[0] as T;
      })
    );
  }

  /**
   * Insert/create a new relation
   */
  public postRelation(relation: T): Observable<T> {
    const options = this.options;
    options.params = new HttpParams();

    return this.api.callPost<T>(this.servicePrefix + '/', relation, options).pipe(
      map((apiResponse: HttpResponse<APIInsertSingleResponse<T>>) => {
        return apiResponse.body.raw as T;
      })
    );
  }

  /**
   * Update an existing relation
   */
  public putRelation(relation: T & { public_id: number }): Observable<T> {
    const options = this.options;
    options.params = new HttpParams();

    return this.api.callPut<T>(this.servicePrefix + '/' + relation.public_id, relation, options).pipe(
      map((apiResponse: HttpResponse<APIUpdateSingleResponse<T>>) => {
        return apiResponse.body.result as T;
      })
    );
  }

  /**
   * Delete a relation by public ID
   */
  public deleteRelation(publicID: number): Observable<T> {
    const options = this.options;
    options.params = new HttpParams();

    return this.api.callDelete<T>(this.servicePrefix + '/' + publicID, options).pipe(
      map((apiResponse: HttpResponse<APIDeleteSingleResponse<T>>) => {
        this.sideBarService.loadCategoryTree();
        return apiResponse.body.raw as T;
      })
    );
  }

}
