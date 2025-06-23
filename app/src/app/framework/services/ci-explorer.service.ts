

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  GraphRespWithRoot,
  GraphRespChildren,
  GraphRespParents,
} from '../models/ci-explorer.model';
import { BaseApiService } from 'src/app/core/services/base-api.service';
import { ApiCallService } from 'src/app/services/api-call.service';



@Injectable({
  providedIn: 'root',
})
export class CiExplorerService extends BaseApiService<never> {
  public servicePrefix = 'ci_explorer/items';

  constructor(protected api: ApiCallService) {
    super(api);
  }

  /* ------------------------------------------------------------------
     initial page-load  (root + 1-level parents & children)
     ------------------------------------------------------------------ */
  loadWithRoot(targetId: number): Observable<GraphRespWithRoot> {
    const url =
      `${this.servicePrefix}` +
      `?target_id=${targetId}` +
      `&target_type=BOTH` +
      `&with_root=true`;

    return this.handleGetRequest<GraphRespWithRoot>(url);
  }

  /* ------------------------------------------------------------------
     expand CHILDRen of a node
     ------------------------------------------------------------------ */
  expandChild(targetId: number): Observable<GraphRespChildren> {
    const url =
      `${this.servicePrefix}` +
      `?target_id=${targetId}` +
      `&target_type=CHILD` +
      `&with_root=false`;

    return this.handleGetRequest<GraphRespChildren>(url);
  }

  /* ------------------------------------------------------------------
     expand PARENTS of a node
     ------------------------------------------------------------------ */
  expandParent(targetId: number): Observable<GraphRespParents> {
    const url =
      `${this.servicePrefix}` +
      `?target_id=${targetId}` +
      `&target_type=PARENT` +
      `&with_root=false`;

    return this.handleGetRequest<GraphRespParents>(url);
  }
}
