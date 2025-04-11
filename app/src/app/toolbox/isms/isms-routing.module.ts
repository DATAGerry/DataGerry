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
import { ControlMeassuresAddComponent } from './control-meassure/control-meassure-add/control-meassures-add.component';
import { ControlMeassuresListComponent } from './control-meassure/control-meassure-list/control-meassure-list.component';
import { PersonListComponent } from './person/person-list/person-list.component';
import { PersonAddEditComponent } from './person/person-add/person-add-edit.component';


const routes: Routes = [
    {
        path: '',
        data: {
            breadcrumb: 'Overview'
        },
        component: IsmsComponent,
        children: [
            { path: '', redirectTo: 'overview', pathMatch: 'full' },
            { path: 'overview', component: OverviewComponent },
            {
                path: 'configure',
                data: {
                    breadcrumb: 'Configure ISMS Settings'
                },
                component: ConfigureComponent
            },
        ]
    },
    { path: 'threats', component: ThreatsListComponent },
    { path: 'threats/add', component: ThreatsAddComponent },
    { path: 'threats/edit/:id', component: ThreatsAddComponent },
    { path: 'vulnerabilities', component: VulnerabilitiesListComponent },
    { path: 'vulnerabilities/add', component: VulnerabilitiesAddComponent },
    { path: 'vulnerabilities/edit', component: VulnerabilitiesAddComponent },
    { path: 'risks', component: RisksListComponent },
    { path: 'risks/add', component: RiskAddComponent },
    { path: 'risks/edit', component: RiskAddComponent },

    { path: 'control-meassures', component: ControlMeassuresListComponent },
    { path: 'control-meassures/add', component: ControlMeassuresAddComponent },
    { path: 'control-meassures/edit', component: ControlMeassuresAddComponent },


    {
        path: 'persons',
        children: [
          { path: '', component: PersonListComponent },
          { path: 'add', component: PersonAddEditComponent },
          { path: 'edit', component: PersonAddEditComponent }
        ]
      },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class IsmsRoutingModule { }
