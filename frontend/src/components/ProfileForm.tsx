import React from 'react';
import { PortfolioProfile, RiskProfile, PrimaryGoal, TimeHorizon, ManagementStyle } from '../types/portfolio';
import { Shield, Target, Clock, Wallet, Settings2, CheckCircle2 } from 'lucide-react';

interface ProfileFormProps {
  profile: PortfolioProfile;
  setProfile: (profile: PortfolioProfile) => void;
  onSave: () => void;
  saving: boolean;
}

const ProfileForm: React.FC<ProfileFormProps> = ({ profile, setProfile, onSave, saving }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setProfile({
      ...profile,
      [name]: name.includes('pct') || name === 'initial_capital' ? parseFloat(value) : value
    });
  };

  const toggleDomain = (domain: string) => {
    const domains = profile.allowed_domains.includes(domain)
      ? profile.allowed_domains.filter(d => d !== domain)
      : [...profile.allowed_domains, domain];
    setProfile({ ...profile, allowed_domains: domains });
  };

  return (
    <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-2xl">
      <div className="flex items-center gap-3 mb-8 pb-4 border-b border-slate-800/50">
        <div className="bg-sky-500/20 p-2 rounded-lg">
          <Settings2 className="w-5 h-5 text-sky-400" />
        </div>
        <div>
          <h2 className="text-lg font-black text-white uppercase tracking-wider">Configuração do Perfil</h2>
          <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Defina suas restrições e objetivos operacionais</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Capital Inicial */}
        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <Wallet className="w-3 h-3" /> Capital Inicial (USD/BRL)
          </label>
          <input 
            type="number" 
            name="initial_capital"
            value={profile.initial_capital}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 focus:ring-1 focus:ring-sky-500/50 transition-all outline-none"
          />
        </div>

        {/* Perfil de Risco */}
        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <Shield className="w-3 h-3" /> Perfil de Risco
          </label>
          <select 
            name="risk_profile"
            value={profile.risk_profile}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 outline-none"
          >
            <option value="CONSERVATIVE">Conservador</option>
            <option value="MODERATE">Moderado</option>
            <option value="AGGRESSIVE">Agressivo</option>
          </select>
        </div>

        {/* Objetivo Primário */}
        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <Target className="w-3 h-3" /> Objetivo Primário
          </label>
          <select 
            name="primary_goal"
            value={profile.primary_goal}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 outline-none"
          >
            <option value="INCOME">Renda (Income)</option>
            <option value="GROWTH">Crescimento (Growth)</option>
            <option value="PROTECTION">Proteção</option>
            <option value="SPECULATION">Especulação</option>
            <option value="MIXED">Misto</option>
          </select>
        </div>

        {/* Horizonte */}
        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <Clock className="w-3 h-3" /> Horizonte de Tempo
          </label>
          <select 
            name="horizon"
            value={profile.horizon}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 outline-none"
          >
            <option value="SHORT">Curto Prazo</option>
            <option value="MEDIUM">Médio Prazo</option>
            <option value="LONG">Longo Prazo</option>
          </select>
        </div>

        {/* Domínios Permitidos */}
        <div className="md:col-span-2 space-y-3">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Domínios Permitidos</label>
          <div className="flex gap-3">
            {['CRYPTO_SPOT', 'B3_EQUITIES'].map(domain => (
              <button
                key={domain}
                onClick={() => toggleDomain(domain)}
                className={`flex-1 px-4 py-3 rounded-xl border transition-all flex items-center justify-center gap-2 text-xs font-bold uppercase tracking-wider ${
                  profile.allowed_domains.includes(domain)
                    ? 'bg-sky-500/10 border-sky-500/50 text-sky-400'
                    : 'bg-slate-950 border-slate-800 text-slate-500 hover:border-slate-700'
                }`}
              >
                {profile.allowed_domains.includes(domain) && <CheckCircle2 className="w-3 h-3" />}
                {domain.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        {/* Limites de Exposição */}
        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Reserva de Caixa (%)</label>
          <input 
            type="number" 
            name="keep_cash_reserve_pct"
            value={profile.keep_cash_reserve_pct}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 outline-none"
          />
        </div>

        <div className="space-y-2">
          <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Max por Posição (%)</label>
          <input 
            type="number" 
            name="max_single_position_pct"
            value={profile.max_single_position_pct}
            onChange={handleChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:border-sky-500/50 outline-none"
          />
        </div>
      </div>

      <button 
        onClick={onSave}
        disabled={saving}
        className="w-full mt-10 bg-sky-500 hover:bg-sky-400 disabled:opacity-50 text-white font-black uppercase tracking-[0.2em] py-4 rounded-xl shadow-lg shadow-sky-500/20 transition-all flex items-center justify-center gap-3"
      >
        {saving ? 'Salvando...' : 'Salvar Perfil Operacional'}
      </button>
    </div>
  );
};

export default ProfileForm;
