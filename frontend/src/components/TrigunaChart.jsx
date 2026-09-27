import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { Feather, Flame, Moon, Info } from 'lucide-react';

export default function TrigunaChart({ sattvaScore, rajasScore, tamasScore, dominantPattern }) {
  const chartData = [
    {
      guna: 'Sattva (सत्त्व)',
      tendency: Math.round(sattvaScore || 0),
      color: '#2E7D32',
      meaning: 'Clarity, serenity, and emotional composure',
    },
    {
      guna: 'Rajas (रजस्)',
      tendency: Math.round(rajasScore || 0),
      color: '#D97706',
      meaning: 'Movement, restlessness, and passionate drive',
    },
    {
      guna: 'Tamas (तमस्)',
      tendency: Math.round(tamasScore || 0),
      color: '#475569',
      meaning: 'Inertia, fatigue, and heaviness',
    },
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-md border border-parchment-300 text-xs space-y-1">
          <p className="font-semibold text-sage-900">{data.guna}</p>
          <p className="text-sage-700">
            Tendency Score: <strong className="font-mono font-bold">{data.tendency}%</strong>
          </p>
          <p className="text-[#6B7770] italic text-[11px]">{data.meaning}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 rounded-2xl bg-white border border-parchment-300/80 shadow-soft space-y-5 print-border-subtle">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-parchment-200 pb-3.5 gap-2">
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-sage-600 block">
            Indian Psychology Framework (Sāṁkhya-Yoga)
          </span>
          <h3 className="font-serif text-lg font-semibold text-sage-900">
            Triguna Tendency Profile
          </h3>
        </div>
        {dominantPattern && (
          <span className="self-start sm:self-auto text-xs font-semibold px-3 py-1 rounded-full bg-parchment-100 text-sage-800 border border-parchment-300">
            Current Pattern: {dominantPattern}
          </span>
        )}
      </div>

      <p className="text-xs text-[#5C6863] leading-relaxed">
        In the context of Indian Psychology, every individual experiences an ever-shifting combination of three primary qualities (Gunas). 
        These reflect current tendencies of mind, not permanent traits.
      </p>

      {/* Simple, Clean Bar Chart */}
      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <XAxis
              type="number"
              domain={[0, 100]}
              tick={{ fontSize: 11, fill: '#6B7770' }}
              tickFormatter={(v) => `${v}%`}
            />
            <YAxis
              dataKey="guna"
              type="category"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#23342E', fontWeight: 500 }}
              width={100}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(242, 236, 225, 0.4)' }} />
            <Bar dataKey="tendency" radius={[0, 6, 6, 0]} barSize={20}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 3 Conceptual Tendency Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
        {/* Sattva */}
        <div className="p-3.5 rounded-xl border border-sattva-border/70 bg-sattva-light/30 space-y-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1.5 text-sattva">
              <Feather className="w-3.5 h-3.5" />
              <span className="text-xs font-semibold">Sattva</span>
            </div>
            <span className="text-xs font-bold font-mono text-sattva">
              {Math.round(sattvaScore || 0)}%
            </span>
          </div>
          <p className="text-[11px] text-[#4A5550] leading-snug">
            Equilibrium, mental stillness, clarity (prakāśa), and serene contentment.
          </p>
        </div>

        {/* Rajas */}
        <div className="p-3.5 rounded-xl border border-rajas-border/70 bg-rajas-light/30 space-y-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1.5 text-rajas">
              <Flame className="w-3.5 h-3.5" />
              <span className="text-xs font-semibold">Rajas</span>
            </div>
            <span className="text-xs font-bold font-mono text-rajas">
              {Math.round(rajasScore || 0)}%
            </span>
          </div>
          <p className="text-[11px] text-[#4A5550] leading-snug">
            Active motion, cognitive restlessness (calatva), and emotional drive.
          </p>
        </div>

        {/* Tamas */}
        <div className="p-3.5 rounded-xl border border-tamas-border/70 bg-tamas-light/30 space-y-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1.5 text-tamas">
              <Moon className="w-3.5 h-3.5" />
              <span className="text-xs font-semibold">Tamas</span>
            </div>
            <span className="text-xs font-bold font-mono text-tamas">
              {Math.round(tamasScore || 0)}%
            </span>
          </div>
          <p className="text-[11px] text-[#4A5550] leading-snug">
            Inertia (ālasya), lethargy, heaviness, and routine irregularity.
          </p>
        </div>
      </div>
    </div>
  );
}
