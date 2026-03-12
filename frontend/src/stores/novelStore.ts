// frontend/src/stores/novelStore.ts
import { create } from 'zustand';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

interface NovelChapter {
  chapter_num: number;
  title: string;
  event_title: string;
  content: string;
  word_count: number;
  status: string;
}

interface NovelSkeleton {
  premise: string;
  estimated_chapters: number;
  chapter_outlines: any[];
  narrative_style: string;
  main_character_arc: string;
}

interface NovelProject {
  novel_id: string;
  session_id: string;
  scenario_id: string;
  skeleton: NovelSkeleton | null;
  chapters: NovelChapter[];
  total_words: number;
  status: string;
}

interface NovelStore {
  // 状态
  currentNovel: NovelProject | null;
  novels: NovelProject[];
  isLoading: boolean;
  error: string | null;

  // Actions
  createNovel: (sessionId: string, scenarioId: string, playerBackground?: string) => Promise<void>;
  getNovel: (novelId: string) => Promise<void>;
  generateChapter: (novelId: string, chapterNum: number, eventContext: string) => Promise<void>;
  exportNovel: (novelId: string) => Promise<string>;
  listNovels: () => Promise<void>;
  clearError: () => void;
}

export const useNovelStore = create<NovelStore>((set, get) => ({
  currentNovel: null,
  novels: [],
  isLoading: false,
  error: null,

  createNovel: async (sessionId: string, scenarioId: string, playerBackground = '') => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/novels/create`, {
        session_id: sessionId,
        scenario_id: scenarioId,
        player_background: playerBackground
      });
      set({ currentNovel: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '创建小说失败', isLoading: false });
    }
  },

  getNovel: async (novelId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/novels/${novelId}`);
      set({ currentNovel: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取小说失败', isLoading: false });
    }
  },

  generateChapter: async (novelId: string, chapterNum: number, eventContext: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post(
        `${API_BASE}/novels/${novelId}/chapter/${chapterNum}/generate`,
        { event_context: eventContext }
      );
      // 更新当前小说的章节
      const { currentNovel } = get();
      if (currentNovel) {
        const updatedChapters = [...currentNovel.chapters];
        updatedChapters[chapterNum - 1] = response.data;
        set({
          currentNovel: {
            ...currentNovel,
            chapters: updatedChapters
          },
          isLoading: false
        });
      }
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '生成章节失败', isLoading: false });
    }
  },

  exportNovel: async (novelId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/novels/${novelId}/export`);
      set({ isLoading: false });
      return response.data.text;
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '导出小说失败', isLoading: false });
      return '';
    }
  },

  listNovels: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/novels/list/all`);
      set({ novels: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || '获取小说列表失败', isLoading: false });
    }
  },

  clearError: () => set({ error: null })
}));
