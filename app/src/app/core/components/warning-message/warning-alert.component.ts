import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-warning-alert',
  templateUrl: './warning-alert.component.html',
  styleUrls: ['./warning-alert.component.scss']
})
export class WarningAlertComponent {
  @Input() iconClass: string = 'fas fa-exclamation-circle';
  @Input() title: string = 'Warning:';
  @Input() message: string = '';
}
