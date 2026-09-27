import React from 'react';
import { Activity, ShieldCheck } from 'lucide-react';

export default function WellnessScoreGauge({ score, stateLabel }) {
  // Clamp score between 0 and 100
  const normalizedScore = Math.max(0, Math.min(100, Math.round(score || 0)));

  // Circular gauge geometry
  const radius = 60;
  const strokeWidth = 9;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  // Harmonious color styling based on score
  let strokeColor = '#2F855A'; // Emerald/Sage
  let badgeStyle = 'bg-emerald-50 text-emerald-800 border-emerald-200';

  if (normalizedScore < 40) {
    strokeColor = '#B06840'; // Ochre/Warm rust
    badgeStyle = 'bg-amber-50 text-amber-900 border-amber-200';
  } else if (normalizedScore < 65) {
    strokeColor = '#D97706'; // Amber
    badgeStyle = 'bg-amber-50 text-amber-800 border-amber-200';
  }

  return (
    <div className="flex flex-col sm:flex-row items-center gap-6 sm:gap-8 p-6 sm:p-8 rounded-2xl bg-white border border-parchment-300/80 shadow-soft print-border-subtle">
      {/* SVG Circular Meter */}
      <div className="relative flex-shrink-0 w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 150 150">
          {/* Background track */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke="#EFEBE4"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Active progress arc */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center score readout */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="font-serif text-3xl sm:text-4xl font-bold text-sage-900 leading-none">
            {normalizedScore}%
          </span>
          <span className="text-[11px] font-medium text-[#7E8B85] uppercase tracking-wider mt-1">
            Wellness Score
          </span>
        </div>
      </div>

      {/* Primary Narrative & Interpretation */}
      <div className="space-y-3 text-center sm:text-left flex-1">
        <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${badgeStyle}`}>
            <Activity className="w-3.5 h-3.5 mr-1.5" />
            {stateLabel || 'Current State'}
          </span>
          <span className="inline-flex items-center text-xs text-[#7E8B85]">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-sage-600" />
            Self-Reported Balance
          </span>
        </div>

        <h2 className="font-serif text-xl sm:text-2xl font-bold text-sage-900 leading-snug">
          Your Mental-Wellness Balance
        </h2>

        <p className="text-xs sm:text-sm text-[#4A5550] leading-relaxed">
          Your responses reflect an overall wellness rating of <strong>{normalizedScore}%</strong>. 
          This score synthesizes positive inner anchors—such as calmness, mental clarity, and consistent routine—with your current level of daily strain.
        </p>
      </div>
    </div>
  );
}
