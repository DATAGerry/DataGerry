import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { IsmsComponent } from './isms.component';
import { OverviewComponent } from './overview/overview.component';
import { ConfigureComponent } from './configure/configure.component';

const routes: Routes = [
    {
        path: '',
        component: IsmsComponent,
        children: [
            { path: '', redirectTo: 'overview', pathMatch: 'full' },
            { path: 'overview', component: OverviewComponent },
            { path: 'configure', component: ConfigureComponent },
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class IsmsRoutingModule { }
