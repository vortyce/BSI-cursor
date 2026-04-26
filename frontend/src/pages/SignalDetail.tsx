import React, { useEffect, useState } from 'react';
import { 
  X, Cpu, Zap, Activity, Info, 
  ChevronRight, ChevronDown, CheckCircle2, 
  AlertTriangle, History, Target, TrendingUp, TrendingDown, Clock, Globe, Bitcoin, Landmark
} from 'lucide-react';
import { signalApi } from '../services/api';
import { SignalDetail as SignalDetailType } from '../types/signal';

interface Props {
  signalId: number;
  onClose: () => void;
}

const SignalDetail: React.FC<Props> = ({ signalId, onClose }) => {
  const [signal, setSignal] = useState<SignalDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [showRaw, setShowRaw] = useState(false);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        setLoading(true);
        const data = await signalApi.getSignalDetail(signalId);
        setSignal(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [signalId]);

  if (loading) return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-5xl h-[600px] rounded-2xl animate-pulse"></div>
    </div>
  );

  if (!signal) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-5xl max-h-[90vh] overflow-hidden rounded-2xl shadow-2xl flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/50">
          <div className="flex items-center gap-4">
            <div className={`p-2 rounded-lg ${signal.signal_direction === 'LONG' ? 'bg-emerald-500/20 text-emerald-500' : 'bg-rose-500/20 text-rose-500'}`}>
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-black text-white">{signal.asset}</h2>
                <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest flex items-center gap-1.5 ${
                  signal.domain === 'B3_EQUITIES' ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30' : 'bg-sky-500/20 text-sky-500 border border-sky-500/30'
                }`}>
                  {signal.domain === 'B3_EQUITIES' ? <Landmark className="w-3 h-3" /> : <Bitcoin className="w-3 h-3" />}
                  {signal.domain === 'B3_EQUITIES' ? 'B3 Equities' : 'Crypto Spot'}
                </span>
                <span className="px-2 py-0.5 bg-slate-800 rounded text-[10px] font-bold text-slate-400 uppercase tracking-widest border border-slate-700">
                  {signal.timeframe}M
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest ${signal.signal_direction === 'LONG' ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white'}`}>
                  {signal.signal_direction}
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium mt-0.5">ID: {signal.external_signal_id}</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-8">
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Bloco A: Dados Técnicos Brutos */}
            <div className="lg:col-span-1 space-y-6">
              <section className="bg-slate-950/50 p-5 rounded-xl border border-slate-800/50">
                <div className="flex items-center gap-2 mb-4">
                  <Zap className="w-4 h-4 text-sky-500" />
                  <h3 className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400">Technical Snapshot</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Trigger Price</span>
                    <span className="text-sm font-mono text-white">${signal.trigger_price.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Market</span>
                    <span className="text-xs text-slate-300">{signal.market}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Domain</span>
                    <span className="text-xs font-black text-white">{signal.domain?.replace('_', ' ')}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Strategy</span>
                    <span className="text-xs text-slate-300">{signal.strategy_name} v{signal.strategy_version}</span>
                  </div>
                </div>
              </section>

              {/* Bloco C: Auditoria de Ciclo de Vida */}
              <section className="bg-slate-950/50 p-5 rounded-xl border border-slate-800/50">
                <div className="flex items-center gap-2 mb-4">
                  <History className="w-4 h-4 text-slate-500" />
                  <h3 className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400">Audit Trail</h3>
                </div>
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>
                      <div className="w-0.5 h-full bg-slate-800 my-1"></div>
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-white uppercase">Sinal Recebido</p>
                      <p className="text-[9px] text-slate-500">{new Date(signal.created_at).toLocaleString()}</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <div className={`w-2 h-2 rounded-full ${signal.interpretation_full ? 'bg-sky-500' : 'bg-slate-700'}`}></div>
                      <div className="w-0.5 h-full bg-slate-800 my-1"></div>
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-white uppercase">Interpretação IA</p>
                      <p className="text-[9px] text-slate-500">{signal.interpretation_full ? 'Concluída via GPT-4o' : 'Pendente/Indisponível'}</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <div className={`w-2 h-2 rounded-full ${signal.outcome_full && signal.outcome_full.status !== 'OPEN' ? 'bg-amber-500' : 'bg-slate-700'}`}></div>
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-white uppercase">Desfecho (Outcome)</p>
                      <p className="text-[9px] text-slate-500">
                        {signal.outcome_full && signal.outcome_full.status !== 'OPEN' 
                          ? `Resolvido como ${signal.outcome_full.status}` 
                          : 'Aguardando Janela de Resolução'}
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            {/* Bloco B: Interpretação LLM */}
            <div className="lg:col-span-2 space-y-6">
              {signal.interpretation_full ? (
                <div className="bg-slate-950/30 border border-sky-500/20 rounded-xl overflow-hidden shadow-lg">
                  <div className="p-4 bg-sky-500/10 border-b border-sky-500/20 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Cpu className="w-5 h-5 text-sky-400" />
                      <h3 className="text-xs font-black uppercase tracking-widest text-sky-400">LLM Interpretation Report</h3>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-sky-500/70 font-bold uppercase">Confidence Score:</span>
                      <span className="text-sm font-black text-white">{signal.interpretation_full.confidence_score}%</span>
                    </div>
                  </div>
                  
                  <div className="p-6 space-y-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-black block mb-1">Regime</span>
                        <span className="text-[11px] font-bold text-slate-200">{signal.interpretation_full.regime}</span>
                      </div>
                      <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-black block mb-1">Alignment</span>
                        <span className="text-[11px] font-bold text-slate-200">{signal.interpretation_full.context_alignment}</span>
                      </div>
                      <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-black block mb-1">Profile Fit</span>
                        <span className="text-[11px] font-bold text-slate-200">{signal.interpretation_full.profile_fit}</span>
                      </div>
                      <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                        <span className="text-[9px] text-slate-500 uppercase font-black block mb-1">Risk Level</span>
                        <span className="text-[11px] font-bold text-rose-400">{signal.interpretation_full.risk_flags.length > 0 ? 'High' : 'Low'}</span>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                        <Info className="w-3 h-3" />
                        Rationale
                      </h4>
                      <p className="text-sm text-slate-300 leading-relaxed italic border-l-2 border-sky-500/30 pl-4 py-1">
                        "{signal.interpretation_full.rationale_short}"
                      </p>
                    </div>

                    {/* Outcome Detail */}
                    {signal.outcome_full && signal.outcome_full.status !== 'OPEN' && (
                      <div className="bg-slate-900/80 border border-amber-500/20 rounded-xl overflow-hidden mt-4 animate-in zoom-in-95 duration-300">
                        <div className="p-3 bg-amber-500/10 flex items-center justify-between border-b border-amber-500/20">
                          <div className="flex items-center gap-2">
                            <Target className="w-4 h-4 text-amber-500" />
                            <span className="text-[10px] font-black uppercase text-amber-500 tracking-widest">Realization Data (Outcome)</span>
                          </div>
                          <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase ${
                            signal.outcome_full.status === 'WIN' ? 'bg-emerald-500 text-white' : 
                            signal.outcome_full.status === 'LOSS' ? 'bg-rose-500 text-white' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {signal.outcome_full.status}
                          </span>
                        </div>
                        <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                          <div className="flex flex-col">
                            <span className="text-[9px] text-slate-500 uppercase font-bold">Return</span>
                            <span className={`text-sm font-black ${signal.outcome_full.return_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                              {signal.outcome_full.return_pct >= 0 ? '+' : ''}{signal.outcome_full.return_pct.toFixed(2)}%
                            </span>
                          </div>
                          <div className="flex flex-col">
                            <span className="text-[9px] text-slate-500 uppercase font-bold">Max Favorable</span>
                            <span className="text-sm font-black text-sky-400">+{signal.outcome_full.mfe_pct?.toFixed(2)}%</span>
                          </div>
                          <div className="flex flex-col">
                            <span className="text-[9px] text-slate-500 uppercase font-bold">Max Adverse</span>
                            <span className="text-sm font-black text-rose-400">{signal.outcome_full.mae_pct?.toFixed(2)}%</span>
                          </div>
                          <div className="flex flex-col">
                            <span className="text-[9px] text-slate-500 uppercase font-bold">Duration</span>
                            <span className="text-sm font-black text-slate-300 flex items-center gap-1">
                              <Clock className="w-3 h-3" /> {signal.outcome_full.bars} bars
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    <div className="space-y-4">
                      <button 
                        onClick={() => setShowRaw(!showRaw)}
                        className="flex items-center gap-2 text-[9px] font-black text-slate-500 uppercase hover:text-slate-300 transition-colors"
                      >
                        {showRaw ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                        Raw AI Response Body
                      </button>
                      {showRaw && (
                        <pre className="bg-slate-900 p-4 rounded-lg text-[10px] font-mono text-sky-400 overflow-x-auto border border-slate-800">
                          {signal.interpretation_full.raw_response_body}
                        </pre>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-12 flex flex-col items-center text-center">
                  <Cpu className="w-12 h-12 text-slate-800 mb-4" />
                  <h3 className="text-slate-400 font-black uppercase tracking-widest">Interpretation Unavailable</h3>
                  <p className="text-xs text-slate-600 mt-2 max-w-xs">No analysis was recorded for this signal at the moment of ingestion.</p>
                </div>
              )}
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-800 bg-slate-900/50 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-[10px] text-slate-500 font-bold uppercase">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Domain: {signal.domain?.replace('_', ' ')} Verified
            </div>
          </div>
          <p className="text-[10px] text-slate-600 font-bold uppercase tracking-widest">BSI Terminal v8.0 - Multi-Market Mode</p>
        </div>
      </div>
    </div>
  );
};

export default SignalDetail;
