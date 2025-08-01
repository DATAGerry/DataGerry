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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, Input } from '@angular/core';

import { CmdbType, CmdbTypeSection } from '../../../models/cmdb-type';
import { BaseSectionComponent } from '../base-section/base-section.component';
import { RenderResult } from 'src/app/framework/models/cmdb-render';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector: 'cmdb-sections-factory',
    templateUrl: './sections-factory.component.html',
    styleUrls: ['./sections-factory.component.scss']
})
export class SectionsFactoryComponent extends BaseSectionComponent  {
    @Input() public sections: Array<CmdbTypeSection> = [];
    @Input() objectID: number;
    @Input() public typeInstance: CmdbType;
    @Input() public renderResult: RenderResult;

    constructor() {
        super();

    
    }
}
