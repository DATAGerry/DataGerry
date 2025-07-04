import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AiPromptModalRoutingModule } from './ai-assistant-routing.module';
import { AiPromptModalComponent } from './components/ai-prompt-modal/ai-prompt-modal.component';
import { FormInputComponent } from '../core/components/base/input/form-input.component';
import { CoreModule } from '../core/core.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [AiPromptModalComponent],
  imports: [
    CommonModule,
    AiPromptModalRoutingModule,
    CoreModule,
    NgbModule,
    ReactiveFormsModule
  ],
  exports: [AiPromptModalComponent]
})
export class AiPromptModalModule { }