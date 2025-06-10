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
// import { NgModule } from '@angular/core';
// import { RouterModule, Routes } from '@angular/router';
// import { RiskAssessmentAddComponent } from './risk-assessment-add/risk-assessment-add.component';
// import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';
// import { RiskAssessmentListComponent } from './risk-assesment-list/risk-assessment-list.component';



// const routes: Routes = [
//   /* ➜ CREATE ------------------------------------------------------------- */
//   { path:'risks/:riskId/risk-assessments/add',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'objects/:objectId/risk-assessments/add',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'object-groups/:groupId/risk-assessments/add', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

//   /* ➜ LIST --------------------------------------------------------------- */
//   { path:'risks/:riskId/risk-assessments',          component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },
//   { path:'objects/:objectId/risk-assessments',      component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },
//   { path:'object-groups/:groupId/risk-assessments', component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },

//   /* ➜ EDIT --------------------------------------------------------------- */
//   { path:'risks/:riskId/risk-assessments/edit/:id',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'objects/:objectId/risk-assessments/edit/:id',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'object-groups/:groupId/risk-assessments/edit/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

//   /* ➜ VIEW --------------------------------------------------------------- */
//   { path:'risks/:riskId/risk-assessments/view/:id',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'objects/:objectId/risk-assessments/view/:id',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'object-groups/:groupId/risk-assessments/view/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

//   /* fall‑back (no context) ---------------------------------------------- */
//   { path:'risk-assessments/edit/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'risk-assessments/view/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path:'risk-assessments/add',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
// ];


// @NgModule({
//   imports: [RouterModule.forChild(routes)  ],
//   exports: [RouterModule]
// })
// export class RiskAssessmentRoutingModule { }


import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RiskAssessmentAddComponent } from './risk-assessment-add/risk-assessment-add.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';
import { RiskAssessmentListComponent } from './risk-assesment-list/risk-assessment-list.component';

const routes: Routes = [
  /* ➜ CREATE ------------------------------------------------------------- */
  {
    path: 'risks/:riskId/risk-assessments/add',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Add Risk Assessment (Risk)' }
  },
  {
    path: 'objects/:objectId/risk-assessments/add',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Add Risk Assessment (Object)' }
  },
  {
    path: 'object-groups/:groupId/risk-assessments/add',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Add Risk Assessment (Group)' }
  },

  /* ➜ LIST --------------------------------------------------------------- */
  {
    path: 'risks/:riskId/risk-assessments',
    component: RiskAssessmentListComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Risk Assessments (Risk)' }
  },
  {
    path: 'objects/:objectId/risk-assessments',
    component: RiskAssessmentListComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Risk Assessments (Object)' }
  },
  {
    path: 'object-groups/:groupId/risk-assessments',
    component: RiskAssessmentListComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Risk Assessments (Group)' }
  },

  /* ➜ EDIT --------------------------------------------------------------- */
  {
    path: 'risks/:riskId/risk-assessments/edit/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Edit Risk Assessment (Risk)' }
  },
  {
    path: 'objects/:objectId/risk-assessments/edit/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Edit Risk Assessment (Object)' }
  },
  {
    path: 'object-groups/:groupId/risk-assessments/edit/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Edit Risk Assessment (Group)' }
  },

  /* ➜ VIEW --------------------------------------------------------------- */
  {
    path: 'risks/:riskId/risk-assessments/view/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'View Risk Assessment (Risk)' }
  },
  {
    path: 'objects/:objectId/risk-assessments/view/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'View Risk Assessment (Object)' }
  },
  {
    path: 'object-groups/:groupId/risk-assessments/view/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'View Risk Assessment (Group)' }
  },

  /* ➜ fall‑back (no context) ---------------------------------------------- */
  {
    path: 'risk-assessments/edit/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Edit Risk Assessment' }
  },
  {
    path: 'risk-assessments/view/:id',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'View Risk Assessment' }
  },
  {
    path: 'risk-assessments/add',
    component: RiskAssessmentAddComponent,
    canActivate: [preCloudGuard],
    data: { breadcrumb: 'Add Risk Assessment' }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RiskAssessmentRoutingModule {}
