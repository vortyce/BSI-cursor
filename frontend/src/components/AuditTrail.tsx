import React, { useState, useEffect } from 'react';
import { portfolioApi } from '../services/portfolioApi';
import { PortfolioDecision } from '../types/portfolio';
import { History, Check, X, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';

const AuditTrail: React.FC = () => {
  const [history, setHistory] = useState<PortfolioDecision[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await portfolioApi.getDecisionHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to fetch history', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const getChoiceConfig = (choice: string) => {
    switch (choice) {
      case 'ACCEPTED': return { color: 'text-emerald-400', icon: <Check className="w-3 h-3" />, label: 'ACEITO' };
      case 'REJECTED': return { color: 'text-rose-400', icon: <X className="w-3 h-3" />, label: 'REJEITADO' };
      case 'DEFERRED': return { color: 'text-amber-400', icon: <Clock className="w-3 h-3" />, label: 'ADIADO' };
      case 'EXPIRED': return { color: 'text-slate-500', icon: <AlertTriangle className="w-3 h-3" />, label: 'EXPIRADO' };
      default: return { color: 'text-slate-400', icon: null, label: choice };
    }
  };

  return (
    <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2">
          <History className="w-4 h-4 text-sky-400" />
          Trilha Auditável de Decisões
        </h3>
        <span className="text-[10px] font-bold text-slate-500 uppercase">{history.length} Registros</span>
      </div>

      <div className="space-y-6">
        {history.length > 0 ? history.map((record) => {
          const config = getChoiceConfig(record.user_choice);
          return (
            <div key={record.id} className="relative pl-6 border-l border-slate-800">
              <div className="absolute -left-[6.5px] top-0 w-3 h-3 rounded-full bg-slate-900 border-2 border-slate-800" />
              
              <div className="flex flex-col gap-1 mb-2">
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded bg-slate-800 text-[9px] font-black flex items-center gap-1.5 ${config.color}`}>
                    {config.icon} {config.label}
                  </span>
                  <span className="text-[10px] font-black text-white uppercase">{record.asset}</span>
                  <span className="text-[9px] font-bold text-slate-600 uppercase">({record.action_type})</span>
                </div>
                <span className="text-[9px] font-bold text-slate-500">
                  {new Date(record.decision_timestamp).toLocaleString()}
                </span>
              </div>

              {record.notes && (
                <p className="text-[11px] text-slate-400 italic mb-2">"{record.notes}"</p>
              )}

              {record.simulated_execution_status === 'APPLIED' ? (
                <div className="mt-2 p-2 rounded-lg bg-emerald-500/5 border border-emerald-500/10 flex items-center gap-2">
                  <ShieldCheck className="w-3 h-3 text-emerald-400" />
                  <span className="text-[9px] font-black text-emerald-400 uppercase tracking-tighter">Impacto Aplicado na Carteira Simulada</span>
                </div>
              ) : (
                <div className="mt-2 p-2 rounded-lg bg-slate-800/30 border border-slate-800/50 flex items-center gap-2 opacity-60">
                  <Clock className="w-3 h-3 text-slate-500" />
                  <span className="text-[9px] font-black text-slate-500 uppercase tracking-tighter">Decisão Registrada - Sem Alteração na Carteira</span>
                </div>
              )}
            </div>
          );
        }) : (
          <div className="py-10 text-center">
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-600">Sem histórico disponível</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditTrail;
