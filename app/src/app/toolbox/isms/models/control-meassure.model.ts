export interface ControlMeassure {
    public_id?: number;
    title: string;
    control_measure_type: 'CONTROL' | 'REQUIREMENT' | 'MEASURE';
    source: number;                // references an Extendable Option of type CONTROL_MEASURE
    implementation_state: number;  // references an Extendable Option of type IMPLEMENTATION_STATE
    identifier?: string;
    chapter?: string;
    description?: string;
    is_applicable?: boolean;
    reason?: string;
  }
  