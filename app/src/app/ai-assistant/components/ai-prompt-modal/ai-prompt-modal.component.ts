import { Component, OnInit } from "@angular/core";
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AiAssistantService } from 'src/app/ai-assistant/services/ai-assistant.service';

@Component({
  selector: 'cmdb-ai-prompt-modal',
  templateUrl: './ai-prompt-modal.component.html',
  styleUrls: ['./ai-prompt-modal.component.scss']
})
export class AiPromptModalComponent implements OnInit {
  public promptForm!: FormGroup;

  constructor(
    public modal: NgbActiveModal,
    private aiAssistantService: AiAssistantService
  ) { }

  ngOnInit(): void {
    this.promptForm = new FormGroup({
      prompt: new FormControl('', Validators.required)
    });
  }

  public submit(): void {
    if (this.promptForm.valid) {
      const message = this.promptForm.get('prompt')?.value;
      this.aiAssistantService.postMessage(message).subscribe({
        next: (response) => {
          // Pass API response on modal close
          this.modal.close(response);
        },
        error: (error) => {
          console.error('Error posting AI message:', error);
        }
      });
    }
  }

  public cancel(): void {
    this.modal.dismiss('cancel');
  }
}