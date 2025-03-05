import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  HostListener,
  OnDestroy,
  OnInit,
  TemplateRef,
  ViewChild
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject, Subject, takeUntil, forkJoin, switchMap, map } from 'rxjs';
import { CmdbMode } from 'src/app/framework/modes.enum';
import { ObjectService } from 'src/app/framework/services/object.service';
import { ObjectRelationService } from 'src/app/framework/services/object-relation.service';
import { TypeService } from 'src/app/framework/services/type.service';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { RenderResult } from 'src/app/framework/models/cmdb-render';
import { CmdbRelation } from 'src/app/framework/models/relation.model';
import { RelationService } from '../../services/relaion.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CoreDeleteConfirmationModalComponent } from 'src/app/core/components/dialog/delete-dialog/core-delete-confirmation-modal.component';

// Interface for ExtendedRelation used in relation selection modal
interface ExtendedRelation extends CmdbRelation {
  canBeParent: boolean;
  canBeChild: boolean;
}

// Interface for raw relation instances from the API
interface ObjectRelationInstance {
  public_id: number;
  relation_id: number;
  relation_parent_id: number;
  relation_child_id: number;
  field_values: Array<{ name: string; value: any }>;
  definition?: CmdbRelation;
}

// Extended interface for table data
interface ExtendedObjectRelationInstance extends ObjectRelationInstance {
  counterpart_id: number;
  type: string;
}

// Interface for grouped relation instances under each tab
interface RelationGroup {
  relationId: number;
  isParent: boolean;
  tabLabel: string;
  tabColor: string;
  tabIcon: string;
  instances: ExtendedObjectRelationInstance[];
  total: number;    // total number of items for this group
  page?: number;     // current page for this group
  pageSize?: number; // items per page for this group
}




@Component({
  selector: 'cmdb-object-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ObjectViewComponent implements OnInit, OnDestroy, AfterViewInit {

  // Table templates
  @ViewChild('counterpartIdTemplate', { static: true }) counterpartIdTemplate: TemplateRef<any>;
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate: TemplateRef<any>;

  public mode: CmdbMode = CmdbMode.View;
  public renderResult: RenderResult;
  public currentObjectID: number;
  private unsubscribe = new Subject<void>();
  private objectViewSubject = new BehaviorSubject<RenderResult>(undefined);

  // Modal and loading states
  public showRelationModal = false;
  public loadingRelations = false;
  public showRelationRoleDialog = false;

  // Relation selection properties
  public availableRelations: CmdbRelation[] = [];
  public extendedRelations: ExtendedRelation[] = [];
  public chosenRelation: ExtendedRelation = null;
  public chosenRole: 'parent' | 'child' = null;
  public roleParentTypeIDs: number[] = [];
  public roleChildTypeIDs: number[] = [];

  // Tab management
  public relationGroups: RelationGroup[] = [];
  public activeRelationTabIndex = 0;
  public activeNestedRelationTabIndex = 0; // Tracks the active tab within Object Relations

  // Action-specific properties
  public dialogMode: CmdbMode = CmdbMode.Create;
  public selectedRelationInstance: ExtendedObjectRelationInstance | null = null;

  // Tracks whether a relation is already used as parent/child by this object
  private usedRolesMap = new Map<number, { parentUsed: boolean; childUsed: boolean }>();

  // Pagination & Sorting properties for relation instances
  public totalRelations: number = 0;
  public relationPage: number = 1;
  public relationPageSize: number = 10;
  public relationSort: string = '';
  public relationOrder: number = 1;

  constructor(
    public objectService: ObjectService,
    private relationService: RelationService,
    private objectRelationService: ObjectRelationService,
    public typeService: TypeService,
    private activateRoute: ActivatedRoute,
    private toastService: ToastService,
    private changesRef: ChangeDetectorRef,
    private modalService: NgbModal
  ) {
    this.activateRoute.data.subscribe({
      next: (data: any) => this.objectViewSubject.next(data.object as RenderResult),
      error: (err) => this.toastService.error(err?.error?.message)
    });
  }

  ngOnInit(): void {
    this.objectViewSubject.pipe(takeUntil(this.unsubscribe)).subscribe({
      next: (result) => {
        this.renderResult = result;
        this.currentObjectID = result?.object_information?.object_id;
        this.activeRelationTabIndex = 0;
        if (this.currentObjectID) {
          this.loadObjectRelationInstances(this.currentObjectID);
        }
        this.changesRef.markForCheck();
      },
      error: (e) => this.toastService.error(e?.error?.message)
    });

    if (this.relationGroups.length > 0) {
      // Load the first group's data automatically on page load
      this.loadGroupInstances(
        this.relationGroups[0].relationId,
        this.relationGroups[0].isParent,
        1, 
        10 
      );
    }
  }

  ngAfterViewInit(): void {
    this.changesRef.detectChanges();
  }

  ngOnDestroy(): void {
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  @HostListener('window:scroll')
  onWindowScroll(): void {
    const dialog = document.getElementsByClassName('object-view-navbar') as HTMLCollectionOf<Element>;
    if (!dialog[0]) return;
    dialog[0].id = document.body.scrollTop > 20 ? 'object-form-action' : '';
    dialog[0].classList.toggle('shadow', document.body.scrollTop > 20);
  }

  /**
 * Returns columns for the cmdb-table based on group properties.
 * @param group The relation group
 */
  public getColumns(group: RelationGroup): any[] {
    return [
      { display: 'ID', name: 'public_id', data: 'public_id', searchable: true, sortable: true, style: { width: '120px', 'text-align': 'center' } },
      { display: 'Linked Object', name: 'counterpart_id', data: 'counterpart_id', sortable: true, template: this.counterpartIdTemplate, style: { width: 'auto', 'text-align': 'center' } },
      // { display: group.isParent ? 'Type Parent' : 'Type Child', name: 'type', data: 'type', sortable: false },
      { display: 'Actions', name: 'actions', template: this.actionsTemplate, sortable: false, style: { width: '150px', 'text-align': 'center' } }
    ];
  }




  // private loadGroupInstances(relationId: number, isParent: boolean, page: number, pageSize: number): void {
  //   const filter = isParent
  //     ? { $and: [ { relation_id: relationId }, { relation_parent_id: this.currentObjectID } ] }
  //     : { $and: [ { relation_id: relationId }, { relation_child_id: this.currentObjectID } ] };
  
  //   const params = {
  //     filter,
  //     limit: pageSize,
  //     sort: this.relationSort,
  //     order: this.relationOrder,
  //     page: page
  //   };
  
  //   this.objectRelationService.getObjectRelations(params)
  //     .pipe(takeUntil(this.unsubscribe))
  //     .subscribe({
  //       next: (response) => {
  //         const group = this.relationGroups.find(g => g.relationId === relationId && g.isParent === isParent);
  //         if (group) {
  //           group.instances = (response.results || []).map(inst => ({
  //             ...inst,
  //             // For parent groups, the linked (counterpart) is the child; vice versa.
  //             counterpart_id: isParent ? inst.relation_child_id : inst.relation_parent_id
  //           }));
  //           group.total = response.total || 0;
  //           group.page = page;
  //           group.pageSize = pageSize;
  //         }
  //         this.changesRef.markForCheck();
  //       },
  //       error: (err) => {
  //         this.toastService.error(err?.error?.message || 'Failed to load group instances');
  //         this.changesRef.markForCheck();
  //       }
  //     });
  // }
  
  private loadGroupInstances(relationId: number, isParent: boolean, page: number, pageSize: number): void {
    const filter = isParent
      ? { $and: [{ relation_id: relationId }, { relation_parent_id: this.currentObjectID }] }
      : { $and: [{ relation_id: relationId }, { relation_child_id: this.currentObjectID }] };
  
    const params = {
      filter,
      limit: pageSize,
      sort: this.relationSort,
      order: this.relationOrder,
      page: page
    };
  
    // Fetch the relation definition for this relationId first
    this.relationService.getRelation(relationId).pipe(
      takeUntil(this.unsubscribe),
      switchMap(definition => {
        if (!definition) {
          throw new Error(`Relation definition not found for ID ${relationId}`);
        }
        // Fetch the paginated instances with the definition available
        return this.objectRelationService.getObjectRelations(params).pipe(
          map(response => ({ definition, response }))
        );
      })
    ).subscribe({
      next: ({ definition, response }) => {
        const group = this.relationGroups.find(g => g.relationId === relationId && g.isParent === isParent);
        if (group) {
          group.instances = (response.results || []).map(inst => ({
            ...inst,
            counterpart_id: isParent ? inst.relation_child_id : inst.relation_parent_id,
            type: isParent ? definition.relation_name_parent : definition.relation_name_child,
            definition // Attach the definition to each instance
          }));
          group.total = response.total || group.total;
          group.pageSize = pageSize;
        }
        this.changesRef.markForCheck();
      },
      error: (err) => {
        this.toastService.error(err?.error?.message);
        this.loadingRelations = false;
        this.changesRef.markForCheck();
      }
    });
  }
  

  /**
   * Loads and groups object relation instances by relation type and role.
   * @param objectID The ID of the current object
   */
  private loadObjectRelationInstances(objectID: number): void {
    const params = {
      filter: {
        $or: [
          { relation_parent_id: objectID },
          { relation_child_id: objectID }
        ]
      },
      limit: 0,
      sort: this.relationSort,
      order: this.relationOrder,
      page: this.relationPage
    };

    this.loadingRelations = true;
    this.objectRelationService.getObjectRelations(params)
      .pipe(takeUntil(this.unsubscribe))
      .subscribe({
        next: (response) => {
          console.log('objectRelationService ####', response)
          this.totalRelations = response.total;
          const rawInstances: ObjectRelationInstance[] = response.results || [];
          console.log(`[DEBUG] Received ${rawInstances.length} raw instances`);
          if (!rawInstances.length) {
            this.relationGroups = [];
            this.loadingRelations = false;
            this.changesRef.markForCheck();
            console.log('[DEBUG] No instances found, relationGroups cleared');
            return;
          }

          this.usedRolesMap = new Map<number, { parentUsed: boolean; childUsed: boolean }>();
          rawInstances.forEach(inst => {
            let roles = this.usedRolesMap.get(inst.relation_id);
            if (!roles) {
              roles = { parentUsed: false, childUsed: false };
            }
            if (inst.relation_parent_id === this.currentObjectID) {
              roles.parentUsed = true;
            }
            if (inst.relation_child_id === this.currentObjectID) {
              roles.childUsed = true;
            }
            this.usedRolesMap.set(inst.relation_id, roles);
          });

          const relationIds = [...new Set(rawInstances.map(inst => inst.relation_id))];
          console.log(`[DEBUG] Fetching definitions for ${relationIds.length} unique relation IDs: ${relationIds}`);
          const relationObservables = relationIds.map(id => this.relationService.getRelation(id));
          const oldTabIndex = this.activeRelationTabIndex;

          forkJoin(relationObservables).pipe(takeUntil(this.unsubscribe)).subscribe({
            next: (definitions: CmdbRelation[]) => {
              console.log(`[DEBUG] Received ${definitions.length} relation definitions`);
              const relationMap = new Map<number, CmdbRelation>();
              definitions.forEach(def => relationMap.set(def.public_id, def));

              const groupedInstances = rawInstances.reduce((acc, instance) => {
                const key = instance.relation_id;
                if (!acc[key]) acc[key] = [];
                acc[key].push(instance);
                return acc;
              }, {} as Record<number, ObjectRelationInstance[]>);

              const groups: RelationGroup[] = [];
              for (const relationIdStr in groupedInstances) {
                const relationId = parseInt(relationIdStr, 10);
                const instancesForRelation = groupedInstances[relationId];
                const definition = relationMap.get(relationId);
                if (!definition) {
                  console.warn(`[DEBUG] Definition missing for relation ID ${relationId}`);
                  continue;
                }

                const parentInstances = instancesForRelation
                  .filter(inst => inst.relation_parent_id === this.currentObjectID)
                  .map(inst => ({
                    ...inst,
                    counterpart_id: inst.relation_child_id,
                    type: definition.relation_name_parent,
                    definition
                  }));

                const childInstances = instancesForRelation
                  .filter(inst => inst.relation_child_id === this.currentObjectID)
                  .map(inst => ({
                    ...inst,
                    counterpart_id: inst.relation_parent_id,
                    type: definition.relation_name_child,
                    definition
                  }));

                if (parentInstances.length > 0) {
                  groups.push({
                    relationId,
                    isParent: true,
                    tabLabel: definition.relation_name_parent,
                    tabColor: definition.relation_color_parent,
                    tabIcon: definition.relation_icon_parent,
                    instances: parentInstances,
                    total: parentInstances.length
                  });
                  console.log(`[DEBUG] Added parent group for relation ${relationId} with ${parentInstances.length} instances`);
                }

                if (childInstances.length > 0) {
                  groups.push({
                    relationId,
                    isParent: false,
                    tabLabel: definition.relation_name_child,
                    tabColor: definition.relation_color_child,
                    tabIcon: definition.relation_icon_child,
                    instances: childInstances,
                    total: childInstances.length
                  });
                  console.log(`[DEBUG] Added child group for relation ${relationId} with ${childInstances.length} instances`);
                }
              }

              this.relationGroups = groups;
              console.log(`[DEBUG] Total relationGroups created: ${this.relationGroups.length}`);

              if (this.activeRelationTabIndex === 1 && this.activeNestedRelationTabIndex > this.relationGroups.length) {
                this.activeNestedRelationTabIndex = 0;
              } else if (oldTabIndex > 1) {
                this.activeRelationTabIndex = 1; // Move to Object Relations if previously on a relation tab
                this.activeNestedRelationTabIndex = oldTabIndex - 1; // Adjust for new structure
              } else {
                this.activeRelationTabIndex = oldTabIndex;
              }

              this.loadingRelations = false;
              this.changesRef.markForCheck();
              console.log('[DEBUG] loadObjectRelationInstances completed');
            },
            error: (err) => {
              this.toastService.error(err?.error?.message || 'Failed to fetch relation definitions');
              this.loadingRelations = false;
              this.changesRef.markForCheck();
              console.error('[DEBUG] Error fetching relation definitions:', err);
            }
          });
        },
        error: (err) => {
          this.toastService.error(err?.error?.message || 'Failed to load object relations');
          this.loadingRelations = false;
          this.changesRef.markForCheck();
          console.error('[DEBUG] Error loading object relations:', err);
        }
      });
  }



  /**
   * Loads available relations for creating a new relation.
   */
  private loadRelationsForNewRelation(): void {
    const typeId = this.renderResult?.type_information?.type_id;
    if (!typeId) {
      this.toastService.warning('No valid type ID found.');
      return;
    }

    this.loadingRelations = true;

    const params = {
      filter: {
        $or: [
          { parent_type_ids: { $in: [typeId] } },
          { child_type_ids: { $in: [typeId] } }
        ]
      },
      limit: 40,
      sort: '',
      order: 1,
      page: 1
    };

    this.relationService.getRelations(params)
      .pipe(takeUntil(this.unsubscribe))
      .subscribe({
        next: (response) => {
          this.availableRelations = response.results || [];

          this.extendedRelations = this.availableRelations.map(rel => {
            let canBeParent = rel.parent_type_ids?.includes(typeId) || false;
            let canBeChild = rel.child_type_ids?.includes(typeId) || false;

            const used = this.usedRolesMap.get(rel.public_id);
            if (used) {
              if (used.parentUsed) {
                canBeParent = false;
              }
              if (used.childUsed) {
                canBeChild = false;
              }
            }

            return {
              ...rel,
              canBeParent,
              canBeChild
            };
          }).filter(rel => rel.canBeParent || rel.canBeChild);

          this.loadingRelations = false;
          this.changesRef.detectChanges();
        },
        error: (err) => {
          this.toastService.error(err?.error?.message || 'Failed to load available relations');
          this.loadingRelations = false;
          this.changesRef.detectChanges();
        }
      });
  }

  /** Opens the relation selection modal */
  // public openRelationModal(): void {
  //   this.showRelationModal = true;
  //   this.chosenRelation = null;
  //   this.chosenRole = null;
  //   this.loadRelationsForNewRelation();
  // }

  public openRelationModal(): void {
    // Refresh used relations and available relations.
    this.loadObjectRelationInstances(this.currentObjectID);
    this.loadRelationsForNewRelation();

    // Reset current selection.
    this.chosenRelation = null;
    this.chosenRole = null;

    setTimeout(() => {
      this.showRelationModal = true;
      this.changesRef.detectChanges();
    }, 10);
  }


  /** Closes the relation selection modal */
  public closeRelationModal(): void {
    this.showRelationModal = false;
  }

  /** Selects a relation and role in the modal */
  public onSelectRelation(relation: ExtendedRelation, role: 'parent' | 'child'): void {
    if ((role === 'parent' && !relation.canBeParent) || (role === 'child' && !relation.canBeChild)) {
      return;
    }
    this.chosenRelation = relation;
    this.chosenRole = role;
  }

  /** Confirms relation selection and opens role dialog */
  public onConfirmRelationSelection(): void {
    if (!this.chosenRelation || !this.chosenRole) return;
    this.closeRelationModal();
    this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : this.chosenRelation.parent_type_ids;
    this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : this.chosenRelation.child_type_ids;
    console.log('[DEBUG] Dialog inputs:', {
      chosenRole: this.chosenRole,
      currentObjectTypeID: this.renderResult.type_information.type_id,
      parentTypeIDs: this.roleParentTypeIDs,
      childTypeIDs: this.roleChildTypeIDs,
      currentObjectID: this.currentObjectID,
      relation: this.chosenRelation
    });
    this.showRelationRoleDialog = true;
    this.dialogMode = CmdbMode.Create; // Ensure Create mode for new relations
    this.selectedRelationInstance = null; // Clear any selected instance
    this.changesRef.detectChanges();
  }

  /** Handles confirmation from the relation role dialog */
  public handlePopUp2Confirm(selection: { parentObjID?: number; childObjID?: number }): void {
    this.showRelationRoleDialog = false;
    this.selectedRelationInstance = null;
    this.dialogMode = CmdbMode.Create; // Reset to default mode
    if (this.currentObjectID) {
      this.loadObjectRelationInstances(this.currentObjectID);
    }
    this.changesRef.markForCheck();
  }

  /** Handles cancellation from the relation role dialog */
  public handlePopUp2Cancel(): void {
    this.showRelationRoleDialog = false;
    this.selectedRelationInstance = null;
    this.dialogMode = CmdbMode.Create; // Reset to default mode
    this.toastService.info('Operation cancelled');
    this.changesRef.markForCheck();
  }

  /** Sets the active tab index */
  public setActiveTab(tabIndex: number): void {
    this.activeRelationTabIndex = tabIndex;
    if (tabIndex !== 1) {
      this.activeNestedRelationTabIndex = 0; // Reset nested tab when switching away from Object Relations
    }
    this.changesRef.markForCheck();
  }

  /** Sets the active nested relation tab index */
  // public setNestedRelationTab(tabIndex: number): void {
  //   this.activeNestedRelationTabIndex = tabIndex;
  //   this.changesRef.markForCheck();
  // }

  public setNestedRelationTab(tabIndex: number): void {
    this.activeNestedRelationTabIndex = tabIndex;
    const group = this.relationGroups[tabIndex];
    if (group) {
      // Use default page 1 and the group's pageSize (or a default value, e.g., 10)
      this.loadGroupInstances(group.relationId, group.isParent, 1, group.pageSize || 10);
    }
    this.changesRef.markForCheck();
  }
  

  /** Handles clicking the "+" tab to add a new relation */
  public onClickAddRelationTab(): void {
    this.openRelationModal();
    this.setActiveTab(1); // Ensure Object Relations is active
    this.setNestedRelationTab(this.relationGroups.length); // Highlight the "+" tab
  }

  /**
   * Creates a new relation for an existing relation group.
   * @param group The relation group to create a new instance for
   */
  // public createNewRelationForGroup(group: RelationGroup): void {
  //   const definition = group.instances[0].definition;
  //   if (!definition) {
  //     this.toastService.error('Relation definition is missing.');
  //     return;
  //   }

  //   const safeDefinition = {
  //     ...definition,
  //     parent_type_ids: Array.isArray(definition.parent_type_ids) ? definition.parent_type_ids : [],
  //     child_type_ids: Array.isArray(definition.child_type_ids) ? definition.child_type_ids : [],
  //     canBeParent: group.isParent,
  //     canBeChild: !group.isParent
  //   };

  //   this.chosenRelation = safeDefinition;
  //   this.chosenRole = group.isParent ? 'parent' : 'child';
  //   this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : safeDefinition.parent_type_ids;
  //   this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : safeDefinition.child_type_ids;

  //   if (this.chosenRole === 'parent' && this.roleChildTypeIDs.length === 0) {
  //     this.toastService.warning('No child types defined for this relation.');
  //     return;
  //   }
  //   if (this.chosenRole === 'child' && this.roleParentTypeIDs.length === 0) {
  //     this.toastService.warning('No parent types defined for this relation.');
  //     return;
  //   }

  //   this.showRelationRoleDialog = true;
  //   this.dialogMode = CmdbMode.Create;
  //   this.selectedRelationInstance = null; // Clear any selected instance
  //   this.changesRef.detectChanges();
  // }

  public createNewRelationForGroup(group: RelationGroup): void {
    // Try to get the definition from the first instance in the group.
    let definition = group.instances.length > 0 ? group.instances[0].definition : null;
    // If not found, look for the definition in extendedRelations.
    if (!definition) {
      definition = this.extendedRelations.find(rel => rel.public_id === group.relationId);
    }
    if (!definition) {
      this.toastService.error('Relation definition is missing.');
      return;
    }
  
    const safeDefinition = {
      ...definition,
      parent_type_ids: Array.isArray(definition.parent_type_ids) ? definition.parent_type_ids : [],
      child_type_ids: Array.isArray(definition.child_type_ids) ? definition.child_type_ids : [],
      canBeParent: group.isParent,
      canBeChild: !group.isParent
    };
  
    this.chosenRelation = safeDefinition;
    this.chosenRole = group.isParent ? 'parent' : 'child';
    this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : safeDefinition.parent_type_ids;
    this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : safeDefinition.child_type_ids;
  
    if (this.chosenRole === 'parent' && this.roleChildTypeIDs.length === 0) {
      this.toastService.warning('No child types defined for this relation.');
      return;
    }
    if (this.chosenRole === 'child' && this.roleParentTypeIDs.length === 0) {
      this.toastService.warning('No parent types defined for this relation.');
      return;
    }
  
    this.showRelationRoleDialog = true;
    this.dialogMode = CmdbMode.Create; // Set mode to Create
    this.selectedRelationInstance = null; // Clear any selected instance
    this.changesRef.markForCheck();
  }
  
  

  /**
   * Deletes a relation instance.
   * @param instance The relation instance to delete
   */
  // public deleteRelationInstance(instance: ExtendedObjectRelationInstance): void {
  //   if (confirm('Are you sure you want to delete this relation instance?')) {
  //     this.loadingRelations = true;
  //     this.objectRelationService.deleteObjectRelation(instance.public_id)
  //       .pipe(takeUntil(this.unsubscribe))
  //       .subscribe({
  //         next: () => {
  //           this.toastService.success('Relation instance deleted successfully');

  //           // Refresh the usedRolesMap after deletion
  //           const roles = this.usedRolesMap.get(instance.relation_id);
  //           if (roles) {
  //             if (instance.relation_parent_id === this.currentObjectID) {
  //               roles.parentUsed = false;
  //             }
  //             if (instance.relation_child_id === this.currentObjectID) {
  //               roles.childUsed = false;
  //             }
  //             this.usedRolesMap.set(instance.relation_id, roles);
  //           }

  //           // Reload relations to ensure the modal updates correctly
  //           this.loadObjectRelationInstances(this.currentObjectID);
  //           this.loadRelationsForNewRelation();

  //           this.changesRef.markForCheck();
  //         },
  //         error: (err) => {
  //           this.toastService.error(err?.error?.message);
  //           this.loadingRelations = false;
  //           this.changesRef.detectChanges();
  //         }
  //       });
  //   }
  // }

  /**
 * Deletes a relation instance using a reusable core delete modal.
 * @param instance The relation instance to delete.
 */
  public deleteRelationInstance(instance: ExtendedObjectRelationInstance): void {
    const modalRef = this.modalService.open(CoreDeleteConfirmationModalComponent, { size: 'lg' });
    modalRef.componentInstance.title = 'Delete Object Relation';
    modalRef.componentInstance.item = instance;
    modalRef.componentInstance.itemType = 'Object Relation';
    modalRef.componentInstance.itemName = instance.public_id;

    modalRef.result.then(
      (result) => {
        if (result === 'confirmed') {
          this.loadingRelations = true;
          this.objectRelationService.deleteObjectRelation(instance.public_id)
            .pipe(takeUntil(this.unsubscribe))
            .subscribe({
              next: () => {
                this.toastService.success('Relation instance deleted successfully');
                this.loadObjectRelationInstances(this.currentObjectID);
              },
              error: (err) => {
                this.toastService.error(err?.error?.message);
                this.loadingRelations = false;
                this.changesRef.markForCheck();
              }
            });
        }
      },
      () => { }
    );
  }


  /**
   * Views a relation instance in read-only mode.
   * @param instance The relation instance to view
   */
  public viewRelationInstance(instance: ExtendedObjectRelationInstance): void {
    this.chosenRelation = {
      ...instance.definition,
      canBeParent: instance.relation_parent_id === this.currentObjectID,
      canBeChild: instance.relation_child_id === this.currentObjectID
    };
    this.chosenRole = instance.relation_parent_id === this.currentObjectID ? 'parent' : 'child';
    this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : instance.definition.parent_type_ids;
    this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : instance.definition.child_type_ids;
    this.dialogMode = CmdbMode.View;
    this.selectedRelationInstance = instance;
    this.showRelationRoleDialog = true;
    this.changesRef.detectChanges();
  }


  /**
   * Edits an existing relation instance.
   * @param instance The relation instance to edit
   */
  public editRelationInstance(instance: ExtendedObjectRelationInstance): void {
    this.chosenRelation = {
      ...instance.definition,
      canBeParent: instance.relation_parent_id === this.currentObjectID,
      canBeChild: instance.relation_child_id === this.currentObjectID
    };
    this.chosenRole = instance.relation_parent_id === this.currentObjectID ? 'parent' : 'child';
    this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : instance.definition.parent_type_ids;
    this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : instance.definition.child_type_ids;
    this.dialogMode = CmdbMode.Edit;
    this.selectedRelationInstance = instance;
    this.showRelationRoleDialog = true;
    this.changesRef.detectChanges();
  }


  /**
   * Copies an existing relation instance for creating a new one.
   * @param instance The relation instance to copy
   */
  public copyRelationInstance(instance: ExtendedObjectRelationInstance): void {
    this.chosenRelation = {
      ...instance.definition,
      canBeParent: instance.relation_parent_id === this.currentObjectID,
      canBeChild: instance.relation_child_id === this.currentObjectID
    };
    this.chosenRole = instance.relation_parent_id === this.currentObjectID ? 'parent' : 'child';
    this.roleParentTypeIDs = this.chosenRole === 'parent' ? [] : instance.definition.parent_type_ids;
    this.roleChildTypeIDs = this.chosenRole === 'child' ? [] : instance.definition.child_type_ids;
    this.dialogMode = CmdbMode.Create;
    this.selectedRelationInstance = instance;
    this.showRelationRoleDialog = true;
    this.changesRef.detectChanges();
  }


  trackByRelationId(index: number, group: RelationGroup): number {
    return group.relationId;
  }

  public onRelationPageChange(newPage: number): void {
    this.relationPage = newPage;
    this.loadObjectRelationInstances(this.currentObjectID);
  }

  public onRelationPageSizeChange(newLimit: number): void {
    this.relationPageSize = newLimit;
    this.relationPage = 1; // Reset to first page
    this.loadObjectRelationInstances(this.currentObjectID);
  }

  public onRelationSortChange(event: { sort: string; order: number }): void {
    this.relationSort = event.sort;
    this.relationOrder = event.order;
    this.loadObjectRelationInstances(this.currentObjectID);
  }

  public onRelationSearchChange(searchTerm: string): void {
    // If your API supports search filtering, update your filter here.
    // For example, you might store the term and include it in your filter params.
    console.log('[DEBUG] Relation search term:', searchTerm);
    // Then re-call your data loading method.
    this.loadObjectRelationInstances(this.currentObjectID);
  }

}