/* -------- basic primitives -------------------------------------------- */
export interface Field {
    name: string;
    value: string;
  }
  export interface TypeFieldDef {
    type: string;
    name: string;
    label: string;
  }
  
  /* -------- CMDB object (“linked_object”) ------------------------------- */
  export interface LinkedObject {
    public_id: number;
    type_id: number;
    version: string;
    creation_time: { $date: string };
    author_id: number;
    last_edit_time: { $date: string } | null;
    editor_id: number | null;
    active: boolean;
    fields: Field[];
    multi_data_sections: any[];
  }
  
  /* -------- CMDB type information (“type_info”) ------------------------- */
  export interface TypeInfo {
    type_id: number;
    label: string;
    icon: string; 
    fields: TypeFieldDef[];
  }
  
  /* -------- Hierarchy helpers --------------------------- */
  export type Direction = 'root' | 'parent' | 'child';
  
  /* -------- Node shape received from / sent to the UI ------------------- */
  export interface CINode {
    /* frontend helpers --------------------------------------------------- */
    level: number; //  0 = root, +1 = child, –1 = parent, …
    direction: Direction; //  "root" | "child" | "parent"
    color: string; 
    title: string; //  short label shown in the node
  
    /* domain data -------------------------------------------------------- */
    linked_object: LinkedObject;
    type_info: TypeInfo;
  }
  
  /* -------- Edge & relation metadata ----------------------------------- */
  export interface RelationMeta {
    relation_id: number;
    relationName: string;
    relationLabel: string; 
    relationIcon: string; 
    relationColor: string; 
  }
  
  export interface CIEdge {
    from: number;
    to: number;
    metadata: RelationMeta[]; // one edge, many relations
  }
  
  /* -------- Response shapes -------------------------------------------- */
  /* Stage-1 : with_root = true, target_type = BOTH */
  export interface GraphRespWithRoot {
    root_node: CINode;
    parent_nodes: CINode[];
    child_nodes: CINode[];
    parent_edges: CIEdge[];
    child_edges: CIEdge[];
  }
  
  /* Stage-2 : with_root = false, target_type = CHILD */
  export interface GraphRespChildren {
    child_nodes: CINode[];
    child_edges: CIEdge[];
  }
  
  /* Stage-3 : with_root = false, target_type = PARENT */
  export interface GraphRespParents {
    parent_nodes: CINode[];
    parent_edges: CIEdge[];
  }
  