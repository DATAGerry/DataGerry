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
import { Injectable, ElementRef } from '@angular/core';
import { GraphNode } from '../interfaces/graph.interfaces';
import { LAYOUT_CONFIG } from '../constants/graph.constants';

@Injectable()
export class GraphViewportService {
    private viewportX = 0;
    private viewportY = 0;
    private zoom = 0.65;
    private targetZoom = 0.65;

    getViewportX(): number { return this.viewportX; }
    getViewportY(): number { return this.viewportY; }
    getZoom(): number { return this.zoom; }
    getTargetZoom(): number { return this.targetZoom; }

    setViewport(x: number, y: number): void {
        this.viewportX = x;
        this.viewportY = y;
    }

    setZoom(zoom: number): void {
        this.zoom = zoom;
        this.targetZoom = zoom;
    }

    centerViewport(graphContainer: ElementRef | undefined, nodes: GraphNode[]): void {
        if (!graphContainer) return;
        const container = graphContainer?.nativeElement;
        const rect = container?.getBoundingClientRect();

        if (nodes.length > 0) {
            const bounds = this.getNodeBounds(nodes, new Set());
            const centerX = (bounds?.minX + bounds?.maxX) / 2;
            const centerY = (bounds?.minY + bounds?.maxY) / 2;
            this.viewportX = rect?.width / 2 - centerX * this.zoom;
            this.viewportY = rect?.height / 2 - centerY * this.zoom;
        }
    }

    getNodeBounds(nodes: GraphNode[], selectedNodes: Set<number>): { minX: number; maxX: number; minY: number; maxY: number } {
        if (nodes?.length === 0) {
            return { minX: 0, maxX: 800, minY: 0, maxY: 600 };
        }

        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
        const nodesToConsider = selectedNodes?.size > 0
            ? nodes?.filter(n => selectedNodes?.has(n?.id))
            : nodes;

        if (nodesToConsider?.length === 0) {
            return { minX: 0, maxX: 800, minY: 0, maxY: 600 };
        }

        nodesToConsider?.forEach(node => {
            if (isFinite(node?.x) && isFinite(node?.y)) {
                minX = Math.min(minX, node?.x);
                maxX = Math.max(maxX, node?.x + LAYOUT_CONFIG?.nodeWidth);
                minY = Math.min(minY, node?.y);
                maxY = Math.max(maxY, node?.y + LAYOUT_CONFIG?.nodeHeight);
            }
        });

        if (!isFinite(minX)) {
            return { minX: 0, maxX: 800, minY: 0, maxY: 600 };
        }

        return { minX, maxX, minY, maxY };
    }

    zoomIn(): void {
        this.targetZoom = Math.min(this.zoom * 1.2, 3);
        this.animateZoom();
    }

    zoomOut(): void {
        this.targetZoom = Math.max(this.zoom / 1.2, 0.3);
        this.animateZoom();
    }

    resetZoom(graphContainer?: ElementRef, nodes?: GraphNode[]): void {
        this.targetZoom = 0.75;
        this.animateZoom();
        if (graphContainer && nodes) {
            this.centerViewport(graphContainer, nodes);
        }
    }

    setZoomWithDelta(delta: number): void {
        this.targetZoom = Math.max(0.3, Math.min(3, this.zoom * delta));
        this.animateZoom();
    }

    private animateZoom(): void {
        const duration = 200;
        const startZoom = this.zoom;
        const startTime = performance?.now();

        const animate = (currentTime: number) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            this.zoom = startZoom + (this.targetZoom - startZoom) * easeProgress;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }

    centerOnNode(node: GraphNode, graphContainer: ElementRef): void {
        if (!graphContainer) return;
        const container = graphContainer?.nativeElement;
        const rect = container?.getBoundingClientRect();
        const nodeX = node?.x + LAYOUT_CONFIG?.nodeWidth / 2;
        const nodeY = node?.y + LAYOUT_CONFIG?.nodeHeight / 2;
        this.viewportX = rect?.width / 2 - nodeX * this.zoom;
        this.viewportY = rect?.height / 2 - nodeY * this.zoom;
    }

    shouldShowNode(node: GraphNode, nodeCount: number, graphContainer?: ElementRef): boolean {
        if (nodeCount <= 500) return true;

        const container = graphContainer?.nativeElement;
        if (!container) return true;

        const rect = container?.getBoundingClientRect();
        const nodeScreenX = node?.x * this.zoom + this.viewportX;
        const nodeScreenY = node?.y * this.zoom + this.viewportY;
        const nodeWidth = LAYOUT_CONFIG?.nodeWidth * this.zoom;
        const nodeHeight = LAYOUT_CONFIG?.nodeHeight * this.zoom;

        const padding = 100;
        return nodeScreenX + nodeWidth > -padding &&
            nodeScreenX < rect?.width + padding &&
            nodeScreenY + nodeHeight > -padding &&
            nodeScreenY < rect?.height + padding;
    }

    // Minimap helpers
    getMinimapViewBox(nodes: GraphNode[]): string {
        if (nodes.length === 0) {
            return "0 0 800 600";
        }
        const bounds = this.getNodeBounds(nodes, new Set());
        const padding = 100;
        const minX = isFinite(bounds.minX) ? bounds?.minX : 0;
        const minY = isFinite(bounds.minY) ? bounds?.minY : 0;
        const maxX = isFinite(bounds.maxX) ? bounds?.maxX : 800;
        const maxY = isFinite(bounds.maxY) ? bounds?.maxY : 600;
        return `${minX - padding} ${minY - padding} ${maxX - minX + 2 * padding} ${maxY - minY + 2 * padding}`;
    }

    getMinimapViewportRect(graphContainer?: ElementRef): any {
        if (!graphContainer) return null;
        const container = graphContainer?.nativeElement;
        const rect = container?.getBoundingClientRect();
        return {
            x: -this.viewportX / this.zoom,
            y: -this.viewportY / this.zoom,
            width: rect.width / this.zoom,
            height: rect.height / this.zoom,
        };
    }

    onMinimapClick(event: MouseEvent, nodes: GraphNode[], graphContainer: ElementRef): void {
        const minimap = event?.currentTarget as SVGElement;
        const rect = minimap?.getBoundingClientRect();
        const x = (event?.clientX - rect?.left) / rect?.width;
        const y = (event?.clientY - rect?.top) / rect?.height;
        const bounds = this.getNodeBounds(nodes, new Set());
        const targetX = bounds?.minX + (bounds?.maxX - bounds?.minX) * x;
        const targetY = bounds?.minY + (bounds?.maxY - bounds?.minY) * y;
        const container = graphContainer?.nativeElement;
        const containerRect = container?.getBoundingClientRect();
        this.viewportX = containerRect?.width / 2 - targetX * this.zoom;
        this.viewportY = containerRect?.height / 2 - targetY * this.zoom;
    }
}