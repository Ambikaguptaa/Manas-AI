import React from 'react';
import { 
  Sparkles, 
  AlertTriangle, 
  Wind, 
  Clock, 
  Smile, 
  Zap, 
  Target, 
  Compass, 
  CheckCircle2 
} from 'lucide-react';

export default function ContributingFactorCard({ factor }) {
  const isSupportive = factor.impact_type === 'supportive';

  // Map internal dimension to representative icon
  const getDimensionIcon = (dim) => {
    switch (dim) {
      case 'restlessness':
      case 'overwhelm':
        return <Wind className="w-4 h-4" />;
      case 'routine':
        return <Clock className="w-4 h-4" />;
      case 'calmness':
        return <Smile className="w-4 h-4" />;
      case 'energy':
        return <Zap className="w-4 h-4" />;
      case 'concentration':
        return <Target className="w-4 h-4" />;
      case 'mental_clarity':
        return <Sparkles className="w-4 h-4" />;
      default:
        return <Compass className="w-4 h-4" />;
    }
  };

  return (
    <div
      className={`p-4 rounded-xl border transition-all duration-200 flex flex-col justify-between space-y-2.5 print-border-subtle print-break-inside-avoid ${
        isSupportive
          ? 'bg-emerald-50/40 border-emerald-200/80 hover:bg-emerald-50/70'
          : 'bg-amber-50/40 border-amber-200/80 hover:bg-amber-50/70'
      }`}
    >
      <div className="space-y-2">
        {/* Badge Row */}
        <div className="flex items-center justify-between gap-2">
          <span
            className={`inline-flex items-center space-x-1 text-[11px] font-semibold px-2 py-0.5 rounded-full border ${
              isSupportive
                ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                : 'bg-amber-100 text-amber-900 border-amber-300'
            }`}
          >
            {isSupportive ? (
              <>
                <CheckCircle2 className="w-3 h-3" />
                <span>Supportive Anchor</span>
              </>
            ) : (
              <>
                <AlertTriangle className="w-3 h-3" />
                <span>Focus Area</span>
              </>
            )}
          </span>

          <span className="font-mono text-xs font-semibold text-[#5C6863]">
            {factor.score?.toFixed(1)} / 5.0
          </span>
        </div>

        {/* Title */}
        <div className="flex items-start space-x-2">
          <span
            className={`mt-0.5 p-1 rounded-md ${
              isSupportive
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-amber-100 text-amber-700'
            }`}
          >
            {getDimensionIcon(factor.dimension)}
          </span>
          <h4 className="font-serif text-sm font-semibold text-sage-900 leading-snug">
            {factor.factor_name}
          </h4>
        </div>

        {/* Narrative Summary */}
        <p className="text-xs text-[#4A5550] leading-relaxed">
          {factor.summary}
        </p>
      </div>

      <div className="text-[10px] text-[#7E8B85] pt-1 border-t border-parchment-200/60">
        {isSupportive ? 'Internal strength to lean on' : 'Gentle adjustments may support balance'}
      </div>
    </div>
  );
}
