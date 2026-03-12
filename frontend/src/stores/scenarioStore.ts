// frontend/src/stores/scenarioStore.ts
import { create } from 'zustand';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export interface Scenario {
  id: string;
  name: string;
  description: string;
  premise: string;
  world_rules: Record<string, any>;
  survival_mechanics: Record<string, any>;
  possible_events: string[];
  ending_conditions: Record<string, any>;
  narrative_style: string;
  is_custom: boolean;
}

interface ScenarioStore {
  scenarios: Scenario[];
  currentScenario: Scenario | null;
  isLoading: boolean;
  error: string | null;

  fetchScenarios: () => Promise<void>;
  fetchScenario: (scenarioId: string) => Promise<void>;
  clearError: () => void;
}

export const useScenarioStore = create<ScenarioStore>((set, get) => ({
  scenarios: [],
  currentScenario: null,
  isLoading: false,
  error: null,

  fetchScenarios: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/scenarios/list`);
      set({ scenarios: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取场景列表失败', isLoading: false });
    }
  },

  fetchScenario: async (scenarioId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/scenarios/${scenarioId}`);
      set({ currentScenario: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取场景失败', isLoading: false });
    }
  },

  clearError: () => set({ error: null })
}));
