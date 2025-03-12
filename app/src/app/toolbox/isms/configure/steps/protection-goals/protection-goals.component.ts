import { Component, Input, OnInit } from '@angular/core';
import { IsmsConfig } from '../../../models/isms-config.model';

@Component({
  selector: 'app-isms-protection-goals',
  templateUrl: './protection-goals.component.html',
  styleUrls: ['./protection-goals.component.scss']
})
export class ProtectionGoalsComponent implements OnInit {
    @Input() config: IsmsConfig;

  constructor() { }

  ngOnInit(): void {
    // Load existing protection goals, add logic for user-defined goals
  }
}
