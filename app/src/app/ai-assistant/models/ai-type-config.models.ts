export interface AiSectionSelection {
    name: string;               // section public_id
    selected: boolean;          // entire section toggle
    selectedFields: string[];   // field public_ids still checked
  }
  
  export interface AiTypeConfigPayload {
    typeId: number;
    sections: AiSectionSelection[];
  }
  