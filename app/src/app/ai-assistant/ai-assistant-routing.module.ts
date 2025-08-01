import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AiPromptPageComponent } from './components/ai-prompt-page/ai-prompt-page.component';

const routes: Routes = [
  { path: 'ai-assistant', component: AiPromptPageComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AiAssistantRoutingModule { }
