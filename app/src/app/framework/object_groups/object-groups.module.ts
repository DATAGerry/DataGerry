import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';

import { ObjectGroupsRoutingModule } from './object-groups-routing.module';
import { ObjectGroupsListComponent } from './object-groups-list.component';
import { ObjectGroupsAddComponent } from './add/object-groups-add.component';
import { TableModule } from 'src/app/layout/table/table.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { CoreModule } from 'src/app/core/core.module';
import { CategoryManagerComponent } from './modal/category-manager.component';

@NgModule({
  declarations: [
    ObjectGroupsListComponent,
    ObjectGroupsAddComponent,
    CategoryManagerComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    NgSelectModule,
    ObjectGroupsRoutingModule,
    TableModule,
    AuthModule,
    CoreModule  ]
})
export class ObjectGroupsModule { }
