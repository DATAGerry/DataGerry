/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2025 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ISMSService } from '../services/isms.service';
import { IsmsConfigValidation } from '../models/isms-config-validation.model';
import { LoaderService } from 'src/app/core/services/loader.service';
import { finalize } from 'rxjs';
import { ToastService } from 'src/app/layout/toast/toast.service';

@Component({
  selector: 'app-isms-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  public validationStatus: boolean = false;
  public isLoading$ = this.loaderService.isLoading$;


  public cards = [
    {
      title: 'Configure ISMS Settings',
      icon: 'fas fa-cogs',
      link: '/isms/configure',
      validationStatus: false
    },
    {
      title: 'Risks',
      icon: 'fas fa-exclamation-triangle',
      link: '/isms/risks'
    },
    {
      title: 'Control/Measures',
      icon: 'fas fa-shield-alt',
      link: '/isms/control-measures'
    },
    {
      title: 'Threats',
      icon: 'fas fa-bolt',
      link: '/isms/threats'
    },
    {
      title: 'Vulnerabilities',
      icon: 'fas fa-bug',
      link: '/isms/vulnerabilities'
    },

    {
      title: 'Persons',
      icon: 'fas fa-user-friends',
      link: '/isms/persons'
    },

    {
      title: 'Person Groups',
      icon: 'fas fa-users',
      link: '/framework/person-groups'
    },

    {
      title: 'Risk Matrix Report',
      icon: 'fas fa-table',
      link: '/isms/reports/risk_matrix'
    },

    {
      title: 'SOA Report',
      icon: 'fas fa-table',
      link: '/isms/reports/soa'
    },

    {
      title: 'Risk treatment plan',
      icon: 'fas fa-table',
      link: '/isms/reports/risk_treatment_plan'
    },

    {
      title: 'Risk Assesments',
      icon: 'fas fa-table',
      link: '/isms/reports/risk_assesments'
    },
  ];


  constructor(private ismsService: ISMSService,
    private cdRef: ChangeDetectorRef,
    private loaderService: LoaderService,
    private toastService: ToastService,

  ) { }

  ngOnInit(): void {
    this.loaderService.show(); // Show loader
    this.ismsService.getIsmsValidationStatus().subscribe({
      next: (status: IsmsConfigValidation) => {
        const isValid =
          status.risk_classes &&
          status.likelihoods &&
          status.impacts &&
          status.impact_categories &&
          status.risk_matrix;

        this.cards.forEach(card => {
          if (card.hasOwnProperty('validationStatus')) {
            card.validationStatus = isValid;
          }
        });

        // Trigger change detection
        this.cdRef.detectChanges();
      },
      error: (err) => {
        this.toastService.error(err?.error?.message)
      },
      complete: () => {
        this.loaderService.hide(); // Hide loader
      }
    });
  }

}
