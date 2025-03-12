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
import { Component, OnInit } from '@angular/core';
import { IsmsConfig } from '../models/isms-config.model';


@Component({
  selector: 'app-isms-configure',
  templateUrl: './configure.component.html',
  styleUrls: ['./configure.component.scss']
})
export class ConfigureComponent implements OnInit {
  public ismsConfig: IsmsConfig;

  constructor() {
    // Initialize the configuration object with empty arrays
    this.ismsConfig = {
      riskClasses: [],
      likelihoodEntries: [],
      impactEntries: [],
      impactCategories: [],
      protectionGoals: [],
      riskMatrix: null 
    };
  }

  ngOnInit(): void {
  }

  saveIsmsConfig(): void {

  }
}
