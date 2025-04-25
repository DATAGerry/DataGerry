import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PersonListComponent } from './person-list/person-list.component';
import { PersonAddEditComponent } from './person-add/person-add-edit.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';

const routes: Routes = [

    {
        path: 'persons',
        children: [
            {
                path: '', component: PersonListComponent,
                data: {
                    breadcrumb: 'Persons',
                    right: 'base.user-management.person.view'
                },
                canActivate: [preCloudGuard]
            },
            {
                path: 'add', component: PersonAddEditComponent,
                data: {
                    breadcrumb: 'Add Person',
                    right: 'base.user-management.person.add'
                },
                canActivate: [preCloudGuard]
            },
            {
                path: 'edit', component: PersonAddEditComponent,
                data: {
                    breadcrumb: 'Edit Person',
                    right: 'base.user-management.person.edit'
                },
                canActivate: [preCloudGuard]
            }
        ]
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PersonRoutingModule { }
