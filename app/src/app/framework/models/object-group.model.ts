export interface ObjectGroup {
    public_id?: number;
    name: string;
    group_type: ObjectGroupMode;
    categories: number[];   // array of ExtendableOption IDs
    assigned_ids: number[]; // object IDs if STATIC, type IDs if DYNAMIC
  }
  
  export interface ExtendableOption {
    public_id: number;
    value: string;
    option_type: string;
  }
  
  export interface GenericObject {
    public_id: number;
    name: string;
  }
  
  export interface GenericType {
    public_id: number;
    label: string;
  }
  
  /** The valid modes for ObjectGroup */
  export enum ObjectGroupMode {
    STATIC = 'STATIC',
    DYNAMIC = 'DYNAMIC'
  }
  