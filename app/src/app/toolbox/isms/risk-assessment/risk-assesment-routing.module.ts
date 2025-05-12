import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RiskAssessmentAddComponent } from './risk-assessment-add/risk-assessment-add.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';
import { RiskAssessmentListComponent } from './risk-assesment-list/risk-assessment-list.component';



// risk-assessment-routing.module.ts
// const routes: Routes = [
//   /* create screens (already there) */
//   { path: 'risks/:riskId/risk-assessments/add',        component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path: 'objects/:objectId/risk-assessments/add',    component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path: 'object-groups/:groupId/risk-assessments/add', component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

//   /* NEW – list */
//   { path: 'risks/:riskId/risk-assessments',            component: RiskAssessmentListComponent, canActivate:[preCloudGuard] },
//   { path: 'objects/:objectId/risk-assessments',        component: RiskAssessmentListComponent, canActivate:[preCloudGuard] },
//   { path: 'object-groups/:groupId/risk-assessments',   component: RiskAssessmentListComponent, canActivate:[preCloudGuard] },

//   { path: 'risk-assessments/view/:id',  component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path: 'risk-assessments/edit/:id',  component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
//   { path: 'risk-assessments/add',       component: RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
// ];

const routes: Routes = [
  /* ➜ CREATE ------------------------------------------------------------- */
  { path:'risks/:riskId/risk-assessments/add',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'objects/:objectId/risk-assessments/add',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'object-groups/:groupId/risk-assessments/add', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

  /* ➜ LIST --------------------------------------------------------------- */
  { path:'risks/:riskId/risk-assessments',          component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },
  { path:'objects/:objectId/risk-assessments',      component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },
  { path:'object-groups/:groupId/risk-assessments', component:RiskAssessmentListComponent, canActivate:[preCloudGuard] },

  /* ➜ EDIT --------------------------------------------------------------- */
  { path:'risks/:riskId/risk-assessments/edit/:id',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'objects/:objectId/risk-assessments/edit/:id',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'object-groups/:groupId/risk-assessments/edit/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

  /* ➜ VIEW --------------------------------------------------------------- */
  { path:'risks/:riskId/risk-assessments/view/:id',          component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'objects/:objectId/risk-assessments/view/:id',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'object-groups/:groupId/risk-assessments/view/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },

  /* fall‑back (no context) ---------------------------------------------- */
  { path:'risk-assessments/edit/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'risk-assessments/view/:id', component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
  { path:'risk-assessments/add',      component:RiskAssessmentAddComponent, canActivate:[preCloudGuard] },
];




  

@NgModule({
  imports: [RouterModule.forChild(routes)  ],
  exports: [RouterModule]
})
export class RiskAssessmentRoutingModule { }
