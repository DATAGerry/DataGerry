export interface RiskMatrixCell {
    row: number;             // y-position of the cell (top row = 0)
    column: number;          // x-position of the cell (leftmost column = 0)
    risk_class_id: number;   // assigned Risk Class (0 = none)
    impact_id: number;       // chosen Impact
    impact_value: number;    // calculation_basis of that Impact
    likelihood_id: number;   // chosen Likelihood
    likelihood_value: number;// calculation_basis of that Likelihood
    calculated_value: number;// impact_value * likelihood_value
  }
  
  export interface IsmsRiskMatrix {
    public_id?: number;
    risk_matrix: RiskMatrixCell[];
    matrix_unit?: string;
  }
  