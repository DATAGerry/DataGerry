import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PersonGroupRoutingModule } from './person-group-routing.module';

import { PersonGroupListComponent } from './person-group-list/person-group-list.component';
import { PersonGroupAddEditComponent } from './person-group-add/person-group-add-edit.component';
import { TableModule } from 'src/app/layout/table/table.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { CoreModule } from 'src/app/core/core.module';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    PersonGroupListComponent,
    PersonGroupAddEditComponent
  ],
  imports: [
    CommonModule,
    PersonGroupRoutingModule,
    TableModule,
    AuthModule,
    CoreModule,
    ReactiveFormsModule
  ]
})
export class PersonGroupModule { }
