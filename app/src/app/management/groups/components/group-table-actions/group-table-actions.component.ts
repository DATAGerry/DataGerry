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

import { Component, Input } from '@angular/core';
import { Group } from '../../../models/group';

@Component({
  selector: 'cmdb-group-table-actions',
  templateUrl: './group-table-actions.component.html',
  styleUrls: ['./group-table-actions.component.scss']
})
export class GroupTableActionsComponent {

  /**
   * PublicID of groups which are not delete able.
   */
  public readonly notDeleteAbleGroups: Array<number> = [1, 2];

  @Input() group: Group;

}
