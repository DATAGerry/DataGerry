export interface ControlMeasureAssignment {
    public_id?: number;
    control_measure_id: number;
    risk_assessment_id?: number;
    planned_implementation_date?: string | null;
    implementation_status: number; // CmdbExtendableOption → IMPLEMENTATION_STATE
    finished_implementation_date?: string | null;
    priority?: number; // 1‑Low,2‑Med,3‑High,4‑VeryHigh
    responsible_for_implementation_id_ref_type?: 'PERSON' | 'PERSON_GROUP';
    responsible_for_implementation_id?: number;

    naming?: {
      cma_summary?: string | null;
  };
  }

  export interface SelectOption<T = any> {
    id: number;
    label: string;
    data?: T;
  }
  
  // export interface ControlMeasureAssignment {
  //   public_id?: number;
  
  //   control_measure_id: number;                 // mandatory
  //   risk_assessment_id: number;                 // mandatory
  
  //   planned_implementation_date?:   string;     // ISO date yyyy‑MM‑dd
  //   implementation_status:          number;     // mandatory (ExtendableOption)
  //   finished_implementation_date?:  string;
  //   priority?:                      number;     // 1‑4
  
  //   responsible_for_implementation_id_ref_type?: 'PERSON' | 'PERSON_GROUP';
  //   responsible_for_implementation_id?:          number;
  // }
  