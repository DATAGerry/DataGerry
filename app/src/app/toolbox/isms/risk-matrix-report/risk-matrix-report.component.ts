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

import { RiskMatrixReportService } from '../services/risk-matrix-report.service';
import { ToastService } from 'src/app/layout/toast/toast.service';



@Component({
    selector: 'app-risk-matrix-report',
    templateUrl: './risk-matrix-report.component.html',
    styleUrls: ['./risk-matrix-report.component.scss']
})
export class RiskMatrixReportComponent implements OnInit {



    loading = false;

    constructor(
        private readonly reportSrv: RiskMatrixReportService,
        private readonly toastService: ToastService,

    ) { }

    ngOnInit(): void { 
        this.reportSrv.getReport1()
        .subscribe({
            next: (res) => {
               console.log('RiskMatrixReport', res);
            },
            error: (error) => {
                this.toastService.error(error?.error?.message);
            }
        });
     }


}
