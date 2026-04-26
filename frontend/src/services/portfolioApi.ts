import { 
  PortfolioProfile, AllocationRecommendation, PortfolioPosition, PortfolioReview,
  PortfolioDecision, PortfolioActionItem, UserChoice
} from '../types/portfolio';

const API_BASE_URL = 'http://localhost:8000/api/v1/portfolio';

export const portfolioApi = {
  getProfile: async (): Promise<PortfolioProfile> => {
    const response = await fetch(`${API_BASE_URL}/profile`);
    if (!response.ok) throw new Error('Failed to fetch profile');
    return response.json();
  },

  updateProfile: async (profile: PortfolioProfile): Promise<PortfolioProfile> => {
    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile),
    });
    if (!response.ok) throw new Error('Failed to update profile');
    return response.json();
  },

  runRecommendation: async (): Promise<AllocationRecommendation> => {
    const response = await fetch(`${API_BASE_URL}/recommendation/run`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to run allocation engine');
    return response.json();
  },

  getLatestRecommendation: async (): Promise<AllocationRecommendation> => {
    const response = await fetch(`${API_BASE_URL}/recommendation/latest`);
    if (!response.ok) throw new Error('No recommendation found');
    return response.json();
  },

  getPositions: async (): Promise<PortfolioPosition[]> => {
    const response = await fetch(`${API_BASE_URL}/positions`);
    if (!response.ok) throw new Error('Failed to fetch positions');
    return response.json();
  },

  runReview: async (): Promise<PortfolioReview> => {
    const response = await fetch(`${API_BASE_URL}/review/run`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to run portfolio review');
    return response.json();
  },

  getLatestReview: async (): Promise<PortfolioReview> => {
    const response = await fetch(`${API_BASE_URL}/review/latest`);
    if (!response.ok) throw new Error('No review found');
    return response.json();
  },

  acknowledgeAction: async (positionId: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/positions/${positionId}/acknowledge`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to acknowledge action');
  },

  getPendingRecommendations: async (): Promise<PortfolioActionItem[]> => {
    const response = await fetch(`${API_BASE_URL}/recommendations/pending`);
    if (!response.ok) throw new Error('Failed to fetch pending recommendations');
    return response.json();
  },

  recordDecision: async (actionItemId: number, choice: UserChoice, notes?: string): Promise<PortfolioDecision> => {
    const response = await fetch(`${API_BASE_URL}/decisions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action_item_id: actionItemId, choice, notes }),
    });
    if (!response.ok) throw new Error('Failed to record decision');
    return response.json();
  },

  getDecisionHistory: async (): Promise<PortfolioDecision[]> => {
    const response = await fetch(`${API_BASE_URL}/decisions/history`);
    if (!response.ok) throw new Error('Failed to fetch decision history');
    return response.json();
  }
};
