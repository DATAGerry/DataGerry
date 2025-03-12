export interface ImpactEntry {
    publicId?: number;     // Optional public ID if needed
    name: string;          // Name of the impact entry
    description: string;   // Detailed description
    calculationBasis: number; // Calculation basis (float)
    sort: number;          // Internal sort order
  }
  