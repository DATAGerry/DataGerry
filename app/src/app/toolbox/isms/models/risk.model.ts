export interface Risk {
    public_id?: number;
    name: string;
    risk_type: string;
    identifier?: string;
    threats?: number[]; 
    vulnerabilities?: number[]; 
    protection_goals?: number[];
    description?: string;
    consequences?: string;
    category_id?: string;
  }  