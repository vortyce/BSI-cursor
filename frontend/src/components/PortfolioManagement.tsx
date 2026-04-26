import React, { useState, useEffect } from 'react';
import { portfolioApi } from '../services/portfolioApi';
import { PortfolioPosition, PortfolioReview } from '../types/portfolio';
import PortfolioDiagnostics from './PortfolioDiagnostics';
import ActionList from './ActionList';
import DecisionCenter from './DecisionCenter';
import AuditTrail from './AuditTrail';
import { RefreshCw, LayoutGrid, List, Activity, Briefcase, ShieldCheck, History } from 'lucide-react';

const PortfolioManagement: React.FC = () => {
  const [positions, setPositions] = useState<PortfolioPosition[]>([]);
  const [review, setReview] = useState<PortfolioReview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<'status' | 'governance'>('status');

  const fetchData = async () => {
    try {
      setLoading(true);
      const [posData, revData] = await Promise.all([
        portfolioApi.getPositions(),
        portfolioApi.getLatestReview().catch(() => null)
      ]);
      setPositions(posData);
      setReview(revData);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Erro ao carregar dados de gestão da carteira.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRunReview = async () => {
    try {
      setLoading(true);
      const newReview = await portfolioApi.runReview();
      setReview(newReview);
      setError(null);
    } catch (err) {
      setError('Erro ao processar análise da carteira.');
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (id: number) => {
    try {
      await portfolioApi.acknowledgeAction(id);
      await fetchData();
    } catch (err) {
      console.error('Failed to acknowledge', err);
    }
  };

  if (loading && !review) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <RefreshCw className="w-8 h-8 text-sky-500 animate-spin mb-4" />
        <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Sincronizando Gestão Viva...</span>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {/* Header Gestão */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-black text-white uppercase tracking-tighter flex items-center gap-3">
            <Activity className="w-8 h-8 text-sky-500" />
            Gestão da Carteira
          </h2>
          <p className="text-xs text-slate-500 mt-1 font-medium">Análise de drift, concentração e priorização contínua.</p>
        </div>
        <button 
          onClick={handleRunReview}
          disabled={loading}
          className="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-slate-700/50 flex items-center gap-2"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Rodar Análise de Saúde
        </button>
      </div>

      {/* Navigation - Status vs Governance */}
      <div className="flex gap-6 border-b border-slate-800 pb-px">
        <button 
          onClick={() => setActiveView('status')}
          className={`flex items-center gap-2 px-4 py-3 text-[9px] font-black uppercase tracking-widest transition-all border-b-2 ${activeView === 'status' ? 'text-sky-500 border-sky-500' : 'text-slate-500 border-transparent hover:text-slate-300'}`}
        >
          <LayoutGrid className="w-3.5 h-3.5" />
          Status da Carteira
        </button>
        <button 
          onClick={() => setActiveView('governance')}
          className={`flex items-center gap-2 px-4 py-3 text-[9px] font-black uppercase tracking-widest transition-all border-b-2 ${activeView === 'governance' ? 'text-sky-500 border-sky-500' : 'text-slate-500 border-transparent hover:text-slate-300'}`}
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          Central de Governança
        </button>
      </div>

      {activeView === 'status' ? (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 animate-in fade-in duration-500">
          {/* Lado Esquerdo: Diagnóstico e Sugestões */}
          <div className="xl:col-span-4 space-y-8">
            {review && <PortfolioDiagnostics review={review} />}
            {review && (
              <ActionList 
                actions={review.actions} 
                onAcknowledge={handleAcknowledge} 
              />
            )}
          </div>

          {/* Lado Direito: Posições Ativas */}
          <div className="xl:col-span-8">
            <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2">
                  <Briefcase className="w-4 h-4 text-sky-400" />
                  Posições Ativas
                </h3>
                <div className="flex gap-2">
                  <button className="p-1.5 bg-slate-800 rounded-lg text-sky-400"><LayoutGrid className="w-4 h-4" /></button>
                  <button className="p-1.5 bg-transparent rounded-lg text-slate-600"><List className="w-4 h-4" /></button>
                </div>
              </div>

              {positions.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {positions.map((pos) => (
                    <div key={pos.id} className="bg-slate-800/40 border border-slate-700/30 rounded-xl p-5 group hover:border-sky-500/30 transition-all">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <div className="text-lg font-black text-white tracking-tighter">{pos.asset}</div>
                          <div className="text-[10px] font-bold text-slate-500 uppercase">{pos.domain}</div>
                        </div>
                        <div className={`px-2 py-1 border rounded text-[9px] font-black uppercase ${pos.status === 'ACTIVE' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-amber-500/10 border-amber-500/20 text-amber-400'}`}>
                          {pos.status}
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <div className="text-[9px] font-black text-slate-500 uppercase">Capital Alocado</div>
                          <div className="text-sm font-black text-white">${pos.allocated_capital.toLocaleString()}</div>
                        </div>
                        <div>
                          <div className="text-[9px] font-black text-slate-500 uppercase">Preço de Entrada</div>
                          <div className="text-sm font-black text-white">${pos.entry_price.toLocaleString()}</div>
                        </div>
                      </div>

                      <div className="pt-3 border-t border-slate-700/50 flex justify-between items-center">
                        <span className="text-[9px] font-bold text-slate-500 uppercase">
                          Desde: {new Date(pos.created_at).toLocaleDateString()}
                        </span>
                        {pos.acknowledged_at && (
                          <span className="text-[8px] font-black text-sky-500 uppercase">Review OK</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-20 text-center">
                  <Briefcase className="w-12 h-12 text-slate-800 mx-auto mb-4" />
                  <p className="text-slate-500 text-sm font-medium">Nenhuma posição ativa no momento.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="xl:col-span-5">
            <DecisionCenter onDecisionMade={fetchData} />
          </div>
          <div className="xl:col-span-7">
            <AuditTrail />
          </div>
        </div>
      )}
    </div>
  );
};

export default PortfolioManagement;
