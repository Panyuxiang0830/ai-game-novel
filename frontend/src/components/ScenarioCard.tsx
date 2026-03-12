// frontend/src/components/ScenarioCard.tsx
import { Scenario } from '../stores/scenarioStore';

interface ScenarioCardProps {
  scenario: Scenario;
  onSelect: (scenarioId: string) => void;
}

export default function ScenarioCard({ scenario, onSelect }: ScenarioCardProps) {
  return (
    <div
      onClick={() => onSelect(scenario.id)}
      className="bg-apocalypse-card border border-apocalypse-border rounded-lg p-6 cursor-pointer
                 hover:border-apocalypse-muted transition-all duration-300 hover:shadow-lg
                 hover:shadow-apocalypse-muted/20"
    >
      <h3 className="text-xl font-bold text-apocalypse-text mb-2">{scenario.name}</h3>
      <p className="text-apocalypse-muted text-sm mb-4">{scenario.description}</p>

      <div className="space-y-2 text-xs text-apocalypse-muted">
        <div className="flex items-center gap-2">
          <span className="font-semibold">叙事风格:</span>
          <span>{scenario.narrative_style}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold">可能事件:</span>
          <span>{scenario.possible_events.length} 种</span>
        </div>
      </div>
    </div>
  );
}
