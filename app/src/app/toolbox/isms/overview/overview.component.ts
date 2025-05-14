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
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ISMSService } from '../services/isms.service';
import { IsmsConfigValidation } from '../models/isms-config-validation.model';

@Component({
  selector: 'app-isms-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  public validationStatus: boolean = false;

  constructor(private ismsService: ISMSService,
    private cdRef: ChangeDetectorRef

  ) { }

  ngOnInit(): void {
    this.ismsService.getIsmsValidationStatus().subscribe((status: IsmsConfigValidation) => {
      this.validationStatus =
        status.risk_classes &&
        status.likelihoods &&
        status.impacts &&
        status.impact_categories &&
        status.risk_matrix;
  
      this.cdRef.detectChanges();
    });
  }
  
}
