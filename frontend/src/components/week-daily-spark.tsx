import { WashiCard } from "./washi-card";

interface WeekDailySparkProps {
  counts: number[];
  labels?: string[];
}

const WIDTH = 280;
const HEIGHT = 72;
const PAD_X = 8;
const PAD_Y = 10;

export function WeekDailySpark({ counts, labels }: WeekDailySparkProps) {
  const max = Math.max(...counts, 1);
  const step = counts.length > 1 ? (WIDTH - PAD_X * 2) / (counts.length - 1) : 0;

  const points = counts.map((count, index) => {
    const x = PAD_X + step * index;
    const y = HEIGHT - PAD_Y - (count / max) * (HEIGHT - PAD_Y * 2);
    return `${x},${y}`;
  });

  const areaPoints = [
    `${PAD_X},${HEIGHT - PAD_Y}`,
    ...points,
    `${PAD_X + step * (counts.length - 1)},${HEIGHT - PAD_Y}`,
  ].join(" ");

  return (
    <WashiCard>
      <p className="page-eyebrow mb-4">ритм недели</p>
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        className="w-full"
        role="img"
        aria-label="График записей по дням"
      >
        <line
          x1={PAD_X}
          y1={HEIGHT - PAD_Y}
          x2={WIDTH - PAD_X}
          y2={HEIGHT - PAD_Y}
          className="haiku-spark-axis"
        />
        <polygon points={areaPoints} className="haiku-spark-fill" />
        <polyline points={points.join(" ")} className="haiku-spark-line" />
        {counts.map((count, index) => {
          const x = PAD_X + step * index;
          const y = HEIGHT - PAD_Y - (count / max) * (HEIGHT - PAD_Y * 2);
          return (
            <g key={index}>
              <circle cx={x} cy={y} r={count > 0 ? 3 : 2} className="haiku-spark-dot" />
              {labels?.[index] && (
                <text x={x} y={HEIGHT - 2} className="haiku-spark-label" textAnchor="middle">
                  {labels[index]}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </WashiCard>
  );
}
