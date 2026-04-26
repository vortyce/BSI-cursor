export type RiskProfile = 'CONSERVATIVE' | 'MODERATE' | 'AGGRESSIVE';
export type PrimaryGoal = 'INCOME' | 'GROWTH' | 'PROTECTION' | 'SPECULATION' | 'MIXED';
export type TimeHorizon = 'SHORT' | 'MEDIUM' | 'LONG';
export type ManagementStyle = 'PASSIVE' | 'ACTIVE' | 'TACTICAL';
export type AllocationStatus = 'RECOMMENDED' | 'SECONDARY' | 'REJECTED' | 'OUT_OF_PROFILE' | 'CAPITAL_CONSTRAINED' | 'LOW_PRIORITY';
export type RecommendationStatus = 'SUCCESS' | 'NO_ACTION' | 'ERROR';

export interface PortfolioProfile {
  id?: number;
  initial_capital: number;
  risk_profile: RiskProfile;
  primary_goal: PrimaryGoal;
  horizon: TimeHorizon;
  allowed_domains: string[];
  max_single_position_pct: number;
  max_domain_exposure_pct: number;
  keep_cash_reserve_pct: number;
  management_style: ManagementStyle;
}

export interface AllocationItem {
  id: number;
  signal_id: number;
  asset: string;
  domain: string;
  direction: string;
  suggested_allocation_pct: number;
  suggested_allocation_amount: number;
  status: AllocationStatus;
  priority_score: number;
  priority_score_components: {
    confidence: number;
    alignment: number;
    thesis: number;
    data_quality: number;
  };
  rationale: string;
}

export interface AllocationRecommendation {
  id: number;
  total_capital: number;
  cash_reserve: number;
  available_capital: number;
  allocated_capital: number;
  unallocated_capital: number;
  macro_allocation_json: Record<string, number>;
  rationale_summary: string;
  status: RecommendationStatus;
  created_at: string;
  items: AllocationItem[];
}

export type PositionStatus = 'ACTIVE' | 'REDUCED' | 'CLOSED' | 'WATCHLIST';
export type PortfolioActionType = 'HOLD' | 'INCREASE' | 'REDUCE' | 'EXIT' | 'REPLACE' | 'REBALANCE' | 'NO_ACTION';
export type ConcentrationStatus = 'HEALTHY' | 'WARNING' | 'CRITICAL';

export interface PortfolioPosition {
  id: number;
  signal_id: number;
  asset: string;
  domain: string;
  entry_price: number;
  allocated_capital: number;
  status: PositionStatus;
  entry_rationale: string;
  acknowledged_at: string | null;
  created_at: string;
}

export interface PortfolioActionItem {
  id: number;
  action_type: PortfolioActionType;
  asset: string;
  priority_score_diff: number | null;
  rationale: string;
  position_id: number | null;
}

export interface PortfolioReview {
  id: number;
  total_market_value: number;
  cash_balance: number;
  drift_analysis_json: {
    domains: Record<string, { current_weight: number, limit: number, drift: number }>;
    positions: Record<string, { current_weight: number, limit: number, drift: number }>;
  };
  concentration_status: ConcentrationStatus;
  status: RecommendationStatus;
  summary: string;
  created_at: string;
  actions: PortfolioActionItem[];
}

export type UserChoice = 'ACCEPTED' | 'REJECTED' | 'DEFERRED' | 'EXPIRED';
export type SimulatedExecutionStatus = 'NONE' | 'PENDING' | 'APPLIED' | 'FAILED';

export interface PortfolioDecision {
  id: number;
  action_type: PortfolioActionType;
  asset: string;
  user_choice: UserChoice;
  decision_timestamp: string;
  simulated_execution_status: SimulatedExecutionStatus;
  impact: any;
  notes: string | null;
}
