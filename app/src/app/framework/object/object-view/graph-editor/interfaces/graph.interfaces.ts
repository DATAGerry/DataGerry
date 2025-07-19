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
import { CINode } from 'src/app/framework/models/ci-explorer.model';

export interface GraphNode {
  /* persistent CI identity */
  id: number;
  label: string;
  type: string;
  level: number;

  /* visual-copy identity */
  uid: string;                     // unique per rendered instance

  /* layout */
  x: number;
  y: number;

  /* smooth-transition helpers  */
  targetX?: number;
  targetY?: number;

  /* runtime UI state */
  color: string;
  icon?: string;
  expanded?: boolean;
  isLoading?: boolean;
  isRoot?: boolean;
  hasChildren?: boolean;
  hasParents?: boolean;

  /* metadata */
  fields?: Array<{ name: string; value: string }>;
  ciNode?: CINode;
  connectionCount?: { parents: number; children: number };
  status?: 'active' | 'inactive';
  metadata?: any;
}

export interface Connection {
  from: number;
  to: number;

  fromLevel: number;
  toLevel: number;

  fromUid?: string;
  toUid?: string;

  relationLabel?: string;
  relationColor?: string;
  relationIcon?: string;
  isValid?: boolean;
  strength?: number;
  dataFlow?: boolean;
  metadata?: any;
}

export interface NodeGroup {
  level: number;
  nodes: GraphNode[];
  x: number;
  y: number;
  collapsed?: boolean;
}

export interface BreadcrumbItem {
  id: number;
  label: string;
  icon: string;
  level: number;
}

export interface PerformanceMetrics {
  nodeCount: number;
  connectionCount: number;
  renderTime: number;
  fps: number;
}