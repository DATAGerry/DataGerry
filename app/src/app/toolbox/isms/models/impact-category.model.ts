export interface ImpactCategory {
    name: string;                      // Name of the impact category
    relevanceFactor: number;           // Value > 0 and <= 1 (default 1.0)
    impactLevelDescriptions: {         // A description for each ImpactEntry defined
      [impactEntryName: string]: string;
    };
  }
  