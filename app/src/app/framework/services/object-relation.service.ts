// src/app/framework/relation/services/object-relation.service.ts
import { Injectable } from '@angular/core';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Observable, map } from 'rxjs';

import { ApiCallService, ApiServicePrefix, resp } from '../../services/api-call.service';
import { SidebarService } from 'src/app/layout/services/sidebar.service';

import {
  APIInsertSingleResponse,
} from '../../services/models/api-response';


export interface CmdbObjectRelationCreateDto {
  relation_id: number;
  relation_parent_id: number;
  relation_child_id: number;
  field_values: Array<{ name: string; value: any }>;
}

@Injectable({
  providedIn: 'root'
})
export class ObjectRelationService implements ApiServicePrefix {
  public servicePrefix: string = 'object_relations'; 

  private options = {
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
   * Create (POST) a new "object relation" record
   * e.g. POST /object_relations
   */
  public postObjectRelation(dto: CmdbObjectRelationCreateDto): Observable<any> {
    const options = { ...this.options };
    return this.api.callPost<any>(this.servicePrefix + '/', dto, options).pipe(
      map((httpResp: HttpResponse<APIInsertSingleResponse<any>>) => {
        // If your API returns the newly created object
        return httpResp.body.raw;
      })
    );
  }

}
