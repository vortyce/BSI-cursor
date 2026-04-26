import React from 'react';
import { AllocationRecommendation, AllocationItem } from '../types/portfolio';
import { 
  BarChart3, PieChart, Info, CheckCircle2, XCircle, 
  AlertTriangle, Clock, ArrowRight, Zap, Target
} from 'lucide-react';

interface AllocationSummaryProps {
  recommendation: AllocationRecommendation;
  onRunAllocation: () => void;
  loading: boolean;
}

const AllocationSummary: React.FC<AllocationSummaryProps> = ({ recommendation, onRunAllocation, loading }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RECOMMENDED': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      case 'SECONDARY': return 'text-sky-400 bg-sky-400/10 border-sky-400/20';
      case 'REJECTED': return 'text-rose-400 bg-rose-400/10 border-rose-400/20';
      case 'OUT_OF_PROFILE': return 'text-amber-400 bg-amber-400/10 border-amber-400/20';
      case 'CAPITAL_CONSTRAINED': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'LOW_PRIORITY': return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'RECOMMENDED': return <CheckCircle2 className="w-4 h-4" />;
      case 'SECONDARY': return <Zap className="w-4 h-4" />;
      case 'REJECTED': return <XCircle className="w-4 h-4" />;
      case 'OUT_OF_PROFILE': return <ShieldAlert className="w-4 h-4" />;
      case 'CAPITAL_CONSTRAINED': return <AlertTriangle className="w-4 h-4" />;
      case 'LOW_PRIORITY': return <Clock className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header com Capital Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Capital Total', value: recommendation.total_capital, icon: Target, color: 'text-white' },
          { label: 'Reserva de Caixa', value: recommendation.cash_reserve, icon: Clock, color: 'text-amber-400' },
          { label: 'Alocado', value: recommendation.allocated_capital, icon: CheckCircle2, color: 'text-emerald-400' },
          { label: 'Disponível / Sobra', value: recommendation.unallocated_capital, icon: ArrowRight, color: 'text-sky-400' },
        ].map((item, idx) => (
          <div key={idx} className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-2xl p-5 shadow-lg">
            <div className="flex items-center gap-2 mb-2">
              <item.icon className={`w-3.5 h-3.5 ${item.color.split(' ')[0]}`} />
              <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">{item.label}</span>
            </div>
            <div className={`text-xl font-black ${item.color}`}>
              ${item.value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
          </div>
        ))}
      </div>

      {/* Tabela de Oportunidades Ranqueadas */}
      <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="p-6 border-b border-slate-800/50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-sky-500/20 p-2 rounded-lg">
              <BarChart3 className="w-5 h-5 text-sky-400" />
            </div>
            <div>
              <h2 className="text-lg font-black text-white uppercase tracking-wider">Ranking de Oportunidades</h2>
              <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Heurística de alocação por prioridade</p>
            </div>
          </div>
          <button 
            onClick={onRunAllocation}
            disabled={loading}
            className="px-6 py-2.5 bg-sky-500 hover:bg-sky-400 disabled:opacity-50 text-white text-[10px] font-black uppercase tracking-widest rounded-lg transition-all"
          >
            {loading ? 'Processando...' : 'Recalcular Alocação'}
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-800/50 bg-slate-950/30">
                <th className="px-6 py-4 text-[10px] font-black uppercase text-slate-500 tracking-widest">Ativo / Domínio</th>
                <th className="px-6 py-4 text-[10px] font-black uppercase text-slate-500 tracking-widest text-center">Score Heurístico</th>
                <th className="px-6 py-4 text-[10px] font-black uppercase text-slate-500 tracking-widest">Status</th>
                <th className="px-6 py-4 text-[10px] font-black uppercase text-slate-500 tracking-widest text-right">Alocação Sugerida</th>
                <th className="px-6 py-4 text-[10px] font-black uppercase text-slate-500 tracking-widest">Racional</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/30">
              {recommendation.items.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/20 transition-colors group">
                  <td className="px-6 py-5">
                    <div className="flex flex-col">
                      <span className="text-sm font-bold text-white group-hover:text-sky-400 transition-colors">
                        {item.asset} <span className="text-[10px] font-normal text-slate-500">({item.direction})</span>
                      </span>
                      <span className="text-[9px] uppercase font-black text-slate-600 tracking-tighter">{item.domain}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex flex-col items-center">
                      <div className="w-full max-w-[100px] h-1.5 bg-slate-800 rounded-full overflow-hidden mb-1.5">
                        <div 
                          className="h-full bg-sky-500 shadow-[0_0_8px_rgba(14,165,233,0.5)]" 
                          style={{ width: `${item.priority_score}%` }}
                        />
                      </div>
                      <span className="text-[10px] font-black text-white">{item.priority_score.toFixed(1)} pts</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border text-[9px] font-black uppercase tracking-widest ${getStatusColor(item.status)}`}>
                      {getStatusIcon(item.status)}
                      {item.status.replace('_', ' ')}
                    </div>
                  </td>
                  <td className="px-6 py-5 text-right">
                    <div className="flex flex-col items-end">
                      <span className="text-sm font-black text-white">${item.suggested_allocation_amount.toLocaleString()}</span>
                      <span className="text-[10px] font-bold text-slate-500">{item.suggested_allocation_pct.toFixed(2)}% do Capital</span>
                    </div>
                  </td>
                  <td className="px-6 py-5 max-w-xs">
                    <p className="text-[11px] text-slate-400 italic line-clamp-2 leading-relaxed">
                      "{item.rationale}"
                    </p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const ShieldAlert = (props: any) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>
);

export default AllocationSummary;
