import React from 'react';
import { SignalListItem, SignalStatus } from '../types/signal';

interface Props {
  signals: SignalListItem[];
  onSelectSignal: (id: number) => void;
}

const getStatusStyles = (status: SignalStatus) => {
  switch (status) {
    case 'INTERPRETED':
      return 'border-sky-500/30 bg-sky-500/10 text-sky-400';
    case 'INTERPRETATION_FAILED':
    case 'ERROR':
      return 'border-rose-500/30 bg-rose-500/10 text-rose-400';
    case 'CLOSED':
      return 'border-slate-500/30 bg-slate-800 text-slate-400';
    case 'REVIEWED':
      return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400';
    default:
      return 'border-slate-700 bg-slate-800 text-slate-400';
  }
};

const SignalsTable: React.FC<Props> = ({ signals, onSelectSignal }) => {
  return (
    <div className="overflow-x-auto bg-slate-900 rounded-lg border border-slate-800 shadow-xl">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-800 bg-slate-900/50">
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Timestamp</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Domínio</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Ativo</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Dir.</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Preço</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Status</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest text-center">Score (IA)</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">Outcome</th>
            <th className="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest text-right">Ações</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {signals.length === 0 ? (
            <tr>
              <td colSpan={9} className="p-8 text-center text-slate-500 italic text-sm">Nenhum sinal encontrado para este domínio.</td>
            </tr>
          ) : (
            signals.map((signal) => (
              <tr 
                key={signal.id} 
                onClick={() => onSelectSignal(signal.id)}
                className="hover:bg-slate-800/50 transition-colors cursor-pointer group"
              >
                <td className="p-4 text-xs text-slate-400">
                  {new Date(signal.created_at).toLocaleString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                </td>
                <td className="p-4">
                   <span className={`text-[8px] font-black px-1.5 py-0.5 rounded border ${
                     signal.domain === 'B3_EQUITIES' ? 'border-emerald-500/30 text-emerald-500 bg-emerald-500/5' : 'border-sky-500/30 text-sky-500 bg-sky-500/5'
                   }`}>
                     {signal.domain === 'B3_EQUITIES' ? 'B3' : 'CRYPTO'}
                   </span>
                </td>
                <td className="p-4 text-sm font-black text-white">
                  {signal.asset} <span className="text-slate-500 font-normal ml-1 text-[10px]">{signal.timeframe}m</span>
                </td>
                <td className="p-4">
                  <span className={`text-[9px] font-black px-2 py-0.5 rounded ${
                    signal.signal_direction === 'LONG' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                  }`}>
                    {signal.signal_direction === 'LONG' ? 'BUY' : 'SELL'}
                  </span>
                </td>
                <td className="p-4 text-xs font-mono text-slate-300">
                  {signal.domain === 'B3_EQUITIES' ? 'R$' : '$'}{signal.trigger_price.toLocaleString()}
                </td>
                <td className="p-4">
                  <span className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full border ${getStatusStyles(signal.status)}`}>
                    {signal.status.replace('_', ' ')}
                  </span>
                </td>
                <td className="p-4">
                  {signal.interpretation ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-10 h-1 bg-slate-800 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${signal.interpretation.confidence_score > 70 ? 'bg-emerald-500' : 'bg-sky-500'}`}
                          style={{ width: `${signal.interpretation.confidence_score}%` }}
                        ></div>
                      </div>
                      <span className="text-[10px] font-bold text-slate-300">{signal.interpretation.confidence_score}%</span>
                    </div>
                  ) : <div className="text-center text-slate-700 text-[10px]">N/A</div>}
                </td>
                <td className="p-4">
                  {signal.outcome && signal.outcome.status !== 'OPEN' ? (
                    <div className="flex items-center gap-2">
                      <span className={`text-[10px] font-black px-2 py-0.5 rounded ${
                        signal.outcome.status === 'WIN' ? 'bg-emerald-500 text-white' : 
                        signal.outcome.status === 'LOSS' ? 'bg-rose-500 text-white' : 'bg-slate-700 text-slate-300'
                      }`}>
                        {signal.outcome.status}
                      </span>
                      <span className={`text-[10px] font-black ${signal.outcome.return_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {signal.outcome.return_pct >= 0 ? '+' : ''}{signal.outcome.return_pct.toFixed(1)}%
                      </span>
                    </div>
                  ) : (
                    <span className="text-[10px] text-slate-600 font-bold uppercase tracking-widest italic">Aberto</span>
                  )}
                </td>
                <td className="p-4 text-right">
                  <button className="text-[10px] text-sky-500 group-hover:text-sky-400 font-black uppercase tracking-widest underline underline-offset-4">
                    Inspecionar
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default SignalsTable;
