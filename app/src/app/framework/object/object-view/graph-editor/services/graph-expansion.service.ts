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
import { Injectable } from '@angular/core';
import {
    CINode,
    GraphRespChildren,
    GraphRespParents
} from 'src/app/framework/models/ci-explorer.model';
import { GraphNode, Connection } from '../interfaces/graph.interfaces';
import { GraphDataService } from './graph-data.service';
import { firstValueFrom } from 'rxjs';


@Injectable()
export class GraphExpansionService {

    constructor(private graphData: GraphDataService) { }

    async expandNodeInstance(
        ui: GraphNode,
        cn: CINode,
        nodes: GraphNode[],
        connections: Connection[],
        typesFilter: number[],
        relationsFilter: number[],
        nodeTypeConfigs: Map<string, { icon: string; gradient: string }>
    ): Promise<void> {
        ui.isLoading = true;
        ui.expanded = true;

        try {
            await this.fetchAndAttach(cn, ui, nodes, connections, typesFilter, relationsFilter, nodeTypeConfigs);
        } finally {
            ui.isLoading = false;
        }
    }

    collapseNodeInstance(
        ui: GraphNode,
        nodes: GraphNode[],
        connections: Connection[]
    ): void {
        const victims = this.getDescendantInstancesFromSpecificNode(ui, nodes, connections);
        const uidsToRemove = victims?.map(n => n.uid);
        this.graphData?.removeNodeInstancesByUID(nodes, connections, uidsToRemove);
        ui.expanded = false;
    }

    private async fetchAndAttach(
        cn: CINode,
        ui: GraphNode,
        nodes: GraphNode[],
        connections: Connection[],
        typesFilter: number[],
        relationsFilter: number[],
        nodeTypeConfigs: Map<string, { icon: string; gradient: string }>
    ): Promise<void> {
        const id = cn?.linked_object?.public_id;
        this.graphData?.setSkipBackendEdges(true);

        const wantType = (n: CINode) =>
            typesFilter?.length === 0 ||
            typesFilter?.includes(n?.type_info?.type_id);

        try {
            const newUIDs: string[] = [];

            // PARENTS (level -1, -2, …)
            if ((cn as any)?.direction === 'parent' || (cn as any)?.direction === 'root') {
                // const res: GraphRespParents = await this.graphData.expandParent(
                //   id,
                //   typesFilter,
                //   relationsFilter
                // ).toPromise();

                const res: GraphRespParents = await firstValueFrom(
                    this.graphData?.expandParent(id, typesFilter, relationsFilter)
                );
                const parents = this.graphData?.getNodes(res, 'parent')?.filter(wantType);
                parents?.forEach(p => { p.level = ui?.level - 1; (p as any).direction = 'parent'; });

                const before = nodes?.length;
                this.graphData?.mergeNodes(nodes, parents, nodeTypeConfigs);
                const added = nodes?.slice(before);

                added?.forEach(p => {
                    connections.push({
                        from: id, to: id,
                        fromLevel: p?.level, toLevel: ui?.level,
                        fromUid: p?.uid, toUid: ui?.uid,
                        relationLabel: 'parent',
                        relationColor: cn?.relation_color,
                        isValid: true, strength: 1
                    });
                    newUIDs.push(p?.uid);
                });
            }

            // CHILDREN (level +1, +2, …)
            if ((cn as any).direction === 'child' || (cn as any).direction === 'root') {
                // const res: GraphRespChildren = await this.graphData.expandChild(
                //   id,
                //   typesFilter,
                //   relationsFilter
                // ).toPromise();

                const res: GraphRespChildren = await firstValueFrom(
                    this.graphData?.expandChild(id, typesFilter, relationsFilter)
                );

                const kids = this.graphData?.getNodes(res, 'child').filter(wantType);
                kids.forEach(k => { k.level = ui?.level + 1; (k as any).direction = 'child'; });

                const before = nodes?.length;
                this.graphData?.mergeNodes(nodes, kids, nodeTypeConfigs);
                const added = nodes?.slice(before);

                added?.forEach(k => {
                    connections.push({
                        from: id, to: id,
                        fromLevel: ui?.level, toLevel: k?.level,
                        fromUid: ui?.uid, toUid: k?.uid,
                        relationLabel: 'child',
                        relationColor: cn?.relation_color,
                        isValid: true, strength: 1
                    });
                    newUIDs.push(k?.uid);
                });
            }


        } catch (err) {
            console.error('expand error', err);
            ui.expanded = false;
        } finally {
            this.graphData?.setSkipBackendEdges(false);
        }
    }

    private getDescendantInstancesFromSpecificNode(
        root: GraphNode,
        nodes: GraphNode[],
        connections: Connection[]
    ): GraphNode[] {
        const nodeInstanceMap = this.graphData?.getNodeInstanceMap();
        const followOutgoing = root?.level >= 0;
        const isFurtherAway = (lvl: number) =>
            followOutgoing ? lvl > root?.level : lvl < root?.level;

        const q: GraphNode[] = [];
        const out: GraphNode[] = [];
        const seen = new Set<string>();

        // Seed the queue with the first hop
        connections
            .filter(c => c?.isValid && (
                followOutgoing ? c?.fromUid === root?.uid : c?.toUid === root?.uid))
            .forEach(c => {
                const nextUid = followOutgoing ? c?.toUid! : c?.fromUid!;
                const n = nodeInstanceMap?.get(nextUid);
                if (n && isFurtherAway(n?.level)) { q?.push(n); }
            });

        // BFS along the proper direction
        while (q?.length) {
            const cur = q?.shift()!;
            if (seen?.has(cur?.uid)) { continue; }
            seen?.add(cur?.uid);
            out.push(cur);

            connections
                ?.filter(c => c?.isValid && (
                    followOutgoing ? c?.fromUid === cur?.uid : c?.toUid === cur?.uid))
                ?.forEach(c => {
                    const nextUid = followOutgoing ? c?.toUid! : c?.fromUid!;
                    const n = nodeInstanceMap?.get(nextUid);
                    if (n && isFurtherAway(n?.level) && !seen?.has(n?.uid)) {
                        q?.push(n);
                    }
                });
        }

        return out;
    }
}