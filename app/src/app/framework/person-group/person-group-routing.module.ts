import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { PersonGroupListComponent } from './person-group-list/person-group-list.component';
import { PersonGroupAddEditComponent } from './person-group-add/person-group-add-edit.component';

const routes: Routes = [
  { path: '', component: PersonGroupListComponent },
  { path: 'add', component: PersonGroupAddEditComponent },
  { path: 'edit', component: PersonGroupAddEditComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PersonGroupRoutingModule {}
