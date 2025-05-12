// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';

// import { IsmsComponent } from './isms.component';
// import { OverviewComponent } from './overview/overview.component';
// import { ConfigureComponent } from './configure/configure.component';
// import { ThreatsListComponent } from './threats/threats-list.component';
// import { ThreatsAddComponent } from './threats/add/threats-add.component';
// import { VulnerabilitiesListComponent } from './vulnerabilities/vulnerabilities-list.component';
// import { VulnerabilitiesAddComponent } from './vulnerabilities/add/vulnerabilities-add.component';
// import { RisksListComponent } from './risks/risks-list/risks-list.component';
// import { RiskAddComponent } from './risks/risks-add/risks-add.component';
// import { ControlmeasuresListComponent } from './control-measure/control-measure-list/control-measure-list.component';
// import { ControlMeasuresAddComponent } from './control-measure/control-measure-add/control-measures-add.component';
// import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';
// import { ControlMeasureAssignmentListComponent } from './control‑measure‑assignment/control‑measure‑assignment-list/control‑measure‑assignment-list.component';
// import { ControlMeasureAssignmentAddComponent } from './control‑measure‑assignment/control‑measure‑assignment-add/control-measure-assignment-add.component';


// const routes: Routes = [
//     {
//         path: '',
//         data: {
//             breadcrumb: 'Overview'
//         },
//         component: IsmsComponent,
//         canActivate: [preCloudGuard],
//         children: [
//             { path: '', redirectTo: 'overview', pathMatch: 'full', canActivate: [preCloudGuard] },
//             { path: 'overview', component: OverviewComponent, canActivate: [preCloudGuard] },
//             {
//                 path: 'configure',
//                 data: {
//                     breadcrumb: 'Configure ISMS Settings'
//                 },
//                 component: ConfigureComponent,
//                 canActivate: [preCloudGuard]
//             },
//         ]
//     },
//     { path: 'threats', component: ThreatsListComponent, canActivate: [preCloudGuard] },
//     { path: 'threats/add', component: ThreatsAddComponent, canActivate: [preCloudGuard] },
//     { path: 'threats/edit/:id', component: ThreatsAddComponent, canActivate: [preCloudGuard] },
//     { path: 'vulnerabilities', component: VulnerabilitiesListComponent, canActivate: [preCloudGuard] },
//     { path: 'vulnerabilities/add', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },
//     { path: 'vulnerabilities/edit', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },

//     { path: 'risks', component: RisksListComponent, canActivate: [preCloudGuard] },
//     { path: 'risks/add', component: RiskAddComponent, canActivate: [preCloudGuard] },
//     { path: 'risks/edit', component: RiskAddComponent, canActivate: [preCloudGuard] },
//     { path: 'risks/view', component: RiskAddComponent, canActivate: [preCloudGuard] },

//     { path: 'control-measures', component: ControlmeasuresListComponent, canActivate: [preCloudGuard] },
//     { path: 'control-measures/add', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard] },
//     { path: 'control-measures/edit', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard] },


//     {
//         path: 'control-measure-assignments',
//         component: ControlMeasureAssignmentListComponent,
//         data: {
//             breadcrumb: 'Control / Measure Assignments',
//             permission: 'base.isms.control_measure_assignment.view'
//         }
//     },
//     {
//         path: 'control-measure-assignments/add',
//         component: ControlMeasureAssignmentAddComponent,
//         data: {
//             breadcrumb: 'Add Control / Measure Assignment',
//             permission: 'base.isms.control_measure_assignment.add'
//         }
//     },
//     {
//         path: 'control-measure-assignments/edit',
//         component: ControlMeasureAssignmentAddComponent,
//         data: {
//             breadcrumb: 'Edit Control / Measure Assignment',
//             permission: 'base.isms.control_measure_assignment.edit'
//         }
//     }

// ];

// @NgModule({
//     imports: [RouterModule.forChild(routes)],
//     exports: [RouterModule]
// })
// export class IsmsRoutingModule { }


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
  {
    path: 'control-measure-assignments',
    component: ControlMeasureAssignmentListComponent,
    data: {
      breadcrumb: 'Control / Measure Assignments',
      permission: 'base.isms.control_measure_assignment.view'
    },
    canActivate: [preCloudGuard]
  },
  {
    path: 'control-measure-assignments/add',
    component: ControlMeasureAssignmentAddComponent,
    data: {
      breadcrumb: 'Add Control / Measure Assignment',
      permission: 'base.isms.control_measure_assignment.add'
    },
    canActivate: [preCloudGuard]
  },

  /* ─── nested under Risk Assessment ─── */
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

  /* ─── nested under Control / Measure ─── */
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
