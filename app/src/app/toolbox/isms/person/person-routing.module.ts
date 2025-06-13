import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PersonListComponent } from './person-list/person-list.component';
import { PersonAddEditComponent } from './person-add/person-add-edit.component';

const routes: Routes = [

    {
        path: '',
        children: [
            {
                path: '', component: PersonListComponent,
                data: {
                    breadcrumb: 'Persons',
                    right: 'base.user-management.person.view'
                },
            },
            {
                path: 'add', component: PersonAddEditComponent,
                data: {
                    breadcrumb: 'Add Person',
                    right: 'base.user-management.person.add'
                },
            },
            {
                path: 'edit', component: PersonAddEditComponent,
                data: {
                    breadcrumb: 'Edit Person',
                    right: 'base.user-management.person.edit'
                },
            }
        ]
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class PersonRoutingModule { }
