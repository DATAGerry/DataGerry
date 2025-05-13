import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ObjectGroupsListComponent } from './object-groups-list.component';
import { ObjectGroupsAddComponent } from './add/object-groups-add.component';
import { preCloudGuard } from 'src/app/modules/auth/guards/pre-cloud.guard';

const routes: Routes = [
  { path: '', component: ObjectGroupsListComponent, canActivate: [preCloudGuard]},
  { path: 'add', component: ObjectGroupsAddComponent, canActivate: [preCloudGuard] },
  { path: 'edit/:id', component: ObjectGroupsAddComponent, canActivate: [preCloudGuard] },
  {path: 'view/:id', component: ObjectGroupsAddComponent, canActivate: [preCloudGuard] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ObjectGroupsRoutingModule {}
