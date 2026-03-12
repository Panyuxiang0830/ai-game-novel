// frontend/src/components/GameNarrative.tsx
import { GameTurn } from '../stores/gameStore';
import ReactMarkdown from 'react-markdown';

interface GameNarrativeProps {
  history: GameTurn[];
}

export default function GameNarrative({ history }: GameNarrativeProps) {
  if (history.length === 0) {
    return (
      <div className="bg-apocalypse-card border border-apocalypse-border rounded-lg p-8
                     text-center text-apocalypse-muted">
        <p>游戏即将开始...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-h-[500px] overflow-y-auto pr-2">
      {history.map((turn) => (
        <div
          key={turn.turn_num}
          className={`bg-apocalypse-card border rounded-lg p-6 ${
            turn.is_key_event
              ? 'border-apocalypse-warning shadow-lg shadow-apocalypse-warning/20'
              : 'border-apocalypse-border'
          }`}
        >
          {turn.is_key_event && (
            <div className="inline-block px-3 py-1 mb-3 text-xs font-bold
                           bg-apocalypse-warning text-black rounded-full">
              关键事件
            </div>
          )}

          <div className="prose prose-invert max-w-none">
            <ReactMarkdown>{turn.ai_response}</ReactMarkdown>
          </div>

          {turn.options && turn.options.length > 0 && (
            <div className="mt-4 pt-4 border-t border-apocalypse-border">
              <p className="text-sm text-apocalypse-muted mb-2">可选行动:</p>
              <div className="space-y-2">
                {turn.options.map((option, i) => (
                  <div
                    key={i}
                    className="px-4 py-2 bg-apocalypse-bg rounded text-apocalypse-text
                               hover:bg-apocalypse-border transition-colors cursor-pointer"
                  >
                    {option}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
