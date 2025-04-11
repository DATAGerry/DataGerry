import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { LoaderService } from 'src/app/core/services/loader.service';
import { finalize } from 'rxjs/operators';

import { PersonGroupService } from 'src/app/toolbox/isms/services/person-group.service';
import { PersonService } from 'src/app/toolbox/isms/services/person.service';
import { CmdbPersonGroup } from 'src/app/toolbox/isms/models/person-group.model';
import { CmdbPerson } from 'src/app/toolbox/isms/models/person.model';

import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { SortDirection } from 'src/app/layout/table/table.types';

@Component({
  selector: 'app-person-group-add-edit',
  templateUrl: './person-group-add-edit.component.html',
  styleUrls: ['./person-group-add-edit.component.scss']
})
export class PersonGroupAddEditComponent implements OnInit {
  public personGroup: CmdbPersonGroup;
  public isEdit = false;
  public isView = false; // If true => read-only mode
  public loading = false;
  public allPersons: CmdbPerson[] = [];

  
  constructor(
    private router: Router,
    private toast: ToastService,
    private loaderService: LoaderService,
    private personGroupService: PersonGroupService,
    private personService: PersonService
  ) {
    this.personGroup = {
      name: '',
      email: '',
      group_members: []
    };
  }


  ngOnInit(): void {
    const navState = history.state;

    // Check if an existing record was passed for edit/view
    if (navState && navState.personGroup) {
      this.personGroup = { ...navState.personGroup };
      this.isEdit = true; // We have an existing record
    }
    if (navState && navState.mode === 'view') {
      this.isView = true; // If user clicked "View"
      // isEdit can remain true or false, but typically we won't save if view only
    }

    this.loadPersons();
  }


  /**
   * Load persons
   * @returns void
   */
  private loadPersons(): void {
    if (this.isView) {
      // If we are just "viewing," only load the members' Person records
      if (this.personGroup.group_members && this.personGroup.group_members.length > 0) {
        const filterObj = { public_id: { '$in': this.personGroup.group_members } };
        const params: CollectionParameters = {
          filter: JSON.stringify(filterObj),
          limit: 9999,
          page: 1,
          sort: 'public_id',
          order: SortDirection.ASCENDING
        };
        this.personService.getPersons(params).subscribe({
          next: (resp) => {
            this.allPersons = resp.results;
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
      } else {
        // No members => do not call API
        this.allPersons = [];
      }
    } else {
      // Normal create/edit => fetch all possible persons
      const params: CollectionParameters = {
        filter: '',
        limit: 9999,
        page: 1,
        sort: 'public_id',
        order: SortDirection.ASCENDING
      };
      this.personService.getPersons(params).subscribe({
        next: (resp) => {
          this.allPersons = resp.results;
        },
        error: (err) => {
          this.toast.error(err?.error?.message);
        }
      });
    }
  }


  /**
   * Handle changes to the name and email fields
   * @param newVal - The new value for the field
   * @returns void
   */
  public onNameChange(newVal: string): void {
    this.personGroup.name = newVal;
  }


  /**
   * Handle changes to the email field
   * @param newVal - The new value for the field
   * @returns void
   */
  public onEmailChange(newVal: string): void {
    this.personGroup.email = newVal;
  }


  /**
   * Handle changes to the group members
   * @param selectedIds - The IDs of the selected members
   * @returns void
   */
  public onMembersChange(selectedIds: number[]): void {
    this.personGroup.group_members = selectedIds;
  }


  /**
   * Save logic
   * @returns void
   */
  public onSave(): void {
    // If in "view" mode => do nothing, or you can skip the save
    if (this.isView) {
      this.toast.info('Currently in view mode; no changes allowed.');
      return;
    }

    if (!this.personGroup.name) {
      this.toast.error('Name is required.');
      return;
    }

    this.loaderService.show();
    this.loading = true;

    if (this.isEdit && this.personGroup.public_id) {
      // Update
      const id = this.personGroup.public_id;
      this.personGroupService.updatePersonGroup(id, this.personGroup)
        .pipe(finalize(() => {
          this.loading = false;
          this.loaderService.hide();
        }))
        .subscribe({
          next: () => {
            this.toast.success('Person Group updated successfully.');
            this.router.navigate(['/framework/person-groups']);
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    } else {
      // Create
      this.personGroupService.createPersonGroup(this.personGroup)
        .pipe(finalize(() => {
          this.loading = false;
          this.loaderService.hide();
        }))
        .subscribe({
          next: () => {
            this.toast.success('Person Group created successfully.');
            this.router.navigate(['/framework/person-groups']);
          },
          error: (err) => {
            this.toast.error(err?.error?.message);
          }
        });
    }
  }


  /**
    * Cancel logic
    * @returns void
   */
  public onCancel(): void {
    this.router.navigate(['/framework/person-groups']);
  }
}
