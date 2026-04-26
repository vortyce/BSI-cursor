import React from 'react';
import { PortfolioReview, ConcentrationStatus } from '../types/portfolio';
import { Activity, AlertTriangle, CheckCircle, PieChart } from 'lucide-react';

interface Props {
  review: PortfolioReview;
}

const PortfolioDiagnostics: React.FC<Props> = ({ review }) => {
  const getStatusColor = (status: ConcentrationStatus) => {
    switch (status) {
      case 'HEALTHY': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'WARNING': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'CRITICAL': return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  const getStatusIcon = (status: ConcentrationStatus) => {
    switch (status) {
      case 'HEALTHY': return <CheckCircle className="w-5 h-5" />;
      case 'WARNING': return <AlertTriangle className="w-5 h-5" />;
      case 'CRITICAL': return <Activity className="w-5 h-5" />;
      default: return null;
    }
  };

  return (
    <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2">
          <PieChart className="w-4 h-4 text-sky-400" />
          Diagnóstico de Saúde
        </h3>
        <div className={`px-4 py-1.5 rounded-full border flex items-center gap-2 text-[10px] font-black uppercase tracking-widest ${getStatusColor(review.concentration_status)}`}>
          {getStatusIcon(review.concentration_status)}
          {review.concentration_status}
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-2">
            <span>Exposição por Domínio</span>
            <span>Drift Máximo</span>
          </div>
          <div className="space-y-3">
            {Object.entries(review.drift_analysis_json.domains).map(([domain, data]) => (
              <div key={domain} className="space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-black text-slate-300">{domain}</span>
                  <span className={`text-[10px] font-bold ${data.drift > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {data.current_weight.toFixed(1)}% / {data.limit}%
                  </span>
                </div>
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div 
                    className={`h-full transition-all duration-1000 ${data.drift > 0 ? 'bg-rose-500' : 'bg-sky-500'}`}
                    style={{ width: `${Math.min(100, (data.current_weight / data.limit) * 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800/50">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800/30 p-3 rounded-xl border border-slate-800/50">
              <div className="text-[9px] font-black text-slate-500 uppercase tracking-tighter mb-1">Valor de Mercado</div>
              <div className="text-sm font-black text-white">
                ${review.total_market_value.toLocaleString(undefined, { minimumFractionDigits: 2 })}
              </div>
            </div>
            <div className="bg-slate-800/30 p-3 rounded-xl border border-slate-800/50">
              <div className="text-[9px] font-black text-slate-500 uppercase tracking-tighter mb-1">Caixa Disponível</div>
              <div className="text-sm font-black text-sky-400">
                ${review.cash_balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PortfolioDiagnostics;
