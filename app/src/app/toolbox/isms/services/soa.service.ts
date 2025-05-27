import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { ControlMeasure } from '../models/control-measure.model';

@Injectable({ providedIn: 'root' })
export class SoaService extends BaseApiService<ControlMeasure> {
  public servicePrefix = 'isms/reports/soa';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  getSoaList(): Observable<ControlMeasure[]> {
    return this.handleGetRequest<ControlMeasure[]>(`${this.servicePrefix}`);
  }
}
