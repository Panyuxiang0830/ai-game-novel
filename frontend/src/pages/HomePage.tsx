// frontend/src/pages/HomePage.tsx
import { useEffect, useState } from 'react';
import { useScenarioStore } from '../stores/scenarioStore';
import { useGameStore } from '../stores/gameStore';
import { useNavigate } from 'react-router-dom';
import ScenarioCard from '../components/ScenarioCard';

export default function HomePage() {
  const { scenarios, fetchScenarios, isLoading, error } = useScenarioStore();
  const { createSession } = useGameStore();
  const navigate = useNavigate();
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);

  useEffect(() => {
    fetchScenarios();
  }, [fetchScenarios]);

  const handleSelectScenario = async (scenarioId: string) => {
    setSelectedScenario(scenarioId);
  };

  const handleStartGame = async () => {
    if (!selectedScenario) return;

    await createSession(selectedScenario);
    navigate('/game');
  };

  return (
    <div className="min-h-screen bg-apocalypse-bg p-8">
      <div className="max-w-4xl mx-auto">
        {/* 标题 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-apocalypse-text mb-4">
            末世生存小说生成器
          </h1>
          <p className="text-apocalypse-muted">
            选择一个末世场景，开始你的生存之旅。AI将根据你的选择实时生成属于你的小说。
          </p>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-apocalypse-danger/20 border border-apocalypse-danger
                         text-apocalypse-danger rounded-lg">
            {error}
          </div>
        )}

        {/* 场景选择 */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {scenarios.map((scenario) => (
            <ScenarioCard
              key={scenario.id}
              scenario={scenario}
              onSelect={handleSelectScenario}
            />
          ))}
        </div>

        {/* 开始按钮 */}
        {selectedScenario && (
          <div className="text-center">
            <button
              onClick={handleStartGame}
              disabled={isLoading}
              className="px-8 py-4 bg-apocalypse-warning text-black font-bold text-lg
                         rounded-lg hover:bg-apocalypse-warning/80 disabled:opacity-50
                         disabled:cursor-not-allowed transition-all shadow-lg
                         shadow-apocalypse-warning/30"
            >
              {isLoading ? '创建中...' : '开始游戏'}
            </button>
          </div>
        )}

        {/* 自定义场景入口 */}
        <div className="mt-12 text-center">
          <button
            className="text-apocalypse-muted hover:text-apocalypse-text transition-colors"
          >
            + 创建自定义场景
          </button>
        </div>
      </div>
    </div>
  );
}
