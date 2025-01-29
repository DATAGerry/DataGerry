import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingPopupComponent } from './components/loading-popup/loading-popup.component';

@NgModule({
  declarations: [
    LoadingPopupComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    LoadingPopupComponent
  ]
})
export class CoreModule {}