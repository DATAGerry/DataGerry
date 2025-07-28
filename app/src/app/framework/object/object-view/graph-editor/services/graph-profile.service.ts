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

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { FilterProfile } from '../interfaces/graph.interfaces';
import { BaseApiService } from 'src/app/core/services/base-api.service';

@Injectable({ providedIn: 'root' })
export class GraphProfileService extends BaseApiService<FilterProfile> {
  public servicePrefix = 'ci_explorer/profile';

  getProfiles(): Observable<FilterProfile[]> {
    return this.handleGetRequest<any>(`${this.servicePrefix}`)
      .pipe(
        map(response => response.results)
      );
  }

  createProfile(profile: FilterProfile): Observable<FilterProfile> {
    return this.handlePostRequest<FilterProfile>(`${this.servicePrefix}`, profile);
  }

  updateProfile(id: number, profile: FilterProfile): Observable<FilterProfile> {
    return this.handlePutRequest<FilterProfile>(`${this.servicePrefix}/${id}`, profile);
  }

  deleteProfile(id: number): Observable<void> {
    return this.handleDeleteRequest<void>(`${this.servicePrefix}/${id}`);
  }
}