import React from 'react';
import { PortfolioActionItem, PortfolioActionType } from '../types/portfolio';
import { ArrowRightLeft, MinusCircle, PlusCircle, Power, Shield, Zap } from 'lucide-react';

interface Props {
  actions: PortfolioActionItem[];
  onAcknowledge: (positionId: number) => void;
}

const ActionList: React.FC<Props> = ({ actions, onAcknowledge }) => {
  const getActionConfig = (type: PortfolioActionType) => {
    switch (type) {
      case 'HOLD': return { color: 'text-emerald-400', icon: <Shield className="w-4 h-4" />, label: 'Manter' };
      case 'REDUCE': return { color: 'text-amber-400', icon: <MinusCircle className="w-4 h-4" />, label: 'Reduzir' };
      case 'EXIT': return { color: 'text-rose-400', icon: <Power className="w-4 h-4" />, label: 'Sair' };
      case 'REPLACE': return { color: 'text-sky-400', icon: <ArrowRightLeft className="w-4 h-4" />, label: 'Substituir' };
      case 'INCREASE': return { color: 'text-indigo-400', icon: <PlusCircle className="w-4 h-4" />, label: 'Aumentar' };
      case 'REBALANCE': return { color: 'text-violet-400', icon: <Zap className="w-4 h-4" />, label: 'Rebalancear' };
      default: return { color: 'text-slate-400', icon: null, label: type };
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-black text-white uppercase tracking-widest">Sugestões de Ação</h3>
        <span className="text-[10px] font-bold text-slate-500 uppercase">{actions.length} Recomendações</span>
      </div>

      {actions.map((action) => {
        const config = getActionConfig(action.action_type);
        return (
          <div key={action.id} className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all group">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-xl bg-slate-800/50 ${config.color}`}>
                  {config.icon}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-black text-white uppercase">{config.label}</span>
                    <span className="text-[10px] font-bold text-slate-500">|</span>
                    <span className="text-xs font-black text-sky-500">{action.asset}</span>
                  </div>
                  {action.priority_score_diff && (
                    <div className="text-[10px] font-bold text-emerald-400 uppercase mt-0.5">
                      Edge Superior: +{action.priority_score_diff.toFixed(0)} pontos
                    </div>
                  )}
                </div>
              </div>
              
              {action.position_id && (
                <button 
                  onClick={() => onAcknowledge(action.position_id!)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white text-[9px] font-black uppercase tracking-widest rounded-lg transition-all border border-slate-700/50"
                >
                  Ciente
                </button>
              )}
            </div>
            
            <p className="mt-4 text-xs leading-relaxed text-slate-400 italic">
              "{action.rationale}"
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default ActionList;
