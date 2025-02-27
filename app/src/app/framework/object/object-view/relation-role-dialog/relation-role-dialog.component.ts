// import {
//   ChangeDetectorRef,
//   Component,
//   EventEmitter,
//   Input,
//   OnDestroy,
//   OnInit,
//   Output
// } from '@angular/core';
// import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
// import { Subject } from 'rxjs';
// import { takeUntil } from 'rxjs/operators';

// import { ObjectService } from 'src/app/framework/services/object.service';
// import { ToastService } from 'src/app/layout/toast/toast.service';

// import { CmdbMode } from 'src/app/framework/modes.enum';
// import { CmdbRelation } from 'src/app/framework/models/relation.model';

// /** Just adapt to your real object structure. */
// type ObjectType = any;

// /** Each option in the dropdown must have these fields. */
// interface FlatOptionItem {
//   value: number;
//   label: string;
//   group: string; // e.g. "Company [2]"
// }

// @Component({
//   selector: 'relation-role-dialog',
//   templateUrl: './relation-role-dialog.component.html',
//   styleUrls: ['./relation-role-dialog.component.scss']
// })
// export class RelationRoleDialogComponent implements OnInit, OnDestroy {
//   @Input() chosenRole!: 'parent' | 'child';
//   @Input() parentTypeIDs: number[] = [];
//   @Input() childTypeIDs: number[] = [];
//   @Input() currentObjectID!: number;

//   /**
//    * The chosen relation that contains .sections and .fields,
//    * e.g.:
//    * {
//    *   public_id: 1005,
//    *   relation_name: 'network',
//    *   sections: [...],
//    *   fields: [...]
//    *   ...
//    * }
//    */
//   @Input() relation: CmdbRelation | null = null;

//   @Output() onConfirm = new EventEmitter<{ parentObjID: number; childObjID: number; relationData?: any }>();
//   @Output() onCancel = new EventEmitter<void>();

//   /** The form for the parent/child dropdown. */
//   public form: FormGroup;

//   /** The form for relation fields. */
//   public relationForm: FormGroup;

//   /** So we can loop easily in the template. */
//   public sections: any[] = [];

//   // The arrays used by ng-select
//   public flatParentOptions: FlatOptionItem[] = [];
//   public flatChildOptions: FlatOptionItem[] = [];

//   public loading = false;
//   private destroy$ = new Subject<void>();

//   /** For using in the template if needed */
//   public CmdbMode = CmdbMode;

//   constructor(
//     private fb: FormBuilder,
//     private objectService: ObjectService,
//     private toastService: ToastService,
//   ) {
//     // 1) Dropdown form
//     this.form = this.fb.group({
//       parent: [{ value: null, disabled: false }],
//       child:  [{ value: null, disabled: false }]
//     });

//     // 2) Relation fields form
//     this.relationForm = this.fb.group({});
//   }

//   ngOnInit(): void {
//     console.log('[RelationRoleDialog] OnInit ->', {
//       chosenRole: this.chosenRole,
//       parentTypeIDs: this.parentTypeIDs,
//       childTypeIDs: this.childTypeIDs,
//       currentObjectID: this.currentObjectID,
//       relation: this.relation
//     });

//     // 1) Set up the dropdown form
//     this.initializeForm();
//     this.loadOptions();

//     // 2) Extract relation sections for easy looping
//     if (this.relation?.sections) {
//       this.sections = this.relation.sections;
//     }
//   }

//   ngOnDestroy(): void {
//     this.destroy$.next();
//     this.destroy$.complete();
//   }

//   /**
//    * If chosenRole == 'parent', disable 'parent' (pre-set to currentObjectID).
//    * If chosenRole == 'child', disable 'child' (pre-set to currentObjectID).
//    */
//   private initializeForm(): void {
//     if (this.chosenRole === 'parent') {
//       this.form.get('parent')?.setValue(this.currentObjectID);
//       this.form.get('parent')?.disable();
//       this.form.get('child')?.enable();
//     } else {
//       this.form.get('child')?.setValue(this.currentObjectID);
//       this.form.get('child')?.disable();
//       this.form.get('parent')?.enable();
//     }
//   }

//   /** Decide whether to load child or parent options for the dropdown. */
//   private loadOptions(): void {
//     if (this.chosenRole === 'parent') {
//       this.loadChildOptions();
//     } else {
//       this.loadParentOptions();
//     }
//   }

//   /** Load possible "parent" objects. */
//   private loadParentOptions(): void {
//     const validTypeIDs = this.validateTypeIDs(this.parentTypeIDs);
//     console.log('[Parent] validTypeIDs ->', validTypeIDs);

//     if (!validTypeIDs.length) {
//       this.toastService.warning('Invalid parent type configuration');
//       return;
//     }

//     this.loading = true;
//     this.objectService.getObjectsByType(validTypeIDs)
//       .pipe(takeUntil(this.destroy$))
//       .subscribe({
//         next: (results: any[]) => {
//           console.log('[Parent] API Results ->', results);
//           this.flatParentOptions = this.buildFlatOptions(results);
//           console.log('[Parent] final flatParentOptions ->', this.flatParentOptions);

//           this.loading = false;
//           // Force change detection so that ng-select sees the new data
//           // this.cdRef.detectChanges();
//         },
//         error: (err) => {
//           console.error('Parent Load Error:', err);
//           this.loading = false;
//         }
//       });
//   }

//   /** Load possible "child" objects. */
//   private loadChildOptions(): void {
//     const validTypeIDs = this.validateTypeIDs(this.childTypeIDs);
//     console.log('[Child] validTypeIDs ->', validTypeIDs);

//     if (!validTypeIDs.length) {
//       this.toastService.warning('Invalid child type configuration');
//       return;
//     }

//     this.loading = true;
//     this.objectService.getObjectsByType(validTypeIDs)
//       .pipe(takeUntil(this.destroy$))
//       .subscribe({
//         next: (results: any[]) => {
//           console.log('[Child] API Results ->', results);
//           this.flatChildOptions = this.buildFlatOptions(results);
//           console.log('[Child] final flatChildOptions ->', this.flatChildOptions);

//           this.loading = false;
//           // // Force change detection
//           // this.cdRef.detectChanges();
//         },
//         error: (err) => {
//           console.error('Child Load Error:', err);
//           this.loading = false;
//         }
//       });
//   }

//   /** Flatten and parse the type ID arrays. */
//   private validateTypeIDs(ids: any[]): number[] {
//     return ids.flat(Infinity).filter((id: any) => Number.isInteger(id) && id > 0);
//   }

//   /**
//    * Build an array with `group` string for ng-select grouping.
//    * Adjust this logic as needed based on your actual data structure.
//    */
//   private buildFlatOptions(results: any[]): FlatOptionItem[] {
//     if (!Array.isArray(results) || results.length === 0) {
//       console.warn('No results, returning fallback example for debugging grouping...');
//       // return [
//       //   { value: 3,  label: 'Company #3 becon | fulda', group: 'Company [2]' },
//       //   { value: 6,  label: 'Company #6 sasas |',       group: 'Company [2]' },
//       //   { value: 11, label: 'Country #11',             group: 'Country [1]' },
//       //   { value: 10, label: 'dsd #10 dsd #10',          group: 'dsd [1]' },
//       //   { value: 12, label: 'User #12  |',             group: 'User [1]' }
//       // ];
//     }

//     // Build a map: typeId -> { label, count }
//     const typeMap: Record<number, { label: string; count: number }> = {};
//     for (const obj of results) {
//       const tId = this.getTypeID(obj);
//       const tLabel = this.getTypeLabel(obj) || '(no label)';
//       if (!typeMap[tId]) {
//         typeMap[tId] = { label: tLabel, count: 0 };
//       }
//       typeMap[tId].count++;
//     }

//     // Transform each item into { value, label, group }
//     const flat: FlatOptionItem[] = results.map(obj => {
//       const tId = this.getTypeID(obj);
//       const { label: tLabel, count } = typeMap[tId];
//       const groupLabel = `${tLabel} [${count}]`;

//       const objectId = this.getObjectID(obj);
//       const summary  = this.getSummary(obj);
//       const itemLabel = summary ? `${tLabel} #${objectId} ${summary}` : `${tLabel} #${objectId}`;

//       return {
//         value: objectId,
//         label: itemLabel.trim(),
//         group: groupLabel
//       };
//     });

//     // Sort by group
//     flat.sort((a, b) => a.group.localeCompare(b.group));
//     return flat;
//   }

//   private getTypeID(obj: any): number {
//     return obj?.type_information?.type_id
//       ?? obj?.type_id
//       ?? 0;
//   }

//   private getObjectID(obj: any): number {
//     return obj?.object_information?.object_id
//       ?? obj?.public_id
//       ?? 0;
//   }

//   private getSummary(obj: any): string {
//     return obj?.summary_line ?? '';
//   }

//   private getTypeLabel(obj: any): string {
//     return obj?.type_information?.type_label
//       ?? ('Type ' + (obj?.type_id ?? 'Unknown'));
//   }


//   public getFieldObject(fieldName: string) {
//     // Return the matching field object from this.relation.fields
//     return this.relation?.fields?.find((f) => f.name === fieldName);
//   }

  
//   /**
//    * Final confirmation.
//    * If chosenRole == 'parent', the parent is currentObjectID,
//    * else we read from form.value.parent, etc.
//    * Also gather the dynamic relationForm values.
//    */
//   confirm(): void {
//     const parentObjID = (this.chosenRole === 'parent')
//       ? this.currentObjectID
//       : this.form.value.parent;

//     const childObjID = (this.chosenRole === 'child')
//       ? this.currentObjectID
//       : this.form.value.child;

//     // All dynamic fields from the relation
//     const relationData = this.relationForm.value;

//     console.log('[RelationRoleDialog] confirm ->', {
//       parentObjID,
//       childObjID,
//       relationData
//     });

//     // Emit them upwards
//     this.onConfirm.emit({ parentObjID, childObjID, relationData });
//   }

//   cancel(): void {
//     console.log('[RelationRoleDialog] cancel');
//     this.onCancel.emit();
//   }

//   // For the <cmdb-render-element> 'mode'
//   // Adjust to your real logic (Create, Edit, etc.)
//   getViewMode() {
//     return CmdbMode.Edit;
//   }
// }



import {
  Component,
  Input,
  Output,
  EventEmitter,
  OnInit,
  OnDestroy
} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';

import { CmdbMode } from 'src/app/framework/modes.enum';
import { ObjectService } from 'src/app/framework/services/object.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

import { CmdbRelation } from 'src/app/framework/models/relation.model';
import { ObjectRelationService, CmdbObjectRelationCreateDto } from 'src/app/framework/services/object-relation.service';


/** For the dropdown items */
interface FlatOptionItem {
  value: number;   // the numeric ID
  label: string;
  group: string;
}

@Component({
  selector: 'relation-role-dialog',
  templateUrl: './relation-role-dialog.component.html',
  styleUrls: ['./relation-role-dialog.component.scss']
})
export class RelationRoleDialogComponent implements OnInit, OnDestroy {
  /**
   * E.g. "parent" means the currentObjectID is the parent,
   * so the user will pick the child from the dropdown.
   */
  @Input() chosenRole!: 'parent' | 'child';

  /** 
   * The type IDs that are valid for "parent" 
   * or for "child" 
   */
  @Input() parentTypeIDs: number[] = [];
  @Input() childTypeIDs: number[] = [];

  /** 
   * The ID of the object from your object-view. 
   * e.g. if user is editing "Object #10," 
   * you pass in 10 as currentObjectID.
   */
  @Input() currentObjectID!: number;

  /**
   * The chosen relation definition: 
   *  - .public_id (the "relation_id")
   *  - .sections: array of { label, fields: [fieldNames] }
   *  - .fields: array of { name, type, label, ... }
   */
  @Input() relation: CmdbRelation | null = null;

  /**
   * Fires when the user finishes, returning 
   * { parentObjID, childObjID, relationData }
   */
  @Output() onConfirm = new EventEmitter<{
    parentObjID: number;
    childObjID: number;
    relationData?: any;
  }>();

  /**
   * Fires when the user cancels
   */
  @Output() onCancel = new EventEmitter<void>();

  /** The form for parent/child dropdown. */
  public form: FormGroup;

  /** The form for dynamic relation fields. */
  public relationForm: FormGroup;

  /** We'll loop over `relation.sections` in the template. */
  public sections: any[] = [];

  // The arrays used by ng-select
  public flatParentOptions: FlatOptionItem[] = [];
  public flatChildOptions: FlatOptionItem[] = [];

  public CmdbMode = CmdbMode;
  public loading = false;

  private destroy$ = new Subject<void>();

  constructor(
    private fb: FormBuilder,
    private objectService: ObjectService,
    private toastService: ToastService,
    private objectRelationService: ObjectRelationService
  ) {
    // 1) Parent/Child dropdown form
    this.form = this.fb.group({
      parent: [null],
      child: [null]
    });

    // 2) Relation fields form
    this.relationForm = this.fb.group({});
  }

  ngOnInit(): void {
    console.log('[RelationRoleDialog] OnInit =>', {
      chosenRole: this.chosenRole,
      parentTypeIDs: this.parentTypeIDs,
      childTypeIDs: this.childTypeIDs,
      currentObjectID: this.currentObjectID,
      relation: this.relation
    });

    // Setup which side is fixed to currentObjectID, which side is open to choose
    this.setupDropdownForm();

    // Load the relevant dropdown data
    this.loadOptions();

    // If there's a chosen relation, set up the sections
    if (this.relation?.sections) {
      this.sections = this.relation.sections;
    }
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * If chosenRole === 'parent', disable the "parent" field 
   * and set it to currentObjectID; child is open for selection.
   * Vice versa for 'child'.
   */
  private setupDropdownForm(): void {
    if (this.chosenRole === 'parent') {
      this.form.get('parent')?.setValue(this.currentObjectID);
      this.form.get('parent')?.disable();
      this.form.get('child')?.enable();
    } else {
      this.form.get('child')?.setValue(this.currentObjectID);
      this.form.get('child')?.disable();
      this.form.get('parent')?.enable();
    }
  }

  /** 
   * Based on chosenRole, load either child or parent objects.
   */
  private loadOptions(): void {
    if (this.chosenRole === 'parent') {
      this.loadChildOptions();
    } else {
      this.loadParentOptions();
    }
  }

  private loadParentOptions(): void {
    const validTypeIDs = this.validateTypeIDs(this.parentTypeIDs);
    if (!validTypeIDs.length) {
      this.toastService.warning('No valid parent type configuration');
      return;
    }

    this.loading = true;
    this.objectService.getObjectsByType(validTypeIDs)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (results: any[]) => {
          // Filter out the "currentObjectID"
          // so we don't show it in the counterpart dropdown
          const filtered = results.filter(
            obj => this.getObjectID(obj) !== this.currentObjectID
          );

          this.flatParentOptions = this.buildFlatOptions(filtered);
          this.loading = false;
        },
        error: err => {
          console.error('Parent load error:', err);
          this.loading = false;
        }
      });
  }

  private loadChildOptions(): void {
    const validTypeIDs = this.validateTypeIDs(this.childTypeIDs);
    if (!validTypeIDs.length) {
      this.toastService.warning('No valid child type configuration');
      return;
    }

    this.loading = true;
    this.objectService.getObjectsByType(validTypeIDs)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (results: any[]) => {
          // Filter out the "currentObjectID" from the child side
          const filtered = results.filter(
            obj => this.getObjectID(obj) !== this.currentObjectID
          );

          this.flatChildOptions = this.buildFlatOptions(filtered);
          this.loading = false;
        },
        error: err => {
          console.error('Child load error:', err);
          this.loading = false;
        }
      });
  }

  private validateTypeIDs(ids: any[]): number[] {
    // Flatten deeply, keep only positive integers
    return ids.flat(Infinity).filter((id: any) => Number.isInteger(id) && id > 0);
  }

  /**
   * Transforms API results => FlatOptionItem[] for ng-select,
   * grouping them by typeLabel [count].
   */
  private buildFlatOptions(results: any[]): FlatOptionItem[] {
    if (!Array.isArray(results) || results.length === 0) {
      return [];
    }

    // Map typeId => { label, count }
    const typeMap: Record<number, { label: string; count: number }> = {};

    for (const obj of results) {
      const tId = this.getTypeID(obj);
      const tLabel = this.getTypeLabel(obj) || '(no label)';
      if (!typeMap[tId]) {
        typeMap[tId] = { label: tLabel, count: 0 };
      }
      typeMap[tId].count++;
    }

    // Build final array
    const flat: FlatOptionItem[] = results.map(obj => {
      const tId = this.getTypeID(obj);
      const { label: tLabel, count } = typeMap[tId];
      const groupLabel = `${tLabel} [${count}]`;

      const objectId = this.getObjectID(obj);
      const summary = this.getSummary(obj);
      const itemLabel = summary
        ? `${tLabel} #${objectId} ${summary}`
        : `${tLabel} #${objectId}`;

      return {
        value: objectId,
        label: itemLabel.trim(),
        group: groupLabel
      };
    });

    flat.sort((a, b) => a.group.localeCompare(b.group));
    return flat;
  }

  /** Looks up the actual field object in .relation.fields by name */
  public getFieldObject(fieldName: string) {
    return this.relation?.fields?.find((f) => f.name === fieldName);
  }

  /** For your existing structure */
  private getTypeID(obj: any): number {
    return obj?.type_information?.type_id ?? obj?.type_id ?? 0;
  }
  private getObjectID(obj: any): number {
    return obj?.object_information?.object_id ?? obj?.public_id ?? 0;
  }
  private getSummary(obj: any): string {
    return obj?.summary_line ?? '';
  }
  private getTypeLabel(obj: any): string {
    return obj?.type_information?.type_label ?? (`Type ` + (obj?.type_id ?? 'Unknown'));
  }

  // For <cmdb-render-element>, we want an edit or create mode
  public getViewMode() {
    return CmdbMode.Edit;
  }

  /**
   * On Confirm => 
   * 1) figure out final parent/child IDs 
   * 2) build the field_values array 
   * 3) call /object_relations
   */
  confirm(): void {
    // If chosenRole == 'parent', the parent is currentObjectID,
    // else we read from form.value.parent
    const parentObjID = (this.chosenRole === 'parent')
      ? this.currentObjectID
      : this.form.value.parent;

    // If chosenRole == 'child', the child is currentObjectID,
    // else from form.value.child
    const childObjID = (this.chosenRole === 'child')
      ? this.currentObjectID
      : this.form.value.child;

    // Gather the user-entered fields
    const formValue = this.relationForm.value; 
    // Convert { key: val, ... } => [{ name, value }, ...]
    const field_values = Object.entries(formValue).map(([key, val]) => ({
      name: key,
      value: val
    }));

    // Build the final request body
    const dto: CmdbObjectRelationCreateDto = {
      relation_id: this.relation.public_id,
      relation_parent_id: parentObjID,
      relation_child_id: childObjID,
      field_values
    };

    console.log('[RelationRoleDialog] confirm => Final payload:', dto);

    // POST /object_relations
    this.objectRelationService.postObjectRelation(dto).subscribe({
      next: (res) => {
        this.toastService.success(
          `Relation created successfully: parent=${parentObjID}, child=${childObjID}`
        );
        // Also emit if parent component wants to do something
        this.onConfirm.emit({ parentObjID, childObjID, relationData: res });
      },
      error: (err) => {
        console.error('Create relation failed:', err);
        this.toastService.error(err?.error?.message || 'Failed to create relation');
      }
    });
  }

  cancel(): void {
    this.onCancel.emit();
  }
}
