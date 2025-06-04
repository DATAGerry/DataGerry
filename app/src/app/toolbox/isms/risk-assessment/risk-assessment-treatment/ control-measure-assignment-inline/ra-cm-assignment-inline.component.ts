// import {
//     Component, Input, ViewChild, TemplateRef, OnInit, OnChanges, SimpleChanges, inject,
//     AfterViewInit
// } from '@angular/core';
// import {
//     FormArray, FormBuilder, FormGroup, Validators
// } from '@angular/forms';
// import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
// import { Column, Sort } from 'src/app/layout/table/table.types';
// import { ControlMeasureAssignment } from '../../../models/control‑measure‑assignment.model';
// import { DateFormatterPipe } from 'src/app/layout/pipes/date-formatter.pipe';
// import { DatePipe } from '@angular/common';

// @Component({
//     selector: 'ra-cm-assignment-inline',
//     templateUrl: './ra-cm-assignment-inline.component.html',
//     styleUrls: ['./ra-cm-assignment-inline.component.scss']
// })
// export class RaCmAssignmentInlineComponent implements OnInit, OnChanges, AfterViewInit {

//     @Input() parentForm!: FormGroup;
//     @Input() createMode = true;
//     @Input() allControlMeasures: { public_id: number; title: string }[] = [];
//     @Input() implementationStates: { public_id: number; value: string }[] = [];
//     @Input() allPersons: any[] = [];
//     @Input() allPersonGroups: any[] = [];

//     @ViewChild('modalTpl', { static: true }) modalTpl!: TemplateRef<any>;
//     @ViewChild('cmActionsTpl', { static: true }) cmActionsTpl!: TemplateRef<any>;
//     @ViewChild('dateTpl', { static: false }) dateTpl!: TemplateRef<any>;


//     private readonly fb = inject(FormBuilder);
//     private readonly modal = inject(NgbModal);

//     private readonly cmMap = new Map<number, string>();
//     private readonly stsMap = new Map<number, string>();
//     private readonly prioMap = new Map<number, string>([
//         [1, 'Low'], [2, 'Medium'], [3, 'High'], [4, 'Very High']
//     ]);

//     readonly priorityOptions = [
//         { label: 'Low', value: 1 },
//         { label: 'Medium', value: 2 },
//         { label: 'High', value: 3 },
//         { label: 'Very High', value: 4 }
//     ];

//     responsibleOptions: any[] = [];
//     modalForm!: FormGroup;
//     private modalRef!: NgbModalRef;
//     editIndex: number | null = null;

//     columns!: Column[];
//     addedAssignmentsSelect: { id: number; label: string }[] = [];

//       page: number = 1;


//     constructor(private dateFormatterPipe: DateFormatterPipe, private datePipe: DatePipe
//     ) { }

//     ngOnInit(): void {



//         this.allControlMeasures.forEach(cm => this.cmMap.set(cm.public_id, cm.title));
//         this.implementationStates.forEach(s => this.stsMap.set(s.public_id, s.value));

//         this.responsibleOptions = [
//             ...this.allPersonGroups.map(g => ({
//                 public_id: g.public_id, display_name: g.name,
//                 group: 'Person groups', type: 'PERSON_GROUP'
//             })),
//             ...this.allPersons.map(p => ({
//                 public_id: p.public_id, display_name: p.display_name,
//                 group: 'Persons', type: 'PERSON'
//             }))
//         ];

//         if (!this.parentForm.get('selected_cm_assignment_ids')) {
//             this.parentForm.addControl('selected_cm_assignment_ids', this.fb.control([]));
//         }
//     }

//     ngAfterViewInit(): void {
//         this.columns = [
//             { display: 'CM', name: 'cm', data: 'cmLabel', sortable: true },
//             {
//                 display: 'Planned',
//                 name: 'plan',
//                 data: 'planned_implementation_date',
//                 sortable: true,
//                 style: { width: '130px' },
//                 template: this.dateTpl,
//             }, 
//             { display: 'Status', name: 'sts', data: 'statusLabel' },
//             { display: 'Priority', name: 'prio', data: 'priorityLabel', sortable: true, style: { width: '110px' } },
//             {
//                 display: 'Actions',
//                 name: 'act',
//                 data: 'dummy',
//                 template: this.cmActionsTpl,
//                 sortable: false,
//                 fixed: true,
//                 style: { width: '90px', 'text-align': 'center' }
//             }
//         ];
//     }

//     ngOnChanges(ch: SimpleChanges): void {
//         if (ch['allControlMeasures'] && !ch['allControlMeasures'].firstChange) {
//             this.allControlMeasures.forEach(cm => this.cmMap.set(cm.public_id, cm.title));
//         }
//     }

//     private get cmArray(): FormArray {
//         if (!this.parentForm.get('control_measure_assignments')) {
//             this.parentForm.addControl('control_measure_assignments', new FormArray([]));
//         }
//         return this.parentForm.get('control_measure_assignments') as FormArray;
//     }


//     // get tableRows(): any[] {
//     //     return this.cmArray.value.map((a: ControlMeasureAssignment) => ({
//     //         ...a,
//     //         cmLabel: this.cmMap.get(a.control_measure_id) ?? `#${a.control_measure_id}`,
//     //         statusLabel: this.stsMap.get(a.implementation_status) ?? a.implementation_status,
//     //         priorityLabel: this.prioMap.get(a.priority ?? 0) ?? ''
//     //     }));
//     // }

//     get tableRows(): any[] {
//         const rows = this.cmArray.value.map((a: ControlMeasureAssignment) => ({
//           ...a,
//           cmLabel: this.cmMap.get(a.control_measure_id) ?? `#${a.control_measure_id}`,
//           statusLabel: this.stsMap.get(a.implementation_status) ?? a.implementation_status,
//           priorityLabel: this.prioMap.get(a.priority ?? 0) ?? ''
//         }));

//         const startIndex = (this.page - 1) * 5;
//         const endIndex = startIndex + 5;
//         return rows.slice(startIndex, endIndex);
//       }


//     onSort(_: Sort) { }

//     private buildModalForm(seed?: Partial<ControlMeasureAssignment>): FormGroup {
//         return this.fb.group({
//             control_measure_id: [seed?.control_measure_id ?? null, Validators.required],
//             planned_implementation_date: seed?.planned_implementation_date ?? null,
//             implementation_status: [seed?.implementation_status ?? null, Validators.required],
//             finished_implementation_date: seed?.finished_implementation_date ?? null,
//             priority: seed?.priority ?? null,
//             responsible_for_implementation_id_ref_type: [seed?.responsible_for_implementation_id_ref_type ?? 'PERSON'],
//             responsible_for_implementation_id: [seed?.responsible_for_implementation_id ?? null, Validators.required]
//         });
//     }

//     private resetModalForm(): void {
//         this.modalForm.reset();
//         this.modalForm.patchValue({
//             responsible_for_implementation_id_ref_type: 'PERSON'
//         });
//     }

//     openModal(idx?: number): void {
//         const isAlreadyOpen = !!this.modalRef;
//         this.editIndex = idx ?? null;
//         const seed = idx != null ? { ...this.cmArray.at(idx).getRawValue() } : undefined;

//         if (!isAlreadyOpen) {
//             this.modalForm = this.buildModalForm(seed);
//             this.modalRef = this.modal.open(this.modalTpl, {
//                 size: 'lg', centered: true, backdrop: 'static', windowClass: 'dg-modal'
//             });

//             this.modalRef.result.finally(() => {
//                 this.resetModalForm();
//                 this.editIndex = null;
//                 this.modalRef = undefined!;
//             });
//         } else {
//             this.modalForm.patchValue(seed ?? {});
//         }
//     }

//     private addAssignment(value: ControlMeasureAssignment): void {
//         this.cmArray.push(this.fb.group(value));
//     }

//     private updateAssignment(index: number, value: ControlMeasureAssignment): void {
//         this.cmArray.at(index).patchValue(value);
//     }

//     saveAssignment(): void {
//         if (this.modalForm.invalid) return;

//         const value = this.modalForm.getRawValue();

//         if (this.editIndex !== null) {
//             this.updateAssignment(this.editIndex, value);
//             this.modalRef.close();
//         } else {
//             this.addAssignment(value);
//             this.resetModalForm();
//         }

//         this.updateAddedAssignmentsSelect(); // Only update visible dropdown list
//     }


//     deleteRow(item: ControlMeasureAssignment): void {
//         const index = this.cmArray.value.findIndex(
//           (a: ControlMeasureAssignment) => a.control_measure_id === item.control_measure_id
//         );

//         if (index === -1) {
//           console.warn('No form control found for item', item);
//           return;
//         }

//         const removedId = this.cmArray.at(index).get('control_measure_id')?.value;
//         this.cmArray.removeAt(index);

//         const current = this.parentForm.get('selected_cm_assignment_ids')?.value || [];
//         const updated = current.filter((id: number) => id !== removedId);

//         this.parentForm.get('selected_cm_assignment_ids')?.setValue(updated, { emitEvent: false });
//         this.updateAddedAssignmentsSelect();
//       }



//     onEditRow(item: ControlMeasureAssignment): void {
//         const index = this.cmArray.value.findIndex((a: ControlMeasureAssignment) =>
//             a.control_measure_id === item.control_measure_id
//         );

//         if (index !== -1) {
//             this.openModal(index);
//         } else {
//             console.warn('Could not find index for item', item);
//         }
//     }

//     private updateAddedAssignmentsSelect(): void {
//         this.addedAssignmentsSelect = this.cmArray.value.map((a: ControlMeasureAssignment) => ({
//             id: a.control_measure_id,
//             label: this.cmMap.get(a.control_measure_id) ?? `#${a.control_measure_id}`
//         }));
//     }

//     formatDate(date: any): string {
//         if (!date) return '';

//         // Convert NgbDateStruct to native Date
//         if (typeof date === 'object' && 'year' in date && 'month' in date && 'day' in date) {
//           const jsDate = new Date(date.year, date.month - 1, date.day); // month is 0-indexed
//           return this.datePipe.transform(jsDate, 'mediumDate') ?? '';
//         }

//         // Fallback
//         return this.datePipe.transform(date, 'mediumDate') ?? '';
//       }


//       get rowsLength(): number {
//         return this.cmArray.value.length;
//       }



//       onPageChange(newPage: number): void {
//         this.page = newPage;
//       }


// }


/* eslint-disable @typescript-eslint/no-explicit-any */
// import {
//   Component, Input, ViewChild, TemplateRef,
//   OnInit, OnChanges, SimpleChanges, inject
// } from '@angular/core';
// import {
//   FormArray, FormBuilder, FormGroup, Validators
// } from '@angular/forms';
// import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
// import { Column, Sort } from 'src/app/layout/table/table.types';
// import { ControlMeasureAssignment } from '../../../models/control‑measure‑assignment.model';

// /* ───────── helper types ───────── */
// type CmItem   = { public_id:number; title:string; identifier:string };
// type RespType = 'PERSON' | 'PERSON_GROUP';
// interface RespItem {
//   public_id   : number;
//   display_name: string;
//   group       : string;
//   type        : RespType;
// }

// @Component({
//   selector   : 'ra-cm-assignment-inline',
//   templateUrl: './ra-cm-assignment-inline.component.html',
//   styleUrls  : ['./ra-cm-assignment-inline.component.scss']
// })
// export class RaCmAssignmentInlineComponent implements OnInit, OnChanges {

//   /* ───────── inputs ───────── */
//   @Input({ required:true }) parentForm!: FormGroup;
//   @Input() createMode = true;
//   @Input() allControlMeasures : CmItem[] = [];
//   @Input() implementationStates: { public_id:number; value:string }[] = [];
//   @Input() allPersons         : any[] = [];
//   @Input() allPersonGroups    : any[] = [];

//   /* ───────── template refs ───────── */
//   @ViewChild('modalTpl',     { static:true }) modalTpl!    : TemplateRef<any>;
//   @ViewChild('cmActionsTpl', { static:true }) cmActionsTpl!: TemplateRef<any>;

//   /* ───────── DI ───────── */
//   private readonly fb    = inject(FormBuilder);
//   private readonly modal = inject(NgbModal);

//   /* ───────── maps ───────── */
//   private readonly cmMap  = new Map<number, { title:string; identifier:string }>();
//   private readonly stsMap = new Map<number, string>();

//   /* ───────── dropdown helpers ───────── */
//   readonly priorityOptions = [
//     { label:'Low', value:1 }, { label:'Medium', value:2 },
//     { label:'High', value:3 }, { label:'Very High', value:4 }
//   ];
//   responsibleOptions: RespItem[] = [];
//   availableControlMeasures: CmItem[] = [];

//   /* ───────── modal bookkeeping ───────── */
//   modalRef!  : NgbModalRef;
//   modalForm! : FormGroup;
//   editIndex  : number|null|undefined;
//   modalMode  : 'add'|'edit'|'view' = 'add';

//   /* ───────── table helpers ───────── */
//   columns!: Column[];
//   page    = 1;

//   /* ═════════════════════════ lifecycle ═════════════════════════ */
//   ngOnInit(): void {
//     this.buildMaps();
//     this.buildResponsibleOptions();
//     this.updateAvailableControlMeasures();
//     this.initColumns();
//   }

//   ngOnChanges(ch: SimpleChanges): void {
//     if (ch['allControlMeasures'] && !ch['allControlMeasures'].firstChange) {
//       this.buildMaps();
//       this.updateAvailableControlMeasures();
//     }
//   }

//   /* ═════════════════════ helpers ═════════════════════ */
//   private buildMaps(): void {
//     this.cmMap.clear();
//     this.allControlMeasures.forEach(cm => this.cmMap.set(cm.public_id, {
//       title      : cm.title,
//       identifier : cm.identifier
//     }));
//     this.stsMap.clear();
//     this.implementationStates.forEach(st => this.stsMap.set(st.public_id, st.value));
//   }

//   /** build list *with literal types* so TS knows `'PERSON_GROUP' | 'PERSON'` */
//   private buildResponsibleOptions(): void {
//     const groups : RespItem[] = this.allPersonGroups.map(pg => ({
//       public_id   : pg.public_id,
//       display_name: pg.name,
//       group       : 'Groups',
//       type        : 'PERSON_GROUP' as const          // <- literal
//     }));
//     const persons: RespItem[] = this.allPersons.map(p => ({
//       public_id   : p.public_id,
//       display_name: p.display_name,
//       group       : 'Persons',
//       type        : 'PERSON' as const                // <- literal
//     }));
//     this.responsibleOptions = [...groups, ...persons];
//   }

//   private getResponsibleType(id:number): RespType {
//     return this.responsibleOptions.find(o => o.public_id === id)?.type ?? 'PERSON';
//   }

//   private initColumns(): void {
//     this.columns = [
//       { display:'Identifier',  name:'ident', data:'identifier',      sortable:true  },
//       { display:'Control Name',name:'title', data:'title',           sortable:true  },
//       { display:'Responsible', name:'resp',  data:'responsibleLabel'                },
//       { display:'Status',      name:'stat',  data:'statusLabel'                     },
//       {
//         display:'Actions',
//         name   :'act',
//         data   :'dummy',
//         template: this.cmActionsTpl,
//         sortable:false,
//         fixed:true,
//         style  : { width:'100px', 'text-align':'center' }
//       }
//     ];
//   }

//   /* ═════════════════════ form array ═════════════════════ */
//   private get cmArray(): FormArray {
//     if (!this.parentForm.get('control_measure_assignments')) {
//       this.parentForm.addControl('control_measure_assignments', new FormArray([]));
//     }
//     return this.parentForm.get('control_measure_assignments') as FormArray;
//   }

//   /* ═════════════════════ table rows ═════════════════════ */
//   get rowsLength(): number { return this.cmArray.length; }

//   get tableRows(): any[] {
//     return this.cmArray.controls.map(ctrl => {
//       const a = ctrl.value as ControlMeasureAssignment;
//       const cm = this.cmMap.get(a.control_measure_id);
//       return {
//         ...a,
//         identifier       : cm?.identifier ?? `#${a.control_measure_id}`,
//         title            : cm?.title      ?? '',
//         responsibleLabel : this.responsibleOptions.find(r => r.public_id === a.responsible_for_implementation_id)?.display_name ?? '',
//         statusLabel      : this.stsMap.get(a.implementation_status) ?? a.implementation_status
//       };
//     });
//   }

//   /* ═════════════════════ pagination & sort stubs ═════════════════════ */
//   onPageChange(p:number): void { this.page = p; }
//   onSort(_s:Sort): void {}

//   /* ═════════════════════ modal helpers ═════════════════════ */
//   private buildModalForm(seed?: Partial<ControlMeasureAssignment>): FormGroup {
//     return this.fb.group({
//       control_measure_id                       : [seed?.control_measure_id ?? null, Validators.required],
//       planned_implementation_date              :  seed?.planned_implementation_date ?? null,
//       implementation_status                    : [seed?.implementation_status ?? null, Validators.required],
//       finished_implementation_date             :  seed?.finished_implementation_date ?? null,
//       priority                                 :  seed?.priority ?? null,
//       responsible_for_implementation_id_ref_type: [seed?.responsible_for_implementation_id_ref_type ?? 'PERSON'],
//       responsible_for_implementation_id        : [seed?.responsible_for_implementation_id ?? null, Validators.required]
//     });
//   }

//   private updateAvailableControlMeasures(currentId?: number): void {
//     const used = new Set(this.cmArray.controls.map(c => c.value.control_measure_id));
//     if (currentId != null) used.delete(currentId); // keep current selectable
//     this.availableControlMeasures = this.allControlMeasures
//       .filter(cm => !used.has(cm.public_id))
//       .sort((a, b) => a.title.localeCompare(b.title));
//   }

//   /* -------------------- open modal -------------------- */
//   openModal(idx?: number, mode: 'add'|'edit'|'view' = 'add'): void {
//     this.modalMode = mode;
//     this.editIndex = idx ?? null;

//     const seed = idx != null ? { ...this.cmArray.at(idx).getRawValue() } : undefined;
//     this.modalForm = this.buildModalForm(seed);

//     if (mode === 'view') { this.modalForm.disable(); }
//     this.updateAvailableControlMeasures(seed?.control_measure_id);

//     this.modalRef = this.modal.open(this.modalTpl, {
//       size:'lg', centered:true, backdrop:'static', windowClass:'dg-modal'
//     });
//   }

//   /* -------------------- save -------------------- */
//   saveAssignment(): void {
//     if (this.modalForm.invalid) { return; }

//     const value = this.modalForm.getRawValue();
//     value.responsible_for_implementation_id_ref_type =
//       this.getResponsibleType(value.responsible_for_implementation_id);

//     /* prevent duplicates (ignore self while editing) */
//     const duplicate = this.cmArray.controls.find((c, i) =>
//       c.value.control_measure_id === value.control_measure_id && i !== this.editIndex);
//     if (duplicate) { return; }  // ideally show toast - omitted for brevity

//     if (this.editIndex != null) {
//       this.cmArray.at(this.editIndex).patchValue(value);
//     } else {
//       this.cmArray.push(this.fb.group(value));
//     }
//     this.closeModal();
//     this.updateAvailableControlMeasures();
//   }

//   /* -------------------- close -------------------- */
//   closeModal(): void {
//     this.modalRef.close();
//     this.modalMode = 'add';
//     this.editIndex = undefined;
//     this.modalForm.enable();
//   }

//   /* -------------------- row actions -------------------- */
//   onEditRow(row:any): void {
//     const idx = this.cmArray.controls.findIndex(c => c.value.control_measure_id === row.control_measure_id);
//     if (idx !== -1) { this.openModal(idx, 'edit'); }
//   }
//   onViewRow(row:any): void {
//     const idx = this.cmArray.controls.findIndex(c => c.value.control_measure_id === row.control_measure_id);
//     if (idx !== -1) { this.openModal(idx, 'view'); }
//   }
//   deleteRow(row:any): void {
//     const idx = this.cmArray.controls.findIndex(c => c.value.control_measure_id === row.control_measure_id);
//     if (idx !== -1) {
//       this.cmArray.removeAt(idx);
//       this.updateAvailableControlMeasures();
//     }
//   }
// }


import {
  Component, Input, ViewChild, TemplateRef,
  OnInit, OnChanges, SimpleChanges, inject,
  AfterViewInit
} from '@angular/core';
import {
  FormArray, FormGroup, Validators, NonNullableFormBuilder
} from '@angular/forms';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { Column, Sort } from 'src/app/layout/table/table.types';
import { ControlMeasureAssignment } from '../../../models/control‑measure‑assignment.model';


/* ───────── helper types ───────── */
type CmItem   = { public_id:number; title:string; identifier:string };
type RespType = 'PERSON' | 'PERSON_GROUP';
interface RespItem {
  public_id   : number;
  display_name: string;
  group       : string;
  type        : RespType;
}

@Component({
  selector   : 'ra-cm-assignment-inline',
  templateUrl: './ra-cm-assignment-inline.component.html',
  styleUrls  : ['./ra-cm-assignment-inline.component.scss']
})
export class RaCmAssignmentInlineComponent implements OnInit, OnChanges, AfterViewInit {

  /* ───────── inbound data ───────── */
  @Input({ required:true }) parentForm!: FormGroup;
  /** When `false`, component runs in *edit / view* context */
  @Input() createMode = true;
  /** Full CM list */
  @Input() allControlMeasures : CmItem[] = [];
  /** Implementation-state list */
  @Input() implementationStates: { public_id:number; value:string }[] = [];
  /** Person / group master data */
  @Input() allPersons      : any[] = [];
  @Input() allPersonGroups : any[] = [];
  @Input() riskAssessmentId?: number;


  /* ───────── template refs ───────── */
  @ViewChild('modalTpl',     { static:true }) modalTpl!: TemplateRef<any>;
  @ViewChild('cmActionsTpl', { static:true }) cmActionsTpl!: TemplateRef<any>;

  /* ───────── DI ───────── */
  private readonly fb    = inject(NonNullableFormBuilder);
  private readonly modal = inject(NgbModal);

  /* ───────── lookup maps ───────── */
  private readonly cmMap  = new Map<number,CmItem>();
  private readonly stsMap = new Map<number,string>();

  /* ───────── dropdown helpers ───────── */
  readonly priorityOptions = [
    { label:'Low', value:1 }, { label:'Medium', value:2 },
    { label:'High', value:3 }, { label:'Very High', value:4 }
  ];
  responsibleOptions: RespItem[] = [];
  availableControlMeasures: CmItem[] = [];

  /* ───────── modal bookkeeping ───────── */
  private modalRef!: NgbModalRef;
  modalForm!: FormGroup;
  editIndex : number|null|undefined;
  modalMode : 'add'|'edit'|'view' = 'add';

  /* ───────── change-tracking (edit-mode) ───────── */
  private originalSnapshot: ControlMeasureAssignment[] = [];

  /* ───────── table helpers ───────── */
  columns!: Column[];
  page = 1;

  /* ═════════════════════════ lifecycle ═════════════════════════ */
  ngOnInit(): void {
    this.buildMaps();
    this.buildResponsibleOptions();
    this.initColumns();
    this.ensureCmArrayExists();

    /* keep pristine copy for diff-calculation (edit / view only) */
    if (!this.createMode) {
      this.originalSnapshot = structuredClone(this.cmArray.value) as ControlMeasureAssignment[];
    }

    this.modalForm = this.buildModalForm();           // create once
    this.updateAvailableControlMeasures();

  }

  ngOnChanges(ch: SimpleChanges): void {
    if (ch['allControlMeasures'] && !ch['allControlMeasures'].firstChange){
      this.buildMaps();
      this.updateAvailableControlMeasures();
    }
  }


  ngAfterViewInit() {
    console.log('createMode:', this.createMode);
  }

  /* ═════════════════════ build-helpers ═════════════════════ */
  private buildMaps():void{
    this.cmMap.clear();
    this.allControlMeasures.forEach(cm => this.cmMap.set(cm.public_id, cm));
    this.stsMap.clear();
    this.implementationStates.forEach(s => this.stsMap.set(s.public_id, s.value));
  }

  private buildResponsibleOptions():void{
    const groups : RespItem[] = this.allPersonGroups.map(pg=>({
      public_id:pg.public_id, display_name:pg.name,
      group:'Groups', type:'PERSON_GROUP'
    }));
    const persons: RespItem[] = this.allPersons.map(p=>({
      public_id:p.public_id, display_name:p.display_name,
      group:'Persons', type:'PERSON'
    }));
    this.responsibleOptions = [...groups, ...persons];
  }
  private getRespType(id:number):RespType{
    return this.responsibleOptions.find(r=>r.public_id===id)?.type ?? 'PERSON';
  }

  private initColumns():void{
    this.columns = [
      { display:'Identifier',  name:'ident', data:'identifier',      sortable:true },
      { display:'Control Name',name:'title', data:'title',           sortable:true },
      { display:'Responsible', name:'resp',  data:'responsibleLabel'               },
      { display:'Status',      name:'stat',  data:'statusLabel'                    },
      {
        display:'Actions',     name:'act',   data:'dummy',
        template:this.cmActionsTpl, fixed:true,
        style:{width:'95px','text-align':'center'}
      }
    ];
  }

  /* ═════════════════════ form-array helpers ═════════════════════ */
  private get cmArray():FormArray{
    return this.parentForm.get('control_measure_assignments') as FormArray;
  }
  private ensureCmArrayExists():void{
    if (!this.parentForm.get('control_measure_assignments')){
      this.parentForm.addControl('control_measure_assignments', this.fb.array([]));
    }
  }

  /* ═════════════════════ table rows ═════════════════════ */
  get rowsLength():number { return this.cmArray.length; }
  get tableRows():any[]{
    return this.cmArray.controls.map(ctrl=>{
      const v  = ctrl.value as ControlMeasureAssignment;
      const cm = this.cmMap.get(v.control_measure_id);
      return {
        ...v,
        identifier      : cm?.identifier ?? `#${v.control_measure_id}`,
        title           : cm?.title ?? '',
        responsibleLabel: this.responsibleOptions.find(r=>r.public_id===v.responsible_for_implementation_id)?.display_name ?? '',
        statusLabel     : this.stsMap.get(v.implementation_status) ?? v.implementation_status
      };
    });
  }
  onPageChange(p:number){ this.page = p; }
  onSort(_:Sort){}

  /* ═════════════════════ modal-helpers ═════════════════════ */
  private buildModalForm(seed?:Partial<ControlMeasureAssignment>):FormGroup{
    return this.fb.group({
      control_measure_id:                      [seed?.control_measure_id ?? null, Validators.required],
      planned_implementation_date:              seed?.planned_implementation_date ?? null,
      implementation_status:                   [seed?.implementation_status ?? null, Validators.required],
      finished_implementation_date:             seed?.finished_implementation_date ?? null,
      priority:                                 seed?.priority ?? null,
      responsible_for_implementation_id_ref_type:[seed?.responsible_for_implementation_id_ref_type ?? 'PERSON'],
      responsible_for_implementation_id:       [seed?.responsible_for_implementation_id ?? null, Validators.required]
    });
  }

  public updateAvailableControlMeasures(currentId?:number):void{
    const used = new Set<number>(this.cmArray.value.map(
        (x:ControlMeasureAssignment)=>x.control_measure_id));
    if(currentId!=null){ used.delete(currentId); }
    this.availableControlMeasures = this.allControlMeasures
      .filter(cm=>!used.has(cm.public_id))
      .sort((a,b)=>a.title.localeCompare(b.title));
  }

  /* -------- open modal ------- */
  openModal(idx?:number, mode:'add'|'edit'|'view'='add'):void{
    this.modalMode = mode;
    this.editIndex = idx ?? null;

    const seed = idx!=null ? { ...this.cmArray.at(idx).getRawValue() } : undefined;
    this.modalForm.reset();
    this.modalForm.patchValue(seed ?? {});
    (mode==='view') ? this.modalForm.disable() : this.modalForm.enable();

    this.updateAvailableControlMeasures(seed?.control_measure_id);

    queueMicrotask(()=>{
      this.modalRef = this.modal.open(this.modalTpl,
        { size:'lg', centered:true, backdrop:'static', windowClass:'dg-modal' });
    });
  }

  /* -------- save ------- */
  saveAssignment():void{
    if(this.modalForm.invalid){ return; }

    const val = this.modalForm.getRawValue();
    val.responsible_for_implementation_id_ref_type =
      this.getRespType(val.responsible_for_implementation_id);

      if (this.riskAssessmentId) {
        (val as any).risk_assessment_id = this.riskAssessmentId;
      }

    /* prevent duplicates */
    const dup = this.cmArray.controls.find((c,i)=>
      c.value.control_measure_id===val.control_measure_id && i!==this.editIndex);
    if(dup){ return; }

    if(this.editIndex!=null){
      this.cmArray.at(this.editIndex).patchValue(val);
    }else{
      /* remove public_id if user somehow typed it in */
      delete (val as any).public_id;
      this.cmArray.push(this.fb.group(val));
    }
    this.closeModal();
    this.updateAvailableControlMeasures();
  }

  /* -------- close ------- */
  closeModal():void{
    this.modalRef?.close();
    this.modalMode='add';
    this.editIndex=undefined;
    this.modalForm.enable();
  }

  /* -------- row actions ------- */
  onEditRow(r:any){ this.openModal(this.rowIndex(r),'edit'); }
  onViewRow(r:any){ this.openModal(this.rowIndex(r),'view'); }
  deleteRow(r:any){
    const idx=this.rowIndex(r);
    if(idx!==-1){ this.cmArray.removeAt(idx); this.updateAvailableControlMeasures(); }
  }
  private rowIndex(r:any):number{
    return this.cmArray.controls.findIndex(c=>c.value.control_measure_id===r.control_measure_id);
  }

  /* ═════════════════════ PUBLIC: build payload ═════════════════════ */
  /** Call this from the parent *once* just before saving RA */
  buildAssignmentsPayload():{
    created: any[],
    updated: any[],
    deleted: number[]
  }{
    const current = this.cmArray.value as ControlMeasureAssignment[];

    /* helper maps */
    const origById = new Map<number,ControlMeasureAssignment>(
      this.originalSnapshot.filter(o=>o.public_id!=null)
                           .map(o=>[o.public_id!,o]));
    const curById  = new Map<number,ControlMeasureAssignment>(
      current.filter(c=>c.public_id!=null).map(c=>[c.public_id!,c]));

    /* created */
    const created = current.filter(c => c.public_id == null)
                           .map(c => ({ ...c })); // keep shape – NO public_id

    /* updated */
    const updated: ControlMeasureAssignment[] = [];
    curById.forEach((cur, id)=>{
      const orig = origById.get(id);
      if(orig && JSON.stringify(orig) !== JSON.stringify(cur)){
        updated.push(cur);
      }
    });

    /* deleted */
    const deleted: number[] = [];
    origById.forEach((_v,id)=>{
      if(!curById.has(id)){ deleted.push(id); }
    });

    return { created, updated, deleted };
  }

  public markSnapshot(): void {
    this.originalSnapshot = structuredClone(
      this.cmArray.value
    ) as ControlMeasureAssignment[];
  }

   public refreshSnapshot(): void {
       this.originalSnapshot = structuredClone(this.cmArray.value) as ControlMeasureAssignment[];
     }
}
