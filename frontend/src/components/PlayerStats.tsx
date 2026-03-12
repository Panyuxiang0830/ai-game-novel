// frontend/src/components/PlayerStats.tsx
import type { PlayerState } from '../stores/gameStore';

interface PlayerStatsProps {
  player: PlayerState;
}

export default function PlayerStats({ player }: PlayerStatsProps) {
  const stats = [
    { label: '生命', value: player.health, color: 'bg-red-500' },
    { label: '饥饿', value: player.hunger, color: 'bg-orange-500' },
    { label: '口渴', value: player.thirst, color: 'bg-blue-500' },
    { label: '精神', value: player.sanity, color: 'bg-purple-500' },
    { label: '力量', value: player.strength, color: 'bg-yellow-600' },
    { label: '敏捷', value: player.agility, color: 'bg-green-500' },
    { label: '智力', value: player.intelligence, color: 'bg-blue-400' },
    { label: '感知', value: player.perception, color: 'bg-pink-500' },
  ];

  return (
    <div className="bg-apocalypse-card border border-apocalypse-border rounded-lg p-4">
      <h3 className="text-lg font-bold text-apocalypse-text mb-4">生存状态</h3>

      <div className="space-y-3">
        {stats.map(stat => (
          <div key={stat.label}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-apocalypse-muted">{stat.label}</span>
              <span className="text-apocalypse-text">{stat.value}/100</span>
            </div>
            <div className="h-2 bg-apocalypse-bg rounded-full overflow-hidden">
              <div
                className={`h-full ${stat.color} transition-all duration-500`}
                style={{ width: `${stat.value}%` }}
              />
            </div>
          </div>
        ))}

        <div className="pt-2 border-t border-apocalypse-border">
          <div className="flex justify-between text-sm">
            <span className="text-apocalypse-muted">体温</span>
            <span className="text-apocalypse-text">{player.temperature.toFixed(1)}°C</span>
          </div>
        </div>

        {player.conditions.length > 0 && (
          <div className="pt-2 border-t border-apocalypse-border">
            <span className="text-sm text-apocalypse-muted">状态: </span>
            {player.conditions.map((cond, i) => (
              <span
                key={i}
                className="inline-block ml-1 px-2 py-0.5 text-xs bg-apocalypse-danger/20
                           text-apocalypse-danger rounded"
              >
                {cond}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
