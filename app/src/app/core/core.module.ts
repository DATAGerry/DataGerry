import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingPopupComponent } from './components/loading-popup/loading-popup.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { ObjectSelectorComponent } from './components/object_selector/object-selector.component';
import { FormsModule } from '@angular/forms';
import { WarningAlertComponent } from './components/warning-message/warning-alert.component';
import { ExtendableOptionManagerComponent } from './components/extendable_option_manager/extendable-option-manager.component';
import { FormInputComponent } from './components/base/input/form-input.component';
import { FormTextareaComponent } from './components/base/textarea/form-textarea.component';

@NgModule({
  declarations: [
    LoadingPopupComponent,
    ObjectSelectorComponent,
    WarningAlertComponent,
    ExtendableOptionManagerComponent,
    FormInputComponent,
    FormTextareaComponent
  ],
  imports: [
    CommonModule,
    NgSelectModule,
    FormsModule
  ],
  exports: [
    LoadingPopupComponent,
    ObjectSelectorComponent,
    WarningAlertComponent,
    ExtendableOptionManagerComponent,
    FormInputComponent,
    FormTextareaComponent
  ]
})
export class CoreModule { }