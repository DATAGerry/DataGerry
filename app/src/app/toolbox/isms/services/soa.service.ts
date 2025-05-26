import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  APIGetMultiResponse
} from 'src/app/services/models/api-response';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { ControlMeasure } from '../models/control-measure.model';

@Injectable({ providedIn: 'root' })
export class SoaService extends BaseApiService<ControlMeasure> {
  public servicePrefix = 'isms/reports/soa';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  /** Get SOA list */
  getSoaList() {
    return this.handleGetRequest<APIGetMultiResponse<ControlMeasure>>(
      `${this.servicePrefix}`
    );
  }
}
