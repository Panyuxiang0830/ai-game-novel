// frontend/src/pages/GamePage.tsx
import { useState, useEffect } from 'react';
import { useGameStore } from '../stores/gameStore';
import { useNovelStore } from '../stores/novelStore';
import PlayerStats from '../components/PlayerStats';
import GameNarrative from '../components/GameNarrative';

export default function GamePage() {
  const { currentSession, history, processTurn, isLoading, error, clearError } = useGameStore();
  const [inputValue, setInputValue] = useState('');
  const [showNovel, setShowNovel] = useState(false);

  const handleSubmit = async () => {
    if (!inputValue.trim()) return;

    const context = history.length > 0
      ? history[history.length - 1].ai_response
      : currentSession ? '游戏开始' : '';

    await processTurn(inputValue, context);
    setInputValue('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  if (!currentSession) {
    return (
      <div className="min-h-screen bg-apocalypse-bg flex items-center justify-center">
        <p className="text-apocalypse-muted">加载中...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-apocalypse-bg">
      {/* 顶部栏 */}
      <div className="bg-apocalypse-card border-b border-apocalypse-border p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-apocalypse-text">末世生存</h1>
          <div className="flex gap-4 text-sm text-apocalypse-muted">
            <span>回合: {currentSession.time_elapsed}</span>
            <span>状态: {currentSession.status}</span>
          </div>
          <button
            onClick={() => setShowNovel(!showNovel)}
            className="px-4 py-2 bg-apocalypse-border text-apocalypse-text rounded
                       hover:bg-apocalypse-muted transition-colors"
          >
            {showNovel ? '返回游戏' : '查看小说'}
          </button>
        </div>
      </div>

      {/* 主内容 */}
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-4 gap-6">
          {/* 左侧：玩家状态 */}
          <div className="col-span-1">
            <PlayerStats player={currentSession.player} />
          </div>

          {/* 右侧：游戏内容 */}
          <div className="col-span-3">
            {error && (
              <div className="mb-4 p-4 bg-apocalypse-danger/20 border border-apocalypse-danger
                             text-apocalypse-danger rounded-lg">
                {error}
                <button onClick={clearError} className="ml-4 underline">关闭</button>
              </div>
            )}

            <GameNarrative history={history} />

            {/* 输入区域 */}
            <div className="mt-6 bg-apocalypse-card border border-apocalypse-border rounded-lg p-4">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="描述你的行动..."
                className="w-full bg-apocalypse-bg text-apocalypse-text rounded p-3
                           border border-apocalypse-border focus:border-apocalypse-warning
                           focus:outline-none resize-none"
                rows={3}
                disabled={isLoading || currentSession.status !== 'active'}
              />
              <div className="mt-3 flex justify-end">
                <button
                  onClick={handleSubmit}
                  disabled={isLoading || !inputValue.trim() || currentSession.status !== 'active'}
                  className="px-6 py-2 bg-apocalypse-warning text-black font-semibold
                             rounded-lg hover:bg-apocalypse-warning/80 disabled:opacity-50
                             disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? '处理中...' : '执行行动'}
                </button>
              </div>
            </div>

            {/* 游戏结束提示 */}
            {currentSession.status === 'ended' && (
              <div className="mt-6 p-6 bg-apocalypse-card border-2 border-apocalypse-danger
                             rounded-lg text-center">
                <h2 className="text-2xl font-bold text-apocalypse-danger mb-4">
                  游戏结束
                </h2>
                <p className="text-apocalypse-muted mb-4">
                  你的末世生存之旅到此为止。但故事会以另一种形式继续...
                </p>
                <button
                  onClick={() => setShowNovel(true)}
                  className="px-6 py-3 bg-apocalypse-warning text-black font-bold
                             rounded-lg hover:bg-apocalypse-warning/80 transition-colors"
                >
                  查看生成的小说
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
