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

import {
    ChangeDetectorRef,
    Component,
    HostListener,
    OnDestroy,
    OnInit
} from '@angular/core';
import { ActivatedRoute, Data } from '@angular/router';
import { BehaviorSubject, Subject, takeUntil } from 'rxjs';

import { ObjectService } from '../../services/object.service';
import { CmdbMode } from '../../modes.enum';
import { RenderResult } from '../../models/cmdb-render';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { RelationService } from '../../services/relaion.service';
import { CmdbRelation } from '../../models/relation.model';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { TypeService } from '../../services/type.service';

/**
 * ExtendedRelation flags which actions (Parent, Child) are available.
 * 
 * - canBeParent = true if the current object's type_id is in the relation's parent_type_ids
 * - canBeChild  = true if the current object's type_id is in the relation's child_type_ids
 * 
 * Therefore:
 *  - If both are true, show both "Parent" and "Child" in the action column.
 *  - If only parent is true, show only "Parent".
 *  - If only child is true, show only "Child".
//  */
// interface ExtendedRelation extends CmdbRelation {
//   canBeParent: boolean;
//   canBeChild: boolean;
// }

// @Component({
//   selector: 'cmdb-object-view',
//   templateUrl: './object-view.component.html',
//   styleUrls: ['./object-view.component.scss']
// })
// export class ObjectViewComponent implements OnInit, OnDestroy {
//   public mode: CmdbMode = CmdbMode.View;
//   public renderResult: RenderResult;
//   private unsubscribe = new Subject<void>();
//   private objectViewSubject = new BehaviorSubject<RenderResult>(undefined);

//   public showRelationModal = false;
//   public loadingRelations = false;
//   public availableRelations: CmdbRelation[] = [];
//   public extendedRelations: ExtendedRelation[] = [];

//   public chosenRelation: ExtendedRelation | null = null;
//   public chosenRole: 'parent' | 'child' | null = null;

//   constructor(
//     public objectService: ObjectService,
//     private activateRoute: ActivatedRoute,
//     private changesRef: ChangeDetectorRef,
//     private toastService: ToastService,
//     private relationService: RelationService
//   ) {
//     this.activateRoute.data.subscribe({
//       next: (data: Data) => {
//         this.objectViewSubject.next(data.object as RenderResult);
//       },
//       error: (err) => {
//         this.toastService.error(err?.error?.message);
//       }
//     });
//   }

//   public ngOnInit(): void {
//     this.objectViewSubject
//       .asObservable()
//       .pipe(takeUntil(this.unsubscribe))
//       .subscribe({
//         next: (result) => {
//           this.renderResult = result;
//         },
//         error: (e) => {
//           this.toastService.error(e?.error?.message);
//         }
//       });
//   }

//   ngAfterViewInit(): void {
//     this.changesRef.detectChanges();
//   }

//   public ngOnDestroy(): void {
//     this.unsubscribe.next();
//     this.unsubscribe.complete();
//   }

//   @HostListener('window:scroll')
//   onWindowScroll(): void {
//     const dialog = document.getElementsByClassName('object-view-navbar') as HTMLCollectionOf<any>;
//     if (!dialog[0]) return;

//     dialog[0].id = 'object-form-action';
//     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//       dialog[0].style.visibility = 'visible';
//       dialog[0].classList.add('shadow');
//     } else {
//       dialog[0].classList.remove('shadow');
//       dialog[0].id = '';
//     }
//   }

//   public openRelationModal(): void {
//     this.showRelationModal = true;
//     this.loadRelationsForCurrentObject();
//   }

//   public closeRelationModal(): void {
//     this.showRelationModal = false;
//     this.chosenRelation = null;
//     this.chosenRole = null;
//   }

//   /**
//    * Fetch relations where this object's type_id is in parent_type_ids or child_type_ids.
//    * Then determine canBeParent/canBeChild for each relation.
//    */
//   private loadRelationsForCurrentObject(): void {
//     this.loadingRelations = true;

//     const tID = this.renderResult?.type_information?.type_id;
//     if (!tID) {
//       this.toastService.warning('No valid type ID found.');
//       this.loadingRelations = false;
//       return;
//     }

//     const params: CollectionParameters = {
//       filter: {
//         $or: [
//           { parent_type_ids: { $in: [tID] } },
//           { child_type_ids: { $in: [tID] } }
//         ]
//       },
//       limit: 40,
//       sort: '',
//       order: 1,
//       page: 1
//     };

//     this.relationService
//       .getRelations(params)
//       .pipe(takeUntil(this.unsubscribe))
//       .subscribe({
//         next: (response) => {
//           this.availableRelations = response.results || [];
//           const results: ExtendedRelation[] = [];

//           for (const rel of this.availableRelations) {
//             const parentHasType = Array.isArray(rel.parent_type_ids) && rel.parent_type_ids.includes(tID);
//             const childHasType  = Array.isArray(rel.child_type_ids)  && rel.child_type_ids.includes(tID);

//             // canBeParent => true if the object's type is found in parent's array
//             // canBeChild  => true if the object's type is found in child's array
//             results.push({
//               ...rel,
//               canBeParent: !!parentHasType,
//               canBeChild:  !!childHasType
//             });
//           }

//           this.extendedRelations = results;
//           this.loadingRelations = false;
//         },
//         error: (err) => {
//           this.toastService.error(err?.error?.message);
//           this.loadingRelations = false;
//         }
//       });
//   }

//   public onSelectRelation(relation: ExtendedRelation, role: 'parent' | 'child'): void {
//     // If user clicks 'parent' but it's not available, do nothing.
//     if (role === 'parent' && !relation.canBeParent) return;
//     // If user clicks 'child' but it's not available, do nothing.
//     if (role === 'child' && !relation.canBeChild) return;

//     this.chosenRelation = relation;
//     this.chosenRole = role;
//   }

//   public onConfirmRelationSelection(): void {
//     if (!this.chosenRelation || !this.chosenRole) {
//       this.toastService.warning('Please select a relation (Parent or Child) first!');
//       return;
//     }
//     if (this.chosenRole === 'parent') {
//       this.toastService.info(
//         `Selected [${this.chosenRelation.relation_name_parent}] as PARENT. Child side is editable!`
//       );
//     } else {
//       this.toastService.info(
//         `Selected [${this.chosenRelation.relation_name_child}] as CHILD. Parent side is editable!`
//       );
//     }
//     this.closeRelationModal();
//   }
// }






interface ExtendedRelation extends CmdbRelation {
  canBeParent: boolean;
  canBeChild: boolean;
}

@Component({
  selector: 'cmdb-object-view',
  templateUrl: './object-view.component.html',
  styleUrls: ['./object-view.component.scss']
})
export class ObjectViewComponent implements OnInit, OnDestroy {
  public mode: CmdbMode = CmdbMode.View;
  public renderResult: RenderResult;
  public currentObjectID: number;
  private unsubscribe = new Subject<void>();
  private objectViewSubject = new BehaviorSubject<RenderResult>(undefined);

  public showRelationModal = false;
  public loadingRelations = false;
  public availableRelations: CmdbRelation[] = [];
  public extendedRelations: ExtendedRelation[] = [];
  public chosenRelation: ExtendedRelation = null;
  public chosenRole: 'parent' | 'child'  = null;
  public showRelationRoleDialog = false;
  public roleParentTypeIDs: number[] = [];
  public roleChildTypeIDs: number[] = [];

  constructor(
    public objectService: ObjectService,

    public typeService: TypeService,
    private activateRoute: ActivatedRoute,
    private changesRef: ChangeDetectorRef,
    private toastService: ToastService,
    private relationService: RelationService
  ) {
    this.activateRoute.data.subscribe({
      next: (data: any) => this.objectViewSubject.next(data.object as RenderResult),
      error: (err) => this.toastService.error(err?.error?.message)
    });
  }

  ngOnInit(): void {
    this.objectViewSubject.pipe(takeUntil(this.unsubscribe)).subscribe({
      next: (result) => this.renderResult = result,
      error: (e) => this.toastService.error(e?.error?.message)
    });
  }

  ngAfterViewInit(): void { this.changesRef.detectChanges(); }
  ngOnDestroy(): void { this.unsubscribe.next(); this.unsubscribe.complete(); }

  @HostListener('window:scroll')
  onWindowScroll(): void {
    const dialog = document.getElementsByClassName('object-view-navbar') as HTMLCollectionOf<any>;
    if (!dialog[0]) return;
    dialog[0].id = document.body.scrollTop > 20 ? 'object-form-action' : '';
    dialog[0].classList.toggle('shadow', document.body.scrollTop > 20);
  }

  openRelationModal(): void { this.showRelationModal = true; this.loadRelationsForCurrentObject(); }
  closeRelationModal(): void { this.showRelationModal = false; }

  private loadRelationsForCurrentObject(): void {
    this.loadingRelations = true;
    const tID = this.renderResult?.type_information?.type_id;
    if (!tID) { this.toastService.warning('No valid type ID found.'); return; }

    const params: CollectionParameters = {
      filter: { $or: [{ parent_type_ids: { $in: [tID] } }, { child_type_ids: { $in: [tID] } }] },
      limit: 40, sort: '', order: 1, page: 1
    };

    this.relationService.getRelations(params).pipe(takeUntil(this.unsubscribe)).subscribe({
      next: (response) => {
        console.log('relation', response.results)
        this.availableRelations = response.results ;
        this.extendedRelations = this.availableRelations.map(rel => ({
          ...rel,
          canBeParent: rel.parent_type_ids?.includes(tID) || false,
          canBeChild: rel.child_type_ids?.includes(tID) || false
        }));
        this.loadingRelations = false;
      },
      error: (err) => { this.toastService.error(err?.error?.message); this.loadingRelations = false; }
    });
  }

  onSelectRelation(relation: ExtendedRelation, role: 'parent' | 'child'): void {
    if ((role === 'parent' && !relation.canBeParent) || (role === 'child' && !relation.canBeChild)) return;
    this.chosenRelation = relation;
    this.chosenRole = role;
  }

  // public onConfirmRelationSelection(): void {
  //   if (!this.chosenRelation || !this.chosenRole) {
  //     this.toastService.warning('Please select a relation first!');
  //     return;
  //   }
  
  //   this.currentObjectID = this.renderResult.object_information.object_id;
  
  //   // Flatten and validate type IDs
  //   this.roleParentTypeIDs = this.chosenRole === 'parent' 
  //     ? [] 
  //     : [].concat(...this.chosenRelation.parent_type_ids).filter(Number.isInteger);
  
  //   this.roleChildTypeIDs = this.chosenRole === 'child' 
  //     ? [] 
  //     : [].concat(...this.chosenRelation.child_type_ids).filter(Number.isInteger);
  
  //   console.log('Final Type IDs:', {
  //     parent: this.roleParentTypeIDs,
  //     child: this.roleChildTypeIDs
  //   });
  
  //   this.closeRelationModal();
  //   this.showRelationRoleDialog = true;
  // }

  public onConfirmRelationSelection(): void {
    if (!this.chosenRelation || !this.chosenRole) return;
  
    this.currentObjectID = this.renderResult.object_information.object_id;

    console.log('currcurrentObjectIDent ääääää ', this.currentObjectID)
  
    // Set parent and child type IDs based on chosen role
    if (this.chosenRole === 'parent') {
      this.roleParentTypeIDs = [];
      this.roleChildTypeIDs = this.chosenRelation.child_type_ids;
    } else {
      this.roleParentTypeIDs = this.chosenRelation.parent_type_ids;
      this.roleChildTypeIDs = [];
    }
  
    console.log('Final Type IDs:', {
      parent: this.roleParentTypeIDs,
      child: this.roleChildTypeIDs
    });
  
    this.closeRelationModal();
    this.showRelationRoleDialog = true;

    

    // console.log('roleChildTypeIDs', this.roleChildTypeIDs)
    // this.objectService.getObjectsByType(this.roleChildTypeIDs).subscribe({
    //   next: (res) => {
    //     console.log("getObjectsByType",res)
    //   }
    // })
  }

  handlePopUp2Confirm(selection: { parentObjID?: number; childObjID?: number }): void {
    this.toastService.success(`Created: Parent=${selection.parentObjID}, Child=${selection.childObjID}`);
    this.showRelationRoleDialog = false;
  }

  handlePopUp2Cancel(): void { this.showRelationRoleDialog = false; this.toastService.info('Cancelled'); }
}