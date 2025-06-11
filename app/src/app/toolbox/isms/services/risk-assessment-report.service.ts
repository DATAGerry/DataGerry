import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';

@Injectable({ providedIn: 'root' })
export class RiskAssesmentsReportService extends BaseApiService<any> {
  public servicePrefix = 'isms/reports/risk_assessments';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  /**
   * Fetch the full Risk assessments reportlist from the backend.
   */
  getRiskAssesmentsReportList(): Observable<any[]> {
    return this.handleGetRequest<any[]>(`${this.servicePrefix}`);
  }

}
