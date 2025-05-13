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
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';

import { IsmsComponent } from './isms.component';
import { OverviewComponent } from './overview/overview.component';
import { ConfigureComponent } from './configure/configure.component';

import { ThreatsListComponent } from './threats/threats-list.component';
import { ThreatsAddComponent } from './threats/add/threats-add.component';
import { VulnerabilitiesListComponent } from './vulnerabilities/vulnerabilities-list.component';
import { VulnerabilitiesAddComponent } from './vulnerabilities/add/vulnerabilities-add.component';

import { RisksListComponent } from './risks/risks-list/risks-list.component';

import { ControlmeasuresListComponent } from './control-measure/control-measure-list/control-measure-list.component';
import { ControlMeasuresAddComponent }   from './control-measure/control-measure-add/control-measures-add.component';
import { ControlMeasureAssignmentAddComponent } from './control‑measure‑assignment/control‑measure‑assignment-add/control-measure-assignment-add.component';
import { ControlMeasureAssignmentListComponent } from './control‑measure‑assignment/control‑measure‑assignment-list/control‑measure‑assignment-list.component';
import { RiskAddComponent } from './risks/risks-add/risks-add.component';


const routes: Routes = [
  {
    path: '',
    component: IsmsComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Overview' },
    children: [
      { path: '', redirectTo: 'overview', pathMatch: 'full', canActivate: [preCloudGuard] },
      { path: 'overview', component: OverviewComponent, canActivate: [preCloudGuard] },
      {
        path: 'configure',
        component: ConfigureComponent,
        canActivate: [preCloudGuard],
        data: { breadcrumb: 'Configure ISMS Settings' }
      }
    ]
  },

  /* ─── threats ─── */
  { path: 'threats',              component: ThreatsListComponent, canActivate: [preCloudGuard] },
  { path: 'threats/add',          component: ThreatsAddComponent,  canActivate: [preCloudGuard] },
  { path: 'threats/edit/:id',     component: ThreatsAddComponent,  canActivate: [preCloudGuard] },

  /* ─── vulnerabilities ─── */
  { path: 'vulnerabilities',      component: VulnerabilitiesListComponent, canActivate: [preCloudGuard] },
  { path: 'vulnerabilities/add',  component: VulnerabilitiesAddComponent,  canActivate: [preCloudGuard] },
  { path: 'vulnerabilities/edit', component: VulnerabilitiesAddComponent,  canActivate: [preCloudGuard] },

  /* ─── risks ─── */
  { path: 'risks',       component: RisksListComponent, canActivate: [preCloudGuard] },
  { path: 'risks/add',   component: RiskAddComponent,   canActivate: [preCloudGuard] },
  { path: 'risks/edit',  component: RiskAddComponent,   canActivate: [preCloudGuard] },
  { path: 'risks/view',  component: RiskAddComponent,   canActivate: [preCloudGuard] },

  /* ─── control / measures ─── */
  { path: 'control-measures',      component: ControlmeasuresListComponent, canActivate: [preCloudGuard] },
  { path: 'control-measures/add',  component: ControlMeasuresAddComponent,  canActivate: [preCloudGuard] },
  { path: 'control-measures/edit', component: ControlMeasuresAddComponent,  canActivate: [preCloudGuard] },
  { path: 'control-measures/view', component: ControlMeasuresAddComponent,  canActivate: [preCloudGuard] },

  /* ─── Control‑Measure Assignments (generic) ─── */
/* ─── Control‑Measure Assignments ─── */
{
  path: 'control-measure-assignments',
  component: ControlMeasureAssignmentListComponent,
  canActivate: [preCloudGuard]
},
{
  path: 'control-measure-assignments/add',
  component: ControlMeasureAssignmentAddComponent,
  canActivate: [preCloudGuard]
},
{
  path: 'control-measure-assignments/edit',
  component: ControlMeasureAssignmentAddComponent,
  canActivate: [preCloudGuard]
},

/* embedded under Risk Assessment */
{
  path: 'risk_assessments/:riskId/control_measure_assignments',
  component: ControlMeasureAssignmentListComponent,
  canActivate: [preCloudGuard]
},
{
  path: 'risk_assessments/:riskId/control_measure_assignments/add',
  component: ControlMeasureAssignmentAddComponent,
  canActivate: [preCloudGuard]
},

/* embedded under Control / Measure */
{
  path: 'control_measures/:cmId/control_measure_assignments',
  component: ControlMeasureAssignmentListComponent,
  canActivate: [preCloudGuard]
},
{
  path: 'control_measures/:cmId/control_measure_assignments/add',
  component: ControlMeasureAssignmentAddComponent,
  canActivate: [preCloudGuard]
}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class IsmsRoutingModule {}
