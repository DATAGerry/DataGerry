// ai-assistant.module.ts (or AiPromptModalModule if you're keeping that name)
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AiAssistantRoutingModule } from './ai-assistant-routing.module';
import { AiPromptPageComponent } from './components/ai-prompt-page/ai-prompt-page.component'; // ✅
import { CoreModule } from '../core/core.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AiPromptPageComponent 
  ],
  imports: [
    CommonModule,
    AiAssistantRoutingModule,
    CoreModule, 
    NgbModule,
    ReactiveFormsModule
  ]
})
export class AiAssistantModule { } 
