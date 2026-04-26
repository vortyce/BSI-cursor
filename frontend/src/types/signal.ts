export type SignalStatus = 
  | 'RECEIVED' | 'VALIDATED' | 'STORED' | 'PENDING_INTERPRETATION'
  | 'INTERPRETED' | 'INTERPRETATION_FAILED' | 'REVIEWED' | 'CLOSED' | 'ERROR';

export type InterpretationStatus = 'PENDING' | 'PROCESSING' | 'SUCCESS' | 'FAILED';
export type OutcomeStatus = 'WIN' | 'LOSS' | 'BREAKEVEN' | 'OPEN' | 'EXPIRED' | 'INCONCLUSIVE';

export interface PerformanceSummary {
  total_signals: number;
  n_resolved: number;
  resolved_rate: number;
  open_rate: number;
  interpreted_success_rate: number;
  interpreted_failed_rate: number;
  no_interpretation_rate: number;
  win_rate_global: number;
  win_rate_ia_success: number;
  n_ia_success: number;
  avg_return_pct: number;
  median_return_pct: number;
  data_quality_label: string;
  domain?: string;
}

export interface LLMImpactAnalysis {
  group: string;
  n: number;
  win_rate: number;
  avg_return_pct: number;
  median_return_pct: number;
  resolved_rate: number;
}

export interface DimensionBreakdown {
  label: string;
  n: number;
  win_rate: number;
  avg_return_pct: number;
  median_return_pct: number;
  sample_too_small: boolean;
}

export interface SignalListItem {
  id: number;
  domain?: string;
  external_signal_id: string;
  strategy_name: string;
  asset: string;
  timeframe: string;
  signal_direction: 'LONG' | 'SHORT';
  trigger_price: number;
  status: SignalStatus;
  created_at: string;
  interpretation?: {
    status: InterpretationStatus;
    regime: string;
    confidence_level: 'HIGH' | 'MEDIUM' | 'LOW';
    confidence_score: number;
    context_alignment: string;
  };
  outcome?: {
    status: OutcomeStatus;
    return_pct: number;
  };
}

export interface SignalDetail extends Omit<SignalListItem, 'interpretation' | 'outcome'> {
  market: string;
  signal_type: string;
  strategy_version: string;
  indicator_snapshot_json: any;
  candle_context_json: any;
  updated_at: string;
  interpretation_full?: any;
  outcome_full?: any;
}

export interface SystemStatus {
  app_name: string;
  environment_mode: string;
  database_ok: boolean;
  counts: {
    signals: number;
    interpretations: number;
    outcomes: number;
  };
  indicators: {
    seeded_data_present: boolean;
    real_captured_present: boolean;
  };
}
