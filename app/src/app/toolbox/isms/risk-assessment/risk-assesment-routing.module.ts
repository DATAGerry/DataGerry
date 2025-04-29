import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RiskAssessmentAddComponent } from './risk-assessment-add/risk-assessment-add.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';



const routes: Routes = [
    { path: 'risks/:riskId/risk-assessments/add', component: RiskAssessmentAddComponent, canActivate: [preCloudGuard] },
    { path: 'objects/:objectId/risk-assessments/add', component: RiskAssessmentAddComponent, canActivate: [preCloudGuard] },
    { path: 'object-groups/:groupId/risk-assessments/add', component: RiskAssessmentAddComponent, canActivate: [preCloudGuard] },
  ];
  

@NgModule({
  imports: [RouterModule.forChild(routes)  ],
  exports: [RouterModule]
})
export class RiskAssessmentRoutingModule { }
