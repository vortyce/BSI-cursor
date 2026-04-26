import { SignalListItem, SignalDetail, PerformanceSummary, DimensionBreakdown, LLMImpactAnalysis, SystemStatus } from '../types/signal';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const signalApi = {
  async getSignals(domain?: string): Promise<SignalListItem[]> {
    const url = domain 
      ? `${API_BASE_URL}/webhooks/signals?domain=${domain}`
      : `${API_BASE_URL}/webhooks/signals`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Falha ao buscar sinais');
    return response.json();
  },

  async getSignalDetail(id: number): Promise<SignalDetail> {
    const response = await fetch(`${API_BASE_URL}/webhooks/signals/${id}/full`);
    if (!response.ok) throw new Error('Falha ao buscar detalhes do sinal');
    return response.json();
  }
};

export const outcomeApi = {
  async getSummary(quality?: string, domain?: string): Promise<PerformanceSummary> {
    const params = new URLSearchParams();
    if (quality) params.append('quality', quality);
    if (domain) params.append('domain', domain);
    
    const url = `${API_BASE_URL}/outcomes/summary?${params.toString()}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Falha ao buscar resumo de performance');
    return response.json();
  },

  async getBreakdown(dimension: string, quality?: string, domain?: string): Promise<DimensionBreakdown[]> {
    const params = new URLSearchParams();
    if (quality) params.append('quality', quality);
    if (domain) params.append('domain', domain);
    
    const url = `${API_BASE_URL}/outcomes/breakdown/${dimension}?${params.toString()}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Falha ao buscar breakdown por ${dimension}`);
    return response.json();
  }
};

export const analyticsApi = {
  async getLLMImpact(domain?: string): Promise<LLMImpactAnalysis[]> {
    const url = domain 
      ? `${API_BASE_URL}/analytics/llm-impact?domain=${domain}`
      : `${API_BASE_URL}/analytics/llm-impact`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Falha ao buscar impacto do LLM');
    return response.json();
  }
};

export const systemApi = {
  async getStatus(): Promise<SystemStatus> {
    const response = await fetch(`${API_BASE_URL}/system/status`);
    if (!response.ok) throw new Error('Falha ao buscar status do sistema');
    return response.json();
  }
};
