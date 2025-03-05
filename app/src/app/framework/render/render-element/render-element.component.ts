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
    Component,
    ComponentFactoryResolver,
    ComponentRef,
    Input,
    OnInit,
    ViewChild,
    ViewContainerRef
} from '@angular/core';
import { UntypedFormControl, Validators } from '@angular/forms';
import { ToastService } from '../../../layout/toast/toast.service';
import { fieldComponents } from '../fields/fields.list';
import { simpleComponents } from '../simple/simple.list';
import { RenderFieldComponent } from '../fields/components.fields';
import { CmdbMode } from '../../modes.enum';

@Component({
    selector: 'cmdb-render-element',
    templateUrl: './render-element.component.html',
    styleUrls: ['./render-element.component.scss']
})
export class RenderElementComponent extends RenderFieldComponent implements OnInit {
    @ViewChild('fieldContainer', { read: ViewContainerRef, static: true }) containerField;

    @Input() objectID: number;
    //if true, use the parent's control value as initial value.
    @Input() useInitialValueFromParent: boolean = false;

    public simpleRender: boolean = false;
    private component: any;
    private componentRef: ComponentRef<any>;

    /* ------------------------------------------------------------------------------------------------------------------ */
    /*                                                     LIFE CYCLE                                                     */
    /* ------------------------------------------------------------------------------------------------------------------ */

    constructor(
        private resolver: ComponentFactoryResolver,
        public toast: ToastService
    ) {
        super();
    }

    public ngOnInit(): void {
        this.containerField.clear();

        switch (this.mode) {
            case CmdbMode.View:
            case CmdbMode.Create:
            case CmdbMode.Edit:
            case CmdbMode.Bulk: {
                this.simpleRender = false;
                this.component = fieldComponents[this.data.type];
                const factory = this.resolver.resolveComponentFactory(this.component);
                this.componentRef = this.containerField.createComponent(factory);
                this.componentRef.instance.parentFormGroup = this.parentFormGroup;
                this.componentRef.instance.data = this.data;
                this.componentRef.instance.mode = this.mode;
                this.componentRef.instance.section = this.section;
                this.componentRef.instance.objectID = this.objectID;
                this.componentRef.instance.toast = this.toast;

                // Determine the initial value conditionally:
                let initialValue: any;
                if (this.useInitialValueFromParent) {
                    // If flag true, use value from parent's form control if exists; otherwise fallback.
                    initialValue = this.parentFormGroup.get(this.data.name)
                        ? this.parentFormGroup.get(this.data.name).value
                        : this.value;
                } else {
                    // Default behavior: use this.value.
                    initialValue = this.value;
                }

                // Create the form control with the determined initial value.
                const fieldControl = new UntypedFormControl(initialValue);
                const validators = [];

                if ((this.mode === CmdbMode.View || this.mode === CmdbMode.Edit) && (initialValue == null)) {
                    fieldControl.patchValue(this.value);
                }

                if (this.data.required) {
                    validators.push(Validators.required);
                }

                if (this.data.regex) {
                    validators.push(Validators.pattern(this.data.regex));
                }

                fieldControl.setValidators(validators);

                if (this.mode === CmdbMode.View) {
                    fieldControl.disable();
                }

                if (this.data.disabled) {
                    fieldControl.disable();
                }

                this.parentFormGroup.removeControl(this.data.name);
                this.componentRef.instance.parentFormGroup.addControl(
                    this.data.name, fieldControl
                );

                if (this.mode === CmdbMode.Bulk) {
                    this.componentRef.instance.changeForm = this.changeForm;
                }
                break;
            }
            case CmdbMode.Simple: {
                if (!this.data) break;
                this.data.value = this.value;
                this.component = simpleComponents[this.data.type];
                const factory = this.resolver.resolveComponentFactory(this.component);
                this.componentRef = this.containerField.createComponent(factory);
                this.componentRef.instance.mode = this.mode;
                this.componentRef.instance.data = this.data;
                this.componentRef.instance.toast = this.toast;
                break;
            }
        }
    }
}
