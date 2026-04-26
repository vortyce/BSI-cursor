import React, { useMemo } from 'react';
import { SignalStatus, InterpretationStatus, SignalListItem } from '../types/signal';

interface Props {
  signals: SignalListItem[];
  filters: {
    search: string;
    asset: string;
    status: string;
    interpStatus: string;
    direction: string;
    regime: string;
    alignment: string;
    confidence: string;
  };
  setFilters: (filters: any) => void;
  sortBy: string;
  setSortBy: (sort: string) => void;
}

const SignalFilters: React.FC<Props> = ({ signals, filters, setFilters, sortBy, setSortBy }) => {
  // Gera lista única de assets a partir dos sinais reais
  const availableAssets = useMemo(() => {
    const assets = new Set(signals.map(s => s.asset));
    return Array.from(assets).sort();
  }, [signals]);

  return (
    <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-2xl space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-9 gap-4">
        
        {/* Busca */}
        <div className="flex flex-col gap-1 lg:col-span-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Busca (ID/Estratégia)</label>
          <input 
            type="text" 
            placeholder="Filtrar..." 
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 focus:ring-1 focus:ring-sky-500 outline-none w-full"
          />
        </div>

        {/* Ativo Dinâmico */}
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Ativo</label>
          <select 
            value={filters.asset}
            onChange={(e) => setFilters({...filters, asset: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            {availableAssets.map(asset => (
              <option key={asset} value={asset}>{asset}</option>
            ))}
          </select>
        </div>

        {/* Direção (NOVO) */}
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Direção</label>
          <select 
            value={filters.direction}
            onChange={(e) => setFilters({...filters, direction: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            <option value="LONG">LONG</option>
            <option value="SHORT">SHORT</option>
          </select>
        </div>

        {/* Signal Status Exaustivo */}
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Status Sinal</label>
          <select 
            value={filters.status}
            onChange={(e) => setFilters({...filters, status: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            <option value="RECEIVED">RECEIVED</option>
            <option value="STORED">STORED</option>
            <option value="INTERPRETED">INTERPRETED</option>
            <option value="CLOSED">CLOSED</option>
            <option value="ERROR">ERROR</option>
          </select>
        </div>

        {/* Interp Status Exaustivo */}
        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Status IA</label>
          <select 
            value={filters.interpStatus}
            onChange={(e) => setFilters({...filters, interpStatus: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            <option value="PENDING">PENDING</option>
            <option value="PROCESSING">PROCESSING</option>
            <option value="SUCCESS">SUCCESS</option>
            <option value="FAILED">FAILED</option>
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Regime</label>
          <select 
            value={filters.regime}
            onChange={(e) => setFilters({...filters, regime: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            <option value="BULLISH_TREND">BULLISH_TREND</option>
            <option value="BEARISH_TREND">BEARISH_TREND</option>
            <option value="RANGE">RANGE</option>
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-slate-500 font-black tracking-widest">Alinhamento</label>
          <select 
            value={filters.alignment}
            onChange={(e) => setFilters({...filters, alignment: e.target.value})}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded px-3 py-2 outline-none"
          >
            <option value="Todos">Todos</option>
            <option value="ALIGNED">ALIGNED</option>
            <option value="MIXED">MIXED</option>
            <option value="CONFLICTING">CONFLICTING</option>
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] uppercase text-sky-500 font-black tracking-widest">Ordenação</label>
          <select 
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-slate-800 border border-sky-500/30 text-xs text-sky-400 font-bold rounded px-3 py-2 outline-none"
          >
            <option value="recent">Mais Recentes</option>
            <option value="score_desc">Confiança (Maior)</option>
            <option value="score_asc">Confiança (Menor)</option>
          </select>
        </div>

      </div>
      
      <div className="flex justify-end">
        <button 
          onClick={() => setFilters({search: '', asset: 'Todos', status: 'Todos', interpStatus: 'Todos', direction: 'Todos', regime: 'Todos', alignment: 'Todos', confidence: 'Todos'})}
          className="text-[9px] uppercase font-black text-slate-500 hover:text-slate-300 tracking-[0.2em] transition-colors"
        >
          Resetar Filtros
        </button>
      </div>
    </div>
  );
};

export default SignalFilters;
