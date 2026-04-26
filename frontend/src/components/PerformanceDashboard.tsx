import React, { useEffect, useState } from 'react';
import { TrendingUp, Target, BarChart3, PieChart, Activity, BrainCircuit, ShieldCheck, ShieldAlert, Scale, Database, Server } from 'lucide-react';
import { outcomeApi, analyticsApi, systemApi } from '../services/api';
import { PerformanceSummary, DimensionBreakdown, LLMImpactAnalysis, SystemStatus } from '../types/signal';

interface PerformanceDashboardProps {
  activeDomain?: string;
}

const PerformanceDashboard: React.FC<PerformanceDashboardProps> = ({ activeDomain }) => {
  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const [breakdown, setBreakdown] = useState<DimensionBreakdown[]>([]);
  const [llmImpact, setLlmImpact] = useState<LLMImpactAnalysis[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [dimension, setDimension] = useState('confidence_level');
  const [qualityFilter, setQualityFilter] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [s, b, i, status] = await Promise.all([
          outcomeApi.getSummary(qualityFilter || undefined, activeDomain),
          outcomeApi.getBreakdown(dimension, qualityFilter || undefined, activeDomain),
          analyticsApi.getLLMImpact(activeDomain),
          systemApi.getStatus()
        ]);
        setSummary(s);
        setBreakdown(b);
        setLlmImpact(i);
        setSystemStatus(status);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [dimension, qualityFilter, activeDomain]);

  if (loading || !summary) {
    return <div className="animate-pulse bg-slate-900 h-64 rounded-xl border border-slate-800 flex items-center justify-center text-slate-500 font-bold uppercase tracking-widest text-[10px]">Carregando Dashboard Consolidado...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Bloco de Saúde e Governança */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${systemStatus?.database_ok ? 'bg-emerald-500/10' : 'bg-rose-500/10'}`}>
              <Database className={`w-4 h-4 ${systemStatus?.database_ok ? 'text-emerald-500' : 'text-rose-500'}`} />
            </div>
            <div>
              <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Database Status</p>
              <p className="text-[10px] font-bold text-slate-300">{systemStatus?.database_ok ? 'CONECTADO' : 'ERRO'}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Sinais</p>
            <p className="text-[10px] font-black text-white">{systemStatus?.counts.signals}</p>
          </div>
        </div>

        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-sky-500/10 rounded-lg">
              <Server className="w-4 h-4 text-sky-500" />
            </div>
            <div>
              <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Environment Mode</p>
              <p className="text-[10px] font-bold text-sky-400">{systemStatus?.environment_mode || 'UNKNOWN'}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Domínio Ativo</p>
            <p className="text-[10px] font-black text-white">{activeDomain?.replace('_', ' ')}</p>
          </div>
        </div>

        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${systemStatus?.indicators.real_captured_present ? 'bg-emerald-500/10' : 'bg-amber-500/10'}`}>
              <ShieldCheck className={`w-4 h-4 ${systemStatus?.indicators.real_captured_present ? 'text-emerald-500' : 'text-amber-500'}`} />
            </div>
            <div>
              <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Data Presence</p>
              <p className="text-[10px] font-bold text-slate-300">
                {systemStatus?.indicators.real_captured_present ? 'REAL DATA ACTIVE' : 'DEMO ONLY'}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Outcomes</p>
            <p className="text-[10px] font-black text-white">{systemStatus?.counts.outcomes}</p>
          </div>
        </div>
      </div>

      {/* Header com Filtros de Base */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
        <div className="flex items-center gap-3">
          <Activity className="w-5 h-5 text-slate-500" />
          <div>
            <h2 className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400">BSI Performance Analytics</h2>
            <p className="text-[9px] text-slate-600 font-bold uppercase mt-0.5">Domínio: {activeDomain === 'CRYPTO_SPOT' ? 'Crypto Spot' : 'B3 Equities'}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="flex flex-col gap-1">
            <span className="text-[8px] font-black text-slate-500 uppercase tracking-widest text-right">Filtro de Qualidade</span>
            <select 
              value={qualityFilter}
              onChange={(e) => setQualityFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-[10px] text-white rounded-lg px-3 py-1.5 outline-none font-bold min-w-[140px]"
            >
              <option value="">TODOS OS DADOS</option>
              <option value="REAL_CAPTURED">REAL CAPTURED</option>
              <option value="SEEDED_DEMO">SEEDED DEMO</option>
              <option value="PARTIAL">PARTIAL</option>
              <option value="MANUAL_OVERRIDE">MANUAL OVERRIDE</option>
            </select>
          </div>
          
          <div className={`flex items-center gap-2 px-3 py-2.5 rounded-lg border text-[9px] font-black uppercase tracking-widest h-fit mt-auto ${
            summary.data_quality_label === 'SEEDED_DEMO' 
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-500' 
              : summary.data_quality_label === 'ALL'
              ? 'bg-slate-800 border-slate-700 text-slate-400'
              : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'
          }`}>
            {summary.data_quality_label === 'SEEDED_DEMO' && <div className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></div>}
            {summary.data_quality_label.replace('_', ' ')}
          </div>
        </div>
      </div>

      {/* Grid de Métricas de Taxa */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 shadow-xl">
          <div className="flex items-center gap-2 mb-4">
            <BrainCircuit className="w-4 h-4 text-sky-400" />
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Interpretação IA</span>
          </div>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-[10px] font-bold mb-1">
                <span className="text-slate-400">Sucesso</span>
                <span className="text-white">{summary.interpreted_success_rate.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                <div className="bg-sky-500 h-full" style={{ width: `${summary.interpreted_success_rate}%` }}></div>
              </div>
            </div>
            <div className="flex justify-between text-[9px] font-bold text-slate-600">
              <span>Falhas/NA</span>
              <span>{(summary.interpreted_failed_rate + summary.no_interpretation_rate).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 shadow-xl">
          <div className="flex items-center gap-2 mb-4">
            <Scale className="w-4 h-4 text-emerald-400" />
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Eficácia Global</span>
          </div>
          <div className="text-2xl font-black text-white">{summary.win_rate_global.toFixed(1)}%</div>
          <div className="text-[8px] text-slate-500 font-black uppercase mt-1">Win Rate Auditoria (n={summary.n_resolved})</div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 shadow-xl">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4 text-indigo-400" />
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Retorno Médio</span>
          </div>
          <div className={`text-2xl font-black ${summary.avg_return_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {summary.avg_return_pct >= 0 ? '+' : ''}{summary.avg_return_pct.toFixed(2)}%
          </div>
          <div className="text-[8px] text-slate-500 font-black uppercase mt-1">Mediana: {summary.median_return_pct.toFixed(2)}%</div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 shadow-xl">
          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-4 h-4 text-slate-500" />
            <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Maturação</span>
          </div>
          <div className="text-2xl font-black text-white">{summary.resolved_rate.toFixed(1)}%</div>
          <div className="text-[8px] text-slate-500 font-black uppercase mt-1">Sinais Resolvidos / Total</div>
        </div>
      </div>

      {/* LLM Impact Analytics */}
      <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex items-center gap-3">
          <BrainCircuit className="w-4 h-4 text-sky-400" />
          <h3 className="text-[11px] font-black uppercase tracking-widest text-slate-300">Impacto do LLM por Domínio</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[10px]">
            <thead>
              <tr className="bg-slate-950/50 border-b border-slate-800">
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest">Grupo Comparado</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-center">n</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest">Win Rate</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-right">Retorno Médio</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-right">Mediana</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {llmImpact.map((item, idx) => (
                <tr key={idx} className={item.group.includes("Success") ? "bg-sky-500/5" : ""}>
                  <td className="px-6 py-4 font-black text-slate-300">{item.group}</td>
                  <td className="px-6 py-4 text-center font-bold text-slate-500">{item.n}</td>
                  <td className="px-6 py-4">
                    <span className={`font-black ${item.win_rate > summary.win_rate_global ? 'text-emerald-400' : 'text-white'}`}>
                      {item.win_rate.toFixed(1)}%
                    </span>
                  </td>
                  <td className={`px-6 py-4 text-right font-bold ${item.avg_return_pct >= 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
                    {item.avg_return_pct >= 0 ? '+' : ''}{item.avg_return_pct.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right font-bold text-slate-500 italic">
                    {item.median_return_pct.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Breakdown por Dimensão */}
      <div className="bg-slate-900 rounded-xl border border-slate-800 shadow-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/50">
          <div className="flex items-center gap-3">
            <PieChart className="w-4 h-4 text-slate-500" />
            <h3 className="text-[11px] font-black uppercase tracking-widest text-slate-300">Detalhamento por Dimensão</h3>
          </div>
          <select 
            value={dimension}
            onChange={(e) => setDimension(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-[10px] text-white rounded px-2 py-1 outline-none font-bold"
          >
            <option value="confidence_level">Confiança</option>
            <option value="regime">Regime Market</option>
            <option value="context_alignment">Alinhamento Contexto</option>
            <option value="primary_thesis">Tese Principal (IA)</option>
            <option value="profile_fit">Aderência Perfil</option>
          </select>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[10px]">
            <thead>
              <tr className="bg-slate-950/50">
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest">Dimensão</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-center">n</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest">Win Rate</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-right">Média</th>
                <th className="px-6 py-3 uppercase font-black text-slate-500 tracking-widest text-right">Mediana</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {breakdown.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-slate-800 rounded text-[9px] font-bold text-slate-300 border border-slate-700 uppercase">
                      {row.label}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-center gap-2 font-bold text-slate-400">
                      {row.n}
                      {row.sample_too_small && (
                        <span title="Amostra insuficiente">
                          <ShieldAlert className="w-3 h-3 text-amber-500" />
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 bg-slate-800 h-1 rounded-full overflow-hidden w-16">
                        <div 
                          className={`h-full ${row.win_rate > summary.win_rate_global ? 'bg-emerald-500' : 'bg-sky-500'}`} 
                          style={{ width: `${row.win_rate}%` }}
                        ></div>
                      </div>
                      <span className="font-black text-white">{row.win_rate.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td className={`px-6 py-4 text-right font-black ${row.avg_return_pct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {row.avg_return_pct >= 0 ? '+' : ''}{row.avg_return_pct.toFixed(2)}%
                  </td>
                  <td className="px-6 py-4 text-right font-bold text-slate-500 italic">
                    {row.median_return_pct.toFixed(2)}%
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

export default PerformanceDashboard;
