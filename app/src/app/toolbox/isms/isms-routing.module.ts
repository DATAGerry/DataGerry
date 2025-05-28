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
import { ControlMeasuresAddComponent } from './control-measure/control-measure-add/control-measures-add.component';
import { ControlMeasureAssignmentAddComponent } from './control‑measure‑assignment/control‑measure‑assignment-add/control-measure-assignment-add.component';
import { ControlMeasureAssignmentListComponent } from './control‑measure‑assignment/control‑measure‑assignment-list/control‑measure‑assignment-list.component';
import { RiskAddComponent } from './risks/risks-add/risks-add.component';
import { RiskMatrixReportComponent } from './risk-matrix-report/risk-matrix-report.component';
import { SoaComponent } from './reporting/soa/soa.component';
import { RiskTreatmentPlanComponent } from './reporting/risk-treatment-plan/risk-treatment-plan.component';
import { RiskAssesmentsComponent } from './reporting/risk-assesments/risk-assesments.component';


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
  // { path: 'threats', component: ThreatsListComponent, canActivate: [preCloudGuard] },
  // { path: 'threats/add', component: ThreatsAddComponent, canActivate: [preCloudGuard] },
  // { path: 'threats/edit/:id', component: ThreatsAddComponent, canActivate: [preCloudGuard] },

  {
    path: 'threats',
    component: ThreatsListComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Threats',
      right: 'base.isms.threat.view' // Permission to view threats
    }
  },
  {
    path: 'threats/add',
    component: ThreatsAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Add Threat',
      right: 'base.isms.threat.add'
    }
  },
  {
    path: 'threats/edit/:id',
    component: ThreatsAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Edit Threat',
      right: 'base.isms.threat.edit'
    }
  },
  {
    path: 'threats/view',
    component: ThreatsAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'View Threat',
      right: 'base.isms.threat.view'
    }
  },

  /* ─── vulnerabilities ─── */
  // { path: 'vulnerabilities', component: VulnerabilitiesListComponent, canActivate: [preCloudGuard] },
  // { path: 'vulnerabilities/add', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },
  // { path: 'vulnerabilities/edit', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },

  {
    path: 'vulnerabilities',
    component: VulnerabilitiesListComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Vulnerabilities',
      right: 'base.isms.vulnerability.view' // Permission to view vulnerabilities
    }
  },
  {
    path: 'vulnerabilities/add',
    component: VulnerabilitiesAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Add Vulnerability',
      right: 'base.isms.vulnerability.add' // Permission to add vulnerabilities
    }
  },
  {
    path: 'vulnerabilities/edit',
    component: VulnerabilitiesAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Edit Vulnerability',
      right: 'base.isms.vulnerability.edit' // Permission to edit vulnerabilities
    }
  },
  {
    path: 'vulnerabilities/view',
    component: VulnerabilitiesAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'View Vulnerability',
      right: 'base.isms.vulnerability.view' // Permission to view vulnerabilities
    }
  },


  /* ─── risks ─── */
  // { path: 'risks',       component: RisksListComponent, canActivate: [preCloudGuard] },
  // { path: 'risks/add',   component: RiskAddComponent,   canActivate: [preCloudGuard] },
  // { path: 'risks/edit',  component: RiskAddComponent,   canActivate: [preCloudGuard] },
  // { path: 'risks/view',  component: RiskAddComponent,   canActivate: [preCloudGuard] },

  {
    path: 'risks',
    component: RisksListComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Risks',
      right: 'base.isms.risk.view'
    }
  },
  {
    path: 'risks/add',
    component: RiskAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Add Risk',
      right: 'base.isms.risk.add'
    }
  },
  {
    path: 'risks/edit',
    component: RiskAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Edit Risk',
      right: 'base.isms.risk.edit'
    }
  },
  {
    path: 'risks/view',
    component: RiskAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'View Risk',
      right: 'base.isms.risk.view'
    }
  },

  /* ─── control / measures ─── */
  // { path: 'control-measures', component: ControlmeasuresListComponent, canActivate: [preCloudGuard], data: { breadcrumb: 'Control Measures' } },
  // { path: 'control-measures/add', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard], data: { breadcrumb: 'Add Control Measure' } },
  // { path: 'control-measures/edit', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard], data: { breadcrumb: 'Edit Control Measure' } },
  // { path: 'control-measures/view', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard] , data: { breadcrumb: 'View Control Measure' } },

  /* ─── Control‑Measure Assignments (generic) ─── */
  /* ─── Control‑Measure Assignments ─── */
  // {
  //   path: 'control-measure-assignments',
  //   component: ControlMeasureAssignmentListComponent,
  //   canActivate: [preCloudGuard]
  // },
  // {
  //   path: 'control-measure-assignments/add',
  //   component: ControlMeasureAssignmentAddComponent,
  //   canActivate: [preCloudGuard]
  // },
  // {
  //   path: 'control-measure-assignments/edit',
  //   component: ControlMeasureAssignmentAddComponent,
  //   canActivate: [preCloudGuard]
  // },

  {
    path: 'control-measures',
    component: ControlmeasuresListComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Control Measures',
      right: 'base.isms.controlMeasure.view'
    }
  },
  {
    path: 'control-measures/add',
    component: ControlMeasuresAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Add Control Measure',
      right: 'base.isms.controlMeasure.add' 
    }
  },
  {
    path: 'control-measures/edit',
    component: ControlMeasuresAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Edit Control Measure',
      right: 'base.isms.controlMeasure.edit' 
    }
  },
  {
    path: 'control-measures/view',
    component: ControlMeasuresAddComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'View Control Measure',
      right: 'base.isms.controlMeasure.view'
    }
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
  },
  {
    path: 'reports/risk_matrix',
    component: RiskMatrixReportComponent,
    canActivate: [preCloudGuard],
    data: {
      breadcrumb: 'Risk Matrix Report',
    }
  },

  {
    path: 'reports/soa',
    component: SoaComponent,
    data: { breadcrumb: 'SOA' }
  },

  {
    path: 'reports/risk_treatment_plan',
    component: RiskTreatmentPlanComponent,
    data: { breadcrumb: 'Risk Treatment Plan'}
  },

  {
    path: 'reports/risk_assesments',
    component: RiskAssesmentsComponent,
    data: { breadcrumb: 'Risk Assesments' } 
  }
  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class IsmsRoutingModule { }
