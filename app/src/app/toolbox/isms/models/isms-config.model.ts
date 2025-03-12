import { RiskClass } from './risk-class.model';
import { LikelihoodEntry } from './likelihood.model';
import { ImpactEntry } from './impact.model';
import { ImpactCategory } from './impact-category.model';
import { ProtectionGoal } from './protection-goal.model';

export interface IsmsConfig {
  riskClasses: RiskClass[];
  likelihoodEntries: LikelihoodEntry[];
  impactEntries: ImpactEntry[];
  impactCategories: ImpactCategory[];
  protectionGoals: ProtectionGoal[];
  riskMatrix: any;
}
