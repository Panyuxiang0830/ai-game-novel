// frontend/src/pages/NovelPage.tsx
import { useEffect, useState } from 'react';
import { useNovelStore } from '../stores/novelStore';
import { useGameStore } from '../stores/gameStore';
import NovelReader from '../components/NovelReader';

export default function NovelPage() {
  const { currentNovel, createNovel, generateChapter, isLoading, error } = useNovelStore();
  const { currentSession, history } = useGameStore();
  const [novelCreated, setNovelCreated] = useState(false);

  // 游戏结束后自动创建小说
  useEffect(() => {
    if (currentSession?.status === 'ended' && !novelCreated && !currentNovel) {
      handleCreateNovel();
    }
  }, [currentSession]);

  const handleCreateNovel = async () => {
    if (!currentSession) return;

    // 构建玩家背景描述
    const playerBackground = history
      .filter(t => t.is_key_event)
      .map(t => t.ai_response.slice(0, 100))
      .join('; ');

    await createNovel(
      currentSession.session_id,
      currentSession.scenario_id,
      playerBackground
    );
    setNovelCreated(true);
  };

  const handleGenerateChapter = async (chapterNum: number) => {
    if (!currentNovel) return;

    // 获取该章节对应的事件上下文
    const eventContext = history[chapterNum - 1]?.ai_response || '章节开始';

    await generateChapter(currentNovel.novel_id, chapterNum, eventContext);
  };

  if (!currentNovel) {
    return (
      <div className="min-h-screen bg-apocalypse-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin mb-4">⏳</div>
          <p className="text-apocalypse-muted">
            {isLoading ? '正在创建小说...' : '加载中...'}
          </p>
          {error && (
            <div className="mt-4 p-4 bg-apocalypse-danger/20 text-apocalypse-danger rounded-lg">
              {error}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-apocalypse-bg p-8">
      <div className="max-w-4xl mx-auto">
        {/* 返回按钮 */}
        <button
          onClick={() => window.history.back()}
          className="mb-6 text-apocalypse-muted hover:text-apocalypse-text transition-colors"
        >
          ← 返回
        </button>

        {error && (
          <div className="mb-6 p-4 bg-apocalypse-danger/20 border border-apocalypse-danger
                         text-apocalypse-danger rounded-lg">
            {error}
          </div>
        )}

        <NovelReader
          novel={currentNovel}
          onGenerateChapter={handleGenerateChapter}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
