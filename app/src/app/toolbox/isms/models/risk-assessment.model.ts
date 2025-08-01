/* risk-assessment.model.ts */

export interface RiskCalculationData {
    impacts: Array<{
      impact_category_id: number;
      impact_id?: number | null;
    }>;
    likelihood_id?: number | null;
    likelihood_value?: number;
    maximum_impact_id?:   number | null;
    maximum_impact_value?: number;
    risk_level_value?: number;
  }
  
  export interface RiskAssessment {
    public_id?: number;
  
    // Top references
    risk_id: number;  // required
    object_id_ref_type: 'OBJECT' | 'OBJECT_GROUP';
    object_id: number; // required
  
    // Before
    risk_calculation_before: RiskCalculationData;
    risk_assessor_id?: number;
    risk_owner_id_ref_type?: 'PERSON' | 'PERSON_GROUP';
    risk_owner_id?: number;
    interviewed_persons?: number[];
    risk_assessment_date: any;   // required
    additional_info?: string;
  
    // Treatment
    risk_treatment_option?: 'AVOID' | 'ACCEPT' | 'REDUCE' | 'TRANSFER_SHARE';
    responsible_persons_id_ref_type?: 'PERSON' | 'PERSON_GROUP';
    responsible_persons_id?: number;
    risk_treatment_description?: string;
    planned_implementation_date?: any;
    implementation_status: number;  // required
    finished_implementation_date?: any;
    required_resources?: string;
    costs_for_implementation?: number;
    costs_for_implementation_currency?: string;
    priority?: number; // 1=Low,2=Med,3=High,4=VeryHigh
    // control_measure_assignments?: any[];

    control_measure_assignments?:
    any[]                                     /* create-mode  */
  | {                                        /* edit-mode */
      created: any[];
      updated: any[];
      deleted: number[];
    };
    // After
    risk_calculation_after: RiskCalculationData;
  
    // Audit
    audit_done_date?: any;
    auditor_id_ref_type?: 'PERSON' | 'PERSON_GROUP';
    auditor_id?: number;
    audit_result?: string;


    naming?: {
      risk_id_name?: string;
      object_group_id_name?: string | null;
      object_id_name?: string | null;
      interviewed_persons_names?: string | null;
      responsible_persons_id_names?: string | null;
  };
  }
  