import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ObjectGroupsListComponent } from './object-groups-list.component';
import { ObjectGroupsAddComponent } from './add/object-groups-add.component';

const routes: Routes = [
  { path: '', component: ObjectGroupsListComponent},
  { path: 'add', component: ObjectGroupsAddComponent, },
  { path: 'edit/:id', component: ObjectGroupsAddComponent,  },
  {path: 'view/:id', component: ObjectGroupsAddComponent, }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ObjectGroupsRoutingModule {}
