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
import { ControlMeasureAssignment } from '../models/control‑measure‑assignment.model';

@Injectable({ providedIn: 'root' })
export class ControlMeasureAssignmentService extends BaseApiService<ControlMeasureAssignment> {
  public servicePrefix = 'isms/control_measure_assignments';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  getAssignments(params: CollectionParameters): Observable<APIGetMultiResponse<ControlMeasureAssignment>> {
    const httpParams = this.buildHttpParams(params);
    return this.handleGetRequest<APIGetMultiResponse<ControlMeasureAssignment>>(
      `${this.servicePrefix}/`, httpParams);
  }

  createAssignment(a: ControlMeasureAssignment):
    Observable<APIInsertSingleResponse<ControlMeasureAssignment>> {
    return this.handlePostRequest<APIInsertSingleResponse<ControlMeasureAssignment>>(
      `${this.servicePrefix}/`, a);
  }

  updateAssignment(id: number, a: ControlMeasureAssignment):
    Observable<APIUpdateSingleResponse<ControlMeasureAssignment>> {
    return this.handlePutRequest<APIUpdateSingleResponse<ControlMeasureAssignment>>(
      `${this.servicePrefix}/${id}`, a);
  }

  deleteAssignment(id: number):
    Observable<APIDeleteSingleResponse<ControlMeasureAssignment>> {
    return this.handleDeleteRequest<APIDeleteSingleResponse<ControlMeasureAssignment>>(
      `${this.servicePrefix}/${id}`);
  }
}
