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
import { UntypedFormControl } from '@angular/forms';

import { FileConfig } from '../file-config/file-config';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    templateUrl: './csv-config.component.html',
    styleUrls: ['./csv-config.component.scss']
})
export class CsvConfigComponent extends FileConfig implements OnInit {

    public constructor() {
        super();
    }


    public ngOnInit(): void {
        for (const defaultConfigEntry in this.defaultParserConfig) {
            this.configForm.addControl(defaultConfigEntry, new UntypedFormControl(''));
        }

        this.configForm.patchValue(this.defaultParserConfig);
    }
}
