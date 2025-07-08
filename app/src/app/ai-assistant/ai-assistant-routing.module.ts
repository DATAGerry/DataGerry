import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AiPromptModalComponent } from './components/ai-prompt-modal/ai-prompt-modal.component';

const routes: Routes = [
  { path: 'ai-assistant', component: AiPromptModalComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AiPromptModalRoutingModule { }