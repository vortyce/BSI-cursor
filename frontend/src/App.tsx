import React, { useState, useEffect, useMemo } from 'react';
import { 
  LayoutDashboard, Terminal as TerminalIcon, 
  AlertCircle, RefreshCw, Database, BarChart3, List, Bitcoin, Landmark, Briefcase
} from 'lucide-react';
import { SignalListItem } from './types/signal';
import { signalApi } from './services/api';
import SignalsTable from './components/SignalsTable';
import SignalFilters from './components/SignalFilters';
import SignalDetail from './pages/SignalDetail';
import PerformanceDashboard from './components/PerformanceDashboard';
import PortfolioTab from './components/PortfolioTab';

function App() {
  const [activeTab, setActiveTab] = useState<'signals' | 'performance' | 'portfolio'>('signals');
  const [activeDomain, setActiveDomain] = useState<string>('CRYPTO_SPOT');
  const [signals, setSignals] = useState<SignalListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSignalId, setSelectedSignalId] = useState<number | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  
  // Filtros
  const [filters, setFilters] = useState({
    search: '',
    asset: 'Todos',
    status: 'Todos',
    interpStatus: 'Todos',
    direction: 'Todos',
    regime: 'Todos',
    alignment: 'Todos',
    confidence: 'Todos'
  });

  const [sortBy, setSortBy] = useState('recent');

  const fetchSignals = async () => {
    try {
      setLoading(true);
      const data = await signalApi.getSignals(activeDomain);
      setSignals(data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      setError('Erro ao conectar com o terminal operacional.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSignals();
    const interval = setInterval(fetchSignals, 15000);
    return () => clearInterval(interval);
  }, [activeDomain]);

  const processedSignals = useMemo(() => {
    return signals
      .filter(s => {
        const matchesSearch = s.external_signal_id.toLowerCase().includes(filters.search.toLowerCase()) || 
                             s.strategy_name.toLowerCase().includes(filters.search.toLowerCase());
        const matchesAsset = filters.asset === 'Todos' || s.asset === filters.asset;
        const matchesStatus = filters.status === 'Todos' || s.status === filters.status;
        const matchesInterp = filters.interpStatus === 'Todos' || s.interpretation?.status === filters.interpStatus;
        const matchesDirection = filters.direction === 'Todos' || s.signal_direction === filters.direction;
        const matchesRegime = filters.regime === 'Todos' || s.interpretation?.regime === filters.regime;
        const matchesAlignment = filters.alignment === 'Todos' || s.interpretation?.context_alignment === filters.alignment;
        
        return matchesSearch && matchesAsset && matchesStatus && matchesInterp && matchesDirection && matchesRegime && matchesAlignment;
      })
      .sort((a, b) => {
        if (sortBy === 'recent') return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        if (sortBy === 'score_desc') return (b.interpretation?.confidence_score || 0) - (a.interpretation?.confidence_score || 0);
        if (sortBy === 'score_asc') return (a.interpretation?.confidence_score || 0) - (b.interpretation?.confidence_score || 0);
        return 0;
      });
  }, [signals, filters, sortBy]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-sky-500/30">
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="bg-sky-500 p-1.5 rounded-lg">
                <TerminalIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-sm font-black uppercase tracking-[0.3em] text-white">BSI Terminal</h1>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Signal Intelligence & Audit</p>
              </div>
            </div>

            {/* Seletor de Domínio */}
            <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-lg border border-slate-700">
              <button 
                onClick={() => setActiveDomain('CRYPTO_SPOT')}
                className={`flex items-center gap-2 px-3 py-1 rounded-md text-[9px] font-black uppercase tracking-widest transition-all ${activeDomain === 'CRYPTO_SPOT' ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <Bitcoin className="w-3 h-3" />
                Crypto
              </button>
              <button 
                onClick={() => setActiveDomain('B3_EQUITIES')}
                className={`flex items-center gap-2 px-3 py-1 rounded-md text-[9px] font-black uppercase tracking-widest transition-all ${activeDomain === 'B3_EQUITIES' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <Landmark className="w-3 h-3" />
                B3 Equities
              </button>
            </div>

            {/* Navegação de Abas */}
            <nav className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
              <button 
                onClick={() => setActiveTab('signals')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'signals' ? 'bg-slate-700 text-white shadow-lg shadow-slate-500/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <List className="w-3 h-3" />
                Signals
              </button>
              <button 
                onClick={() => setActiveTab('performance')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'performance' ? 'bg-slate-700 text-white shadow-lg shadow-slate-500/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <BarChart3 className="w-3 h-3" />
                Performance
              </button>
              <button 
                onClick={() => setActiveTab('portfolio')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'portfolio' ? 'bg-slate-700 text-white shadow-lg shadow-slate-500/20' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <Briefcase className="w-3 h-3" />
                Portfolio
              </button>
            </nav>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 px-3 py-1 bg-amber-500/10 border border-amber-500/20 rounded-full">
              <Database className="w-3 h-3 text-amber-500" />
              <span className="text-[9px] font-black uppercase text-amber-500 tracking-widest">Modo Demo / {activeDomain}</span>
            </div>

            <div className="hidden md:flex flex-col items-end">
              <span className="text-[9px] uppercase font-black text-slate-500 tracking-widest">Status da Rede</span>
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-[10px] font-bold text-emerald-500 uppercase">Operacional</span>
              </div>
            </div>
            <button onClick={fetchSignals} className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-white">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-8 bg-rose-500/10 border border-rose-500/20 p-4 rounded-xl flex items-center gap-3 text-rose-400">
            <AlertCircle className="w-5 h-5" />
            <span className="text-sm font-medium">{error}</span>
          </div>
        )}

        {activeTab === 'signals' && (
          <div className="space-y-8 animate-in fade-in duration-500">
            <SignalFilters signals={signals} filters={filters} setFilters={setFilters} sortBy={sortBy} setSortBy={setSortBy} />

            <div className="space-y-4">
              <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-2">
                  <LayoutDashboard className="w-4 h-4 text-slate-500" />
                  <h2 className="text-xs font-black uppercase tracking-widest text-slate-400">Fluxo de Sinais: {activeDomain}</h2>
                </div>
                <div className="flex flex-col items-end gap-0.5">
                  <span className="text-[10px] font-bold text-slate-600 uppercase tracking-tighter">
                    Última atualização: {lastUpdate.toLocaleTimeString()}
                  </span>
                </div>
              </div>
              
              <SignalsTable signals={processedSignals} onSelectSignal={(id) => setSelectedSignalId(id)} />
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="animate-in fade-in duration-500">
            <PerformanceDashboard activeDomain={activeDomain} />
          </div>
        )}

        {activeTab === 'portfolio' && (
          <div className="animate-in slide-in-from-right-4 duration-500">
            <div className="mb-8">
              <h2 className="text-xl font-black text-white uppercase tracking-wider">Gestão de Alocação e Capital</h2>
              <p className="text-xs text-slate-500 uppercase font-bold tracking-widest mt-1">Primeira camada de decisão operacional baseada em perfil e prioridade</p>
            </div>
            <PortfolioTab />
          </div>
        )}
      </main>

      {selectedSignalId && <SignalDetail signalId={selectedSignalId} onClose={() => setSelectedSignalId(null)} />}
    </div>
  );
}

export default App;
