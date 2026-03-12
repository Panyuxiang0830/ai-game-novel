// frontend/src/stores/gameStore.ts
import { create } from 'zustand';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export interface PlayerState {
  health: number;
  hunger: number;
  thirst: number;
  temperature: number;
  sanity: number;
  strength: number;
  agility: number;
  intelligence: number;
  charisma: number;
  perception: number;
  conditions: string[];
  inventory: any[];
}

export interface GameState {
  session_id: string;
  scenario_id: string;
  player: PlayerState;
  current_location: string;
  time_elapsed: number;
  status: string;
}

export interface GameTurn {
  turn_num: number;
  player_input: string;
  ai_response: string;
  state_changes: Record<string, number>;
  options: string[];
  is_key_event: boolean;
}

interface GameStore {
  // 状态
  currentSession: GameState | null;
  history: GameTurn[];
  isLoading: boolean;
  error: string | null;

  // Actions
  createSession: (scenarioId: string, apiKey: string, config?: any) => Promise<void>;
  processTurn: (action: string, context: string, apiKey?: string) => Promise<void>;
  getSession: (sessionId: string) => Promise<void>;
  getHistory: (sessionId: string) => Promise<void>;
  clearError: () => void;
}

export const useGameStore = create<GameStore>((set, get) => ({
  currentSession: null,
  history: [],
  isLoading: false,
  error: null,

  createSession: async (scenarioId: string, apiKey: string, config?: any) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/games/create`, {
        scenario_id: scenarioId,
        api_key: apiKey,
        config: config || { scenario_id: scenarioId }
      });
      set({ currentSession: response.data, history: [], isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '创建游戏失败', isLoading: false });
    }
  },

  processTurn: async (action: string, context: string, apiKey?: string) => {
    set({ isLoading: true, error: null });
    const { currentSession } = get();
    if (!currentSession) return;

    // 获取 API key
    const effectiveApiKey = apiKey || localStorage.getItem('anthropic_api_key');

    try {
      const response = await axios.post(
        `${API_BASE}/games/${currentSession.session_id}/turn`,
        {
          action,
          input_type: 'free',
          context,
          api_key: effectiveApiKey
        }
      );

      set(state => ({
        history: [...state.history, response.data],
        currentSession: response.data.session ? response.data.session : state.currentSession,
        isLoading: false
      }));
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '处理回合失败', isLoading: false });
    }
  },

  getSession: async (sessionId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/games/${sessionId}`);
      set({ currentSession: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取游戏失败', isLoading: false });
    }
  },

  getHistory: async (sessionId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/games/${sessionId}/history`);
      set({ history: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取历史失败', isLoading: false });
    }
  },

  clearError: () => set({ error: null })
}));
