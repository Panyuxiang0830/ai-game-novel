// frontend/src/components/ApiKeySetup.tsx
import { useState } from 'react';

interface ApiKeySetupProps {
  onApiKeySet: (apiKey: string) => void;
}

export default function ApiKeySetup({ onApiKeySet }: ApiKeySetupProps) {
  const [apiKey, setApiKey] = useState('');
  const [showInput, setShowInput] = useState(false);

  const handleSubmit = () => {
    if (apiKey.trim()) {
      // 保存到 localStorage
      localStorage.setItem('anthropic_api_key', apiKey.trim());
      onApiKeySet(apiKey.trim());
    }
  };

  const handleSkip = () => {
    onApiKeySet('');
  };

  return (
    <div className="min-h-screen bg-apocalypse-bg flex items-center justify-center p-8">
      <div className="bg-apocalypse-card border border-apocalypse-border rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold text-apocalypse-text mb-4 text-center">
          欢迎来到末世生存小说生成器
        </h2>

        <div className="mb-6 text-apocalypse-muted text-sm space-y-3">
          <p>
            这个游戏使用 Claude AI 生成故事内容。请提供你的 Anthropic API Key 以开始游戏。
          </p>
          <div className="bg-apocalypse-bg border border-apocalypse-border rounded p-4 text-xs">
            <p className="font-semibold text-apocalypse-text mb-2">如何获取 API Key：</p>
            <ol className="list-decimal list-inside space-y-1">
              <li>访问 <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer" className="text-apocalypse-warning hover:underline">console.anthropic.com</a></li>
              <li>登录或注册账号</li>
              <li>在 API Keys 部分创建新的 key</li>
              <li>复制并粘贴到下方输入框</li>
            </ol>
            <p className="mt-3 text-apocalypse-warning">
              注意：API Key 只存储在本地浏览器中，不会发送到任何第三方服务器。
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm text-apocalypse-text mb-2">
              Anthropic API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-ant-..."
              className="w-full bg-apocalypse-bg text-apocalypse-text rounded p-3
                         border border-apocalypse-border focus:border-apocalypse-warning
                         focus:outline-none"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={!apiKey.trim()}
            className="w-full py-3 bg-apocalypse-warning text-black font-bold
                       rounded-lg hover:bg-apocalypse-warning/80 disabled:opacity-50
                       disabled:cursor-not-allowed transition-colors"
          >
            开始游戏
          </button>

          <button
            onClick={handleSkip}
            className="w-full py-2 text-apocalypse-muted hover:text-apocalypse-text
                       text-sm transition-colors"
          >
            稍后设置（使用后端配置的 API Key）
          </button>
        </div>
      </div>
    </div>
  );
}
