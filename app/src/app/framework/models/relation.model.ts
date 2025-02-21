

export interface RelationSection {
    type: string;
    name: string;
    label: string; 
    fields: Array<any>; 
  }
  
  export interface RelationField {
    type: string;             // e.g. "text", "number", "textarea", etc.
    name: string;             // unique identifier
    label: string;
    required?: boolean;
    description?: string;
    regex?: string;
    placeholder?: string;
    value?: any;
    helperText?: string;
    options?: Array<{ name: string, label: string }>; // for radio/select
  }

  export interface CmdbRelationSection {
    type: string;
    name: string;
    label: string;
    fields?: Array<any>;
    bg_color?: string;
    reference?: {
        type_id: number;
        section_name: string;
        selected_fields?: Array<string>;
    };
}
  
  export class CmdbRelation {
    public_id: number; 
    relation_name: string;
    relation_name_parent: string;
    relation_icon_parent: string;
    relation_color_parent: string;
    relation_name_child: string;
    relation_icon_child: string;
    relation_color_child: string;

    parent_type_ids:  number[]; 
    child_type_ids: number[];     
    description?: string;
  
    sections: RelationSection[];
    fields: RelationField[];
  
    constructor() {
      this.relation_name = '';
      this.relation_name_parent = '';
      this.relation_icon_parent = '';  
      this.relation_color_parent = '#e9ecef';
      this.relation_name_child = '';
      this.relation_icon_child = '';
      this.relation_color_child = '#e9ecef';
      this.parent_type_ids = [];
      this.child_type_ids = [];
      this.description = '';
      this.sections = [];
      this.fields = [];
    }
  }  