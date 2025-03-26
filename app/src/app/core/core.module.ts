import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingPopupComponent } from './components/loading-popup/loading-popup.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { ObjectSelectorComponent } from './components/object_selector/object-selector.component';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    LoadingPopupComponent,
    ObjectSelectorComponent

  ],
  imports: [
    CommonModule,
    NgSelectModule,
    FormsModule
  ],
  exports: [
    LoadingPopupComponent,
    ObjectSelectorComponent
  ]
})
export class CoreModule { }