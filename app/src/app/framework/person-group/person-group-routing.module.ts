import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { PersonGroupListComponent } from './person-group-list/person-group-list.component';
import { PersonGroupAddEditComponent } from './person-group-add/person-group-add-edit.component';

const routes: Routes = [

  {
    path: '', component: PersonGroupListComponent,
    data: {
      breadcrumb: 'New',
      right: 'base.user-management.personGroup.view'
    },
  },
  {
    path: 'add', component: PersonGroupAddEditComponent,
    data: {
      breadcrumb: 'Add',
      right: 'base.user-management.personGroup.add'
    },
  },
  {
    path: 'edit', component: PersonGroupAddEditComponent,
    data: {
      breadcrumb: 'Edit',
      right: 'base.user-management.personGroup.edit'
    },
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)  ],
  exports: [RouterModule]
})
export class PersonGroupRoutingModule { }
