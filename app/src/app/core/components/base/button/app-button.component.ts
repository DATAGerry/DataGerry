import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './app-button.component.html',
  styleUrls: ['./app-button.component.scss']
})
export class ButtonComponent {
  /**
   * Text shown on the button.
   */
  @Input() label: string = 'Button';

  /**
   * Set the HTML button type: 'submit', 'button', or 'reset'.
   * Default is 'button'.
   */
  @Input() type: 'button' | 'submit' | 'reset' = 'button';

  /**
   * Pass in any Bootstrap class(es) you like, e.g. 'btn-success', 'btn-secondary mr-2'.
   * This will be applied along with the default 'btn' class.
   */
  @Input() bootstrapClass: string = 'btn-secondary';

  /**
   * If true, button is disabled.
   */
  @Input() disabled: boolean = false;

  /**
   * Emitted when the button is clicked (unless disabled).
   */
  @Output() clicked = new EventEmitter<void>();

  onClick(): void {
    if (!this.disabled) {
      this.clicked.emit();
    }
  }
}
