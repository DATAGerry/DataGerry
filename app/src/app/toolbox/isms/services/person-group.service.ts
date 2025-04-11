import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from 'src/app/services/models/api-response';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { CmdbPersonGroup } from '../models/person-group.model';

@Injectable({
  providedIn: 'root'
})
export class PersonGroupService extends BaseApiService<CmdbPersonGroup> {
  public servicePrefix = 'person_groups';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  getPersonGroups(params: CollectionParameters): Observable<APIGetMultiResponse<CmdbPersonGroup>> {
    const httpParams = this.buildHttpParams(params);
    return this.handleGetRequest<APIGetMultiResponse<CmdbPersonGroup>>(`${this.servicePrefix}/`, httpParams);
  }

  createPersonGroup(pg: CmdbPersonGroup): Observable<APIInsertSingleResponse<CmdbPersonGroup>> {
    return this.handlePostRequest<APIInsertSingleResponse<CmdbPersonGroup>>(`${this.servicePrefix}/`, pg);
  }

  updatePersonGroup(id: number, pg: CmdbPersonGroup): Observable<APIUpdateSingleResponse<CmdbPersonGroup>> {
    return this.handlePutRequest<APIUpdateSingleResponse<CmdbPersonGroup>>(`${this.servicePrefix}/${id}`, pg);
  }

  deletePersonGroup(id: number): Observable<APIDeleteSingleResponse<CmdbPersonGroup>> {
    return this.handleDeleteRequest<APIDeleteSingleResponse<CmdbPersonGroup>>(`${this.servicePrefix}/${id}`);
  }
}
