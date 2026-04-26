import React, { useState, useEffect } from 'react';
import { portfolioApi } from '../services/portfolioApi';
import { PortfolioActionItem, UserChoice } from '../types/portfolio';
import { CheckCircle, XCircle, Clock, AlertCircle, MessageSquare } from 'lucide-react';

interface Props {
  onDecisionMade: () => void;
}

const DecisionCenter: React.FC<Props> = ({ onDecisionMade }) => {
  const [pending, setPending] = useState<PortfolioActionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [notes, setNotes] = useState<Record<number, string>>({});

  const fetchPending = async () => {
    try {
      setLoading(true);
      const data = await portfolioApi.getPendingRecommendations();
      setPending(data);
    } catch (err) {
      console.error('Failed to fetch pending', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPending();
  }, []);

  const handleDecision = async (id: number, choice: UserChoice) => {
    try {
      await portfolioApi.recordDecision(id, choice, notes[id]);
      await fetchPending();
      onDecisionMade();
    } catch (err) {
      console.error('Decision failed', err);
    }
  };

  if (loading && pending.length === 0) return null;
  if (pending.length === 0) return (
    <div className="bg-slate-900/40 border border-slate-800 border-dashed rounded-2xl p-10 text-center">
      <CheckCircle className="w-8 h-8 text-slate-700 mx-auto mb-3" />
      <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">Nenhuma decisão pendente</p>
    </div>
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-black text-white uppercase tracking-widest">Central de Decisões</h3>
        <div className="px-3 py-1 bg-sky-500/10 border border-sky-500/20 rounded-full text-[9px] font-black text-sky-400 uppercase">
          {pending.length} Pendentes
        </div>
      </div>

      {pending.map((item) => {
        const canMutatePortfolio = !['HOLD', 'NO_ACTION'].includes(item.action_type);

        return (
        <div key={item.id} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 hover:border-slate-700 transition-all">
          <div className="flex justify-between items-start mb-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-black text-sky-500 uppercase">{item.asset}</span>
                <span className="text-[10px] font-bold text-slate-600 tracking-tighter uppercase">{item.action_type}</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed italic">"{item.rationale}"</p>
            </div>
          </div>

          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <MessageSquare className="w-3 h-3 text-slate-500" />
              <span className="text-[9px] font-black text-slate-500 uppercase">Observações</span>
            </div>
            <textarea 
              value={notes[item.id] || ''}
              onChange={(e) => setNotes({...notes, [item.id]: e.target.value})}
              placeholder="Justificativa da decisão..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white placeholder:text-slate-700 focus:outline-none focus:border-sky-500/50 transition-all resize-none h-16"
            />
          </div>

          {canMutatePortfolio ? (
            <div className="grid grid-cols-3 gap-3">
              <button 
                onClick={() => handleDecision(item.id, 'ACCEPTED')}
                className="flex items-center justify-center gap-2 py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 rounded-xl text-[10px] font-black uppercase transition-all"
              >
                <CheckCircle className="w-3.5 h-3.5" /> Aceitar
              </button>
              <button 
                onClick={() => handleDecision(item.id, 'REJECTED')}
                className="flex items-center justify-center gap-2 py-2.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-xl text-[10px] font-black uppercase transition-all"
              >
                <XCircle className="w-3.5 h-3.5" /> Rejeitar
              </button>
              <button 
                onClick={() => handleDecision(item.id, 'DEFERRED')}
                className="flex items-center justify-center gap-2 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-400 border border-slate-700 rounded-xl text-[10px] font-black uppercase transition-all"
              >
                <Clock className="w-3.5 h-3.5" /> Adiar
              </button>
            </div>
          ) : (
            <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-3 text-[10px] font-bold uppercase tracking-widest text-slate-500">
              HOLD é diagnóstico de manutenção da posição e não dispara decisão operacional.
            </div>
          )}
          
          <div className="mt-4 flex items-center gap-2 text-[9px] text-slate-600 font-bold uppercase tracking-tighter">
            <AlertCircle className="w-3 h-3" />
            Decisões aceitas alteram a carteira simulada imediatamente.
          </div>
        </div>
        );
      })}
    </div>
  );
};

export default DecisionCenter;
