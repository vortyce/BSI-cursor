import React, { useState, useEffect } from 'react';
import { portfolioApi } from '../services/portfolioApi';
import { PortfolioProfile, AllocationRecommendation } from '../types/portfolio';
import ProfileForm from './ProfileForm';
import AllocationSummary from './AllocationSummary';
import PortfolioManagement from './PortfolioManagement';
import { Briefcase, AlertCircle, RefreshCw, Settings2, PieChart, Activity } from 'lucide-react';

const PortfolioTab: React.FC = () => {
  const [profile, setProfile] = useState<PortfolioProfile | null>(null);
  const [recommendation, setRecommendation] = useState<AllocationRecommendation | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeSubTab, setActiveSubTab] = useState<'allocation' | 'management'>('allocation');

  const fetchData = async () => {
    try {
      setLoading(true);
      const profileData = await portfolioApi.getProfile().catch(() => null);
      
      // Se não houver perfil, mantemos null para forçar configuração explícita
      setProfile(profileData);

      if (profileData) {
        const recData = await portfolioApi.getLatestRecommendation().catch(() => null);
        setRecommendation(recData);
      }
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Erro ao carregar dados do portfólio.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSaveProfile = async () => {
    if (!profile) return;
    try {
      setSaving(true);
      const savedProfile = await portfolioApi.updateProfile(profile);
      setProfile(savedProfile);
      const recommendationData = await portfolioApi.runRecommendation();
      setRecommendation(recommendationData);
      setError(null);
    } catch (err) {
      setError('Erro ao salvar perfil.');
    } finally {
      setSaving(false);
    }
  };

  const handleRunAllocation = async () => {
    try {
      setLoading(true);
      const data = await portfolioApi.runRecommendation();
      setRecommendation(data);
      setError(null);
    } catch (err) {
      setError('Erro ao processar alocação.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !profile) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <RefreshCw className="w-8 h-8 text-sky-500 animate-spin mb-4" />
        <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Sincronizando Camada de Alocação...</span>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {error && (
        <div className="bg-rose-500/10 border border-rose-500/20 p-4 rounded-xl flex items-center gap-3 text-rose-400">
          <AlertCircle className="w-5 h-5" />
          <span className="text-sm font-medium">{error}</span>
        </div>
      )}

      {/* Sub-Tabs Navigation */}
      <div className="flex gap-4 border-b border-slate-800 pb-px">
        <button 
          onClick={() => setActiveSubTab('allocation')}
          className={`flex items-center gap-2 px-6 py-4 text-[10px] font-black uppercase tracking-[0.2em] transition-all border-b-2 ${activeSubTab === 'allocation' ? 'text-sky-500 border-sky-500' : 'text-slate-500 border-transparent hover:text-slate-300'}`}
        >
          <PieChart className="w-3.5 h-3.5" />
          Alocação & Perfil
        </button>
        <button 
          onClick={() => setActiveSubTab('management')}
          className={`flex items-center gap-2 px-6 py-4 text-[10px] font-black uppercase tracking-[0.2em] transition-all border-b-2 ${activeSubTab === 'management' ? 'text-sky-500 border-sky-500' : 'text-slate-500 border-transparent hover:text-slate-300'}`}
        >
          <Activity className="w-3.5 h-3.5" />
          Gestão da Carteira
        </button>
      </div>

      {activeSubTab === 'allocation' ? (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start animate-in fade-in duration-500">
          {/* Lado Esquerdo: Configuração */}
          <div className="xl:col-span-5">
            <ProfileForm 
              profile={profile || {
                initial_capital: 10000,
                risk_profile: 'MODERATE',
                primary_goal: 'GROWTH',
                horizon: 'MEDIUM',
                allowed_domains: ['CRYPTO_SPOT'],
                max_single_position_pct: 10,
                max_domain_exposure_pct: 50,
                keep_cash_reserve_pct: 20,
                management_style: 'TACTICAL'
              }} 
              setProfile={(p) => setProfile(p)} 
              onSave={handleSaveProfile} 
              saving={saving} 
            />
          </div>

          {/* Lado Direito: Resultados */}
          <div className="xl:col-span-7">
            {!profile ? (
              <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 border-dashed rounded-2xl p-20 flex flex-col items-center justify-center text-center h-full">
                <div className="bg-sky-500/10 p-4 rounded-full mb-6">
                  <Settings2 className="w-10 h-10 text-sky-500" />
                </div>
                <h3 className="text-xl font-black text-white uppercase tracking-wider mb-2">Configuração Necessária</h3>
                <p className="text-sm text-slate-500 max-w-sm">Para gerar recomendações de alocação, você deve primeiro salvar seu perfil operacional e restrições de capital.</p>
              </div>
            ) : recommendation ? (
              <AllocationSummary 
                recommendation={recommendation} 
                onRunAllocation={handleRunAllocation} 
                loading={loading}
              />
            ) : (
              <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 border-dashed rounded-2xl p-20 flex flex-col items-center justify-center text-center">
                <div className="bg-slate-800 p-4 rounded-full mb-6">
                  <Briefcase className="w-10 h-10 text-slate-600" />
                </div>
                <h3 className="text-xl font-black text-white uppercase tracking-wider mb-2">Nenhuma Recomendação Ativa</h3>
                <p className="text-sm text-slate-500 max-w-sm mb-8">Clique em rodar para gerar a primeira camada de alocação baseada em seu perfil salvo.</p>
                <button 
                  onClick={handleRunAllocation}
                  className="px-8 py-3 bg-sky-500 hover:bg-sky-400 text-white text-xs font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-sky-500/20"
                >
                  Gerar Recomendação Inicial
                </button>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <PortfolioManagement />
        </div>
      )}
    </div>
  );
};

export default PortfolioTab;
