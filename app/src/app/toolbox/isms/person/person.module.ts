import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TableModule } from 'src/app/layout/table/table.module';
import { AuthModule } from 'src/app/modules/auth/auth.module';
import { CoreModule } from 'src/app/core/core.module';
import { ReactiveFormsModule } from '@angular/forms';
import { PersonRoutingModule } from './person-routing.module';
import { PersonAddEditComponent } from './person-add/person-add-edit.component';
import { PersonListComponent } from './person-list/person-list.component';

@NgModule({
  declarations: [
    PersonAddEditComponent,
    PersonListComponent
  ],
  imports: [
    CommonModule,
    PersonRoutingModule,
    TableModule,
    AuthModule,
    CoreModule,
    ReactiveFormsModule
  ]
})
export class PersonModule { }
