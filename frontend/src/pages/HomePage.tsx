// frontend/src/pages/HomePage.tsx
import { useEffect, useState } from 'react';
import { useScenarioStore } from '../stores/scenarioStore';
import { useGameStore } from '../stores/gameStore';
import { useNavigate } from 'react-router-dom';
import ScenarioCard from '../components/ScenarioCard';
import ApiKeySetup from '../components/ApiKeySetup';

export default function HomePage() {
  const { scenarios, fetchScenarios, isLoading, error, clearError } = useScenarioStore();
  const { createSession } = useGameStore();
  const navigate = useNavigate();
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [showApiSetup, setShowApiSetup] = useState(false);

  useEffect(() => {
    fetchScenarios();
    // 检查本地存储的 API key
    const storedKey = localStorage.getItem('anthropic_api_key');
    if (storedKey) {
      setApiKey(storedKey);
    }
  }, [fetchScenarios]);

  const handleSelectScenario = (scenarioId: string) => {
    setSelectedScenario(scenarioId);
    // 如果没有 API key，显示设置界面
    if (!apiKey) {
      setShowApiSetup(true);
    }
  };

  const handleStartGame = async () => {
    if (!selectedScenario) return;

    // 如果没有 API key，显示设置界面
    if (!apiKey) {
      setShowApiSetup(true);
      return;
    }

    await createSession(selectedScenario, apiKey);
    navigate('/game');
  };

  const handleApiKeySet = (key: string) => {
    setApiKey(key);
    setShowApiSetup(false);
    // 如果已经选择了场景，自动开始游戏
    if (selectedScenario && key) {
      createSession(selectedScenario, key);
      navigate('/game');
    }
  };

  // 显示 API Key 设置界面
  if (showApiSetup) {
    return <ApiKeySetup onApiKeySet={handleApiKeySet} />;
  }

  return (
    <div className="min-h-screen bg-apocalypse-bg p-8">
      <div className="max-w-4xl mx-auto">
        {/* 顶部状态栏 */}
        <div className="flex justify-between items-center mb-8">
          <div></div>
          <div className="flex items-center gap-2">
            <span className={`text-sm ${apiKey ? 'text-apocalypse-success' : 'text-apocalypse-muted'}`}>
              {apiKey ? '✓ API Key 已配置' : '⚠ 需要配置 API Key'}
            </span>
            <button
              onClick={() => setShowApiSetup(true)}
              className="text-sm text-apocalypse-muted hover:text-apocalypse-text underline"
            >
              {apiKey ? '更换' : '设置'}
            </button>
          </div>
        </div>

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
                         text-apocalypse-danger rounded-lg flex justify-between items-center">
            <span>{error}</span>
            <button onClick={clearError} className="underline">关闭</button>
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
            {!apiKey && (
              <p className="mb-4 text-apocalypse-warning">
                请先配置 API Key 以开始游戏
              </p>
            )}
            <button
              onClick={handleStartGame}
              disabled={isLoading || !apiKey}
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
