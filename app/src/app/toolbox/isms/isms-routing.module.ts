import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { IsmsComponent } from './isms.component';
import { OverviewComponent } from './overview/overview.component';
import { ConfigureComponent } from './configure/configure.component';
import { ThreatsListComponent } from './threats/threats-list.component';
import { ThreatsAddComponent } from './threats/add/threats-add.component';
import { VulnerabilitiesListComponent } from './vulnerabilities/vulnerabilities-list.component';
import { VulnerabilitiesAddComponent } from './vulnerabilities/add/vulnerabilities-add.component';

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
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class IsmsRoutingModule { }
