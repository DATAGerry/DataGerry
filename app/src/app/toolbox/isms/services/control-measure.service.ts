/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2025 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { ControlMeassure } from '../models/control-meassure.model';
import {
  APIGetMultiResponse,
  APIInsertSingleResponse,
  APIUpdateSingleResponse,
  APIDeleteSingleResponse
} from 'src/app/services/models/api-response';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { ApiCallService } from 'src/app/services/api-call.service';
import { BaseApiService } from 'src/app/core/services/base-api.service';

@Injectable({
  providedIn: 'root'
})
export class ControlMeasureService extends BaseApiService<ControlMeassure> {
  public servicePrefix = 'isms/control_measures';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  getControlMeasures(params: CollectionParameters): Observable<APIGetMultiResponse<ControlMeassure>> {
    const httpParams = this.buildHttpParams(params);
    return this.handleGetRequest<APIGetMultiResponse<ControlMeassure>>(`${this.servicePrefix}/`, httpParams);
  }

  createControlMeassure(cm: ControlMeassure): Observable<APIInsertSingleResponse<ControlMeassure>> {
    return this.handlePostRequest<APIInsertSingleResponse<ControlMeassure>>(`${this.servicePrefix}/`, cm);
  }

  updateControlMeassure(id: number, cm: ControlMeassure): Observable<APIUpdateSingleResponse<ControlMeassure>> {
    return this.handlePutRequest<APIUpdateSingleResponse<ControlMeassure>>(`${this.servicePrefix}/${id}`, cm);
  }

  deleteControlMeassure(id: number): Observable<APIDeleteSingleResponse<ControlMeassure>> {
    return this.handleDeleteRequest<APIDeleteSingleResponse<ControlMeassure>>(`${this.servicePrefix}/${id}`);
  }
}