import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { IsmsComponent } from './isms.component';
import { OverviewComponent } from './overview/overview.component';
import { ConfigureComponent } from './configure/configure.component';
import { ThreatsListComponent } from './threats/threats-list.component';
import { ThreatsAddComponent } from './threats/add/threats-add.component';
import { VulnerabilitiesListComponent } from './vulnerabilities/vulnerabilities-list.component';
import { VulnerabilitiesAddComponent } from './vulnerabilities/add/vulnerabilities-add.component';
import { RisksListComponent } from './risks/risks-list/risks-list.component';
import { RiskAddComponent } from './risks/risks-add/risks-add.component';
import { ControlmeasuresListComponent } from './control-measure/control-measure-list/control-measure-list.component';
import { ControlMeasuresAddComponent } from './control-measure/control-measure-add/control-measures-add.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';


const routes: Routes = [
    {
        path: '',
        data: {
            breadcrumb: 'Overview'
        },
        component: IsmsComponent,
        canActivate: [preCloudGuard],
        children: [
            { path: '', redirectTo: 'overview', pathMatch: 'full', canActivate: [preCloudGuard] },
            { path: 'overview', component: OverviewComponent, canActivate: [preCloudGuard] },
            {
                path: 'configure',
                data: {
                    breadcrumb: 'Configure ISMS Settings'
                },
                component: ConfigureComponent,
                canActivate: [preCloudGuard]
            },
        ]
    },
    { path: 'threats', component: ThreatsListComponent, canActivate: [preCloudGuard] },
    { path: 'threats/add', component: ThreatsAddComponent, canActivate: [preCloudGuard] },
    { path: 'threats/edit/:id', component: ThreatsAddComponent, canActivate: [preCloudGuard] },
    { path: 'vulnerabilities', component: VulnerabilitiesListComponent, canActivate: [preCloudGuard] },
    { path: 'vulnerabilities/add', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },
    { path: 'vulnerabilities/edit', component: VulnerabilitiesAddComponent, canActivate: [preCloudGuard] },
    { path: 'risks', component: RisksListComponent, canActivate: [preCloudGuard] },
    { path: 'risks/add', component: RiskAddComponent, canActivate: [preCloudGuard] },
    { path: 'risks/edit', component: RiskAddComponent, canActivate: [preCloudGuard] },

    { path: 'control-measures', component: ControlmeasuresListComponent, canActivate: [preCloudGuard] },
    { path: 'control-measures/add', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard] },
    { path: 'control-measures/edit', component: ControlMeasuresAddComponent, canActivate: [preCloudGuard] },


];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class IsmsRoutingModule { }
