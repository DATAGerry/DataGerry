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

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import {
    Component,
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    AfterViewInit,
    Input,
} from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { GraphNode } from '../interfaces/graph.interfaces';
import { LAYOUT_CONFIG } from '../constants/graph.constants';

function normalise(v: unknown): unknown {
    return v === null || v === undefined || v === '' ? 'N/A' : v;
}

@Component({
    selector: 'app-node-details-modal',
    templateUrl: './node-details-modal.component.html',
    styleUrls: ['./node-details-modal.component.scss'],
    changeDetection: ChangeDetectionStrategy.Default,
})
export class NodeDetailsModalComponent implements AfterViewInit {
    readonly LAYOUT_CONFIG = LAYOUT_CONFIG;

    /** always-rendered array; we fill it in loadNode() */
    customFields: Array<{ key: string; value: any }> = [];

    /** guard to know when view is ready */
    private viewInit = false;

    private _node: GraphNode | null = null;
    get node(): GraphNode | null {
        return this._node;
    }

    /** call this _after_ open() to populate data */
    loadNode(n: GraphNode | null): void {
        this._node = n;

        const built: Array<{ key: string; value: any }> = [];
        (n?.fields ?? []).forEach((f, i) =>
            built.push({ key: f.name ?? `field ${i + 1}`, value: normalise(f.value) })
        );
        (n?.metadata ?? []).forEach((m, i) =>
            built.push({ key: m.name ?? `meta ${i + 1}`, value: normalise(m.value) })
        );

        // new reference to force change detection
        this.customFields = [...built];

        if (this.viewInit) {
            this.cdr.detectChanges();
        }
    }

    constructor(
        public activeModal: NgbActiveModal,
        private cdr: ChangeDetectorRef
    ) { }

    ngAfterViewInit(): void {
        this.viewInit = true;
        // if loadNode was called before viewInit, we need one render now
        this.cdr.detectChanges();
    }

    /** font-awesome icon lookup */
    getNodeTypeIcon(type?: string | null): string {
        return (
            this.nodeTypeConfigs?.get(type!)?.icon ||
            'fas fa-question'
        );
    }

    trackByKey(_: number, f: { key: string }): string {
        return f.key;
    }

    @Input() nodeTypeConfigs:
        | Map<string, { icon: string; gradient: string }>
        | null = null;
}
