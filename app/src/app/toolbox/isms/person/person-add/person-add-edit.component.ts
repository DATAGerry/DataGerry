import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { finalize } from 'rxjs/operators';

import { PersonService } from '../../services/person.service';
import { PersonGroupService } from '../../services/person-group.service';
import { CmdbPersonGroup } from '../../models/person-group.model';
import { CmdbPerson } from '../../models/person.model';

import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { SortDirection } from 'src/app/layout/table/table.types';

@Component({
  selector: 'app-person-add-edit',
  templateUrl: './person-add-edit.component.html',
  styleUrls: ['./person-add-edit.component.scss']
})
export class PersonAddEditComponent implements OnInit {
  public person: CmdbPerson;
  public allGroups: CmdbPersonGroup[] = [];
  public isEdit = false;
  public isView = false;
  public loading = false;

  constructor(
    private router: Router,
    private toast: ToastService,
    private loaderService: LoaderService,
    private personService: PersonService,
    private personGroupService: PersonGroupService
  ) {
    this.person = {
      first_name: '',
      last_name: '',
      phone_number: '',
      email: '',
      groups: []
    };
  }

  ngOnInit(): void {
    // If there's a 'person' object in navigation state => edit or view
    const navState = history.state;
    if (navState && navState.person) {
      this.person = { ...navState.person };
      this.isEdit = true;
    }
    if (navState && navState.mode === 'view') {
      this.isView = true;
    }

    this.loadGroups();
  }

  /**
   * Load Person Groups
   * - If isView => load only groups that belong to this person (filter)
   * - Otherwise => load all groups
   * @returns void
   */
  private loadGroups(): void {
    if (this.isView) {
      if (this.person.groups && this.person.groups.length > 0) {
        const filterObj = { public_id: { '$in': this.person.groups } };
        const params: CollectionParameters = {
          filter: JSON.stringify(filterObj),
          limit: 9999,
          page: 1,
          sort: 'public_id',
          order: SortDirection.ASCENDING
        };
        this.personGroupService.getPersonGroups(params)
          .subscribe({
            next: (resp) => {
              this.allGroups = resp.results;
            },
            error: (err) => {
              this.toast.error(err?.error?.message);
            }
          });
      } else {
        // no groups => do not call
        this.allGroups = [];
      }
    } else {
      // normal create/edit => fetch all
      const params: CollectionParameters = {
        filter: '',
        limit: 9999,
        page: 1,
        sort: 'public_id',
        order: SortDirection.ASCENDING
      };
      this.personGroupService.getPersonGroups(params)
        .subscribe({
          next: (resp) => {
            this.allGroups = resp.results;
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    }
  }

  /* 
  * Handlers for form fields 
  * @param newVal - The new value of the field
  * @returns void 
  */
  public onFirstNameChange(newVal: string): void {
    this.person.first_name = newVal;
    this.updateDisplayName();
  }


  /* 
  * Handlers for form fields
  * @param newVal - The new value of the field
  * @returns void
  */
  public onLastNameChange(newVal: string): void {
    this.person.last_name = newVal;
    this.updateDisplayName();
  }



  /**
   * Update display name based on first and last name
   * @returns void
   */
  private updateDisplayName(): void {
    // display_name = first_name + ' ' + last_name
    const fn = this.person.first_name || '';
    const ln = this.person.last_name || '';
    this.person.display_name = (fn + ' ' + ln).trim();
  }

  /*
  * Handlers for form fields
  * @param newVal - The new value of the field
  * @returns void
  */
  public onPhoneNumberChange(newVal: string): void {
    this.person.phone_number = newVal;
  }

  /*
  * Handlers for form fields
  * @param newVal - The new value of the field
  * @returns void
  */
  public onEmailChange(newVal: string): void {
    this.person.email = newVal;
  }

  /**
   * Handle changes in selected groups
   * @param selectedIds - Array of selected group IDs
   * @returns void
   */
  public onGroupsChange(selectedIds: number[]): void {
    this.person.groups = selectedIds;
  }

  /**
   * Save
   * @returns void
   */
  public onSave(): void {
    if (this.isView) {
      this.toast.info('Currently in view mode; no changes allowed.');
      return;
    }

    if (!this.person.first_name || !this.person.last_name) {
      this.toast.error('First Name and Last Name are required.');
      return;
    }

    this.loaderService.show();
    this.loading = true;

    if (this.isEdit && this.person.public_id) {
      // Update
      this.personService.updatePerson(this.person.public_id, this.person)
        .pipe(finalize(() => {
          this.loading = false;
          this.loaderService.hide();
        }))
        .subscribe({
          next: () => {
            this.toast.success('Person updated successfully.');
            this.router.navigate(['/isms/persons']);
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    } else {
      // Create
      this.personService.createPerson(this.person)
        .pipe(finalize(() => {
          this.loading = false;
          this.loaderService.hide();
        }))
        .subscribe({
          next: () => {
            this.toast.success('Person created successfully.');
            this.router.navigate(['/isms/persons']);
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    }
  }

  /**
   * Cancel
   * @returns void
   */
  public onCancel(): void {
    this.router.navigate(['/isms/persons']);
  }
}
