import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { ControlMeasure } from '../models/control-measure.model';

@Injectable({ providedIn: 'root' })
export class RiskTreatmentPlanService extends BaseApiService<any> {
    public servicePrefix = 'isms/reports/risk_treatment_plan';

    constructor(protected api: ApiCallService) {
        super(api);
    }

    /**
     * Get Risk Treatment Plan List
     */
    getRiskTreatmentPlanList(): Observable<any[]> {
        return this.handleGetRequest<any[]>(`${this.servicePrefix}`);
    }
}
