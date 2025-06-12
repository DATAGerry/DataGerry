/* risk-assessment.service.ts */
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  APIGetMultiResponse,
  APIGetSingleResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from 'src/app/services/models/api-response';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { RiskAssessment } from '../models/risk-assessment.model';

type DuplicateRefType = 'risk' | 'object' | 'object_group';


@Injectable({
  providedIn: 'root'
})
export class RiskAssessmentService extends BaseApiService<RiskAssessment> {
  public servicePrefix = 'isms/risk_assessments';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  getRiskAssessments(params: CollectionParameters): Observable<APIGetMultiResponse<RiskAssessment>> {
    const httpParams = this.buildHttpParams(params);
    return this.handleGetRequest<APIGetMultiResponse<RiskAssessment>>(`${this.servicePrefix}/`, httpParams);
  }

  getRiskAssessmentById(id: number): Observable<APIGetSingleResponse<RiskAssessment>> {
    return this.handleGetRequest<APIGetSingleResponse<RiskAssessment>>(`${this.servicePrefix}/${id}`);
  }

  createRiskAssessment(payload: RiskAssessment): Observable<APIInsertSingleResponse<RiskAssessment>> {
    return this.handlePostRequest<APIInsertSingleResponse<RiskAssessment>>(`${this.servicePrefix}/`, payload);
  }

  updateRiskAssessment(id: number, payload: RiskAssessment): Observable<APIUpdateSingleResponse<RiskAssessment>> {
    return this.handlePutRequest<APIUpdateSingleResponse<RiskAssessment>>(`${this.servicePrefix}/${id}`, payload);
  }

  deleteRiskAssessment(id: number): Observable<APIDeleteSingleResponse<RiskAssessment>> {
    return this.handleDeleteRequest<APIDeleteSingleResponse<RiskAssessment>>(`${this.servicePrefix}/${id}`);
  }

  /** Duplicate one or more risk-assessments.  
 *  `ids` – array of risk-assessment `public_id`s to duplicate (will be comma-joined)  
 *  `refType` – context path segment (`risk|object|object_group`)  
 *  `copyCma` – whether control-measure assignments should also be cloned  */
/* risk-assessment.service.ts */
/* ADD / REPLACE this method */
duplicateRiskAssessments(
  targetIds: number[],
  refType: 'risk' | 'object' | 'object_group',
  copyCma = false,
  payload: any = {}
) {
  // URL must contain IDs wrapped in quotes:  "1,2,3"
  const idSegment = `"${targetIds.join(',')}"`;
  const url = `${this.servicePrefix}/duplicate/${refType}/${idSegment}?copy_cma=${copyCma}`;

  return this.handlePostRequest(url, payload);
}


}
