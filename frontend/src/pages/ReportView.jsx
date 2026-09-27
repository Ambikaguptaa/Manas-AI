import React from 'react';
import { 
  Printer, 
  RotateCcw, 
  Home, 
  Leaf, 
  Clock, 
  Calendar, 
  Info, 
  ShieldCheck, 
  Sparkles,
  Award,
  Activity
} from 'lucide-react';
import TrigunaChart from '../components/TrigunaChart';
import ContributingFactorCard from '../components/ContributingFactorCard';
import CrisisSupportNotice from '../components/CrisisSupportNotice';

export default function ReportView({ result, onRetake, onHome }) {
  const {
    assessment_id,
    wellness_score,
    wellness_state,
    interpretation,
    sattva_score,
    rajas_score,
    tamas_score,
    chitta_vikshepa_indicator,
    dominant_pattern,
    overall_wellness_score,
    iks_interpretation,
    ml_prediction,
    recommendations,
    contributing_factors,
    is_high_distress,
    disclaimer
  } = result;

  const displayId = assessment_id || 'mwa_session';
  const displayScore = Math.max(0, Math.min(100, Math.round(wellness_score ?? overall_wellness_score ?? 0)));
  const displayState = wellness_state ?? iks_interpretation?.overall_wellness_state ?? (typeof ml_prediction === 'string' ? ml_prediction : ml_prediction?.predicted_label) ?? 'Evaluation Complete';
  const displaySattva = sattva_score ?? iks_interpretation?.sattva_score ?? 0;
  const displayRajas = rajas_score ?? iks_interpretation?.rajas_score ?? 0;
  const displayTamas = tamas_score ?? iks_interpretation?.tamas_score ?? 0;
  const displayVikshepa = chitta_vikshepa_indicator ?? iks_interpretation?.chitta_vikshepa_indicator ?? 'Mild Chitta Vikṣepa';
  const displayVikshepaDetails = iks_interpretation?.chitta_vikshepa_details || 'Occasional fluctuations of attention that can be gently regulated through breath awareness and short pauses.';
  const displayDominant = dominant_pattern ?? iks_interpretation?.dominant_pattern ?? '';
  const displayExplanation = interpretation ?? iks_interpretation?.explanation ?? 'Your responses indicate an overall moderate balance.';

  // Circular gauge calculations
  const radius = 60;
  const strokeWidth = 9;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (displayScore / 100) * circumference;

  let strokeColor = '#2F855A'; // Emerald/Sage (>=65)
  let badgeStyle = 'bg-emerald-50 text-emerald-800 border-emerald-200';

  if (displayScore < 40) {
    strokeColor = '#B06840'; // Ochre/Rust
    badgeStyle = 'bg-amber-50 text-amber-900 border-amber-200';
  } else if (displayScore < 65) {
    strokeColor = '#D97706'; // Amber
    badgeStyle = 'bg-amber-50 text-amber-800 border-amber-200';
  }

  const handlePrint = () => {
    window.print();
  };

  const currentDate = new Date().toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });

  return (
    <div className="space-y-8 max-w-3xl mx-auto pb-12 print:p-0 print:m-0 print:max-w-none">
      {/* 1. Unified Hero Result Card — Communicates results within 3 seconds */}
      <section className="bg-white rounded-2xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6 print-border-subtle">
        {/* Top utility row */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-parchment-200 pb-4 gap-3">
          <div>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-sage-600 block">
              Assessment Summary • {currentDate}
            </span>
            <h1 className="text-2xl sm:text-3xl font-serif font-bold text-sage-900 leading-tight">
              Mental-Wellness Results
            </h1>
          </div>

          <div className="flex items-center space-x-2 no-print">
            <button
              type="button"
              onClick={handlePrint}
              className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-white hover:bg-parchment-100 border border-parchment-300 text-xs font-medium text-sage-800 transition-colors cursor-pointer"
              title="Print report or save as PDF"
            >
              <Printer className="w-3.5 h-3.5 text-sage-600" />
              <span>Print / PDF</span>
            </button>

            <button
              type="button"
              onClick={onRetake}
              className="inline-flex items-center space-x-1 px-3 py-2 rounded-xl border border-parchment-300 bg-white hover:bg-parchment-50 text-xs text-[#5C6863] transition-colors cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5 text-[#7E8B85]" />
              <span>Retake</span>
            </button>
          </div>
        </div>

        {/* Immediate visual readout */}
        <div className="flex flex-col sm:flex-row items-center gap-6 sm:gap-8 pt-1">
          {/* Circular Score Gauge */}
          <div className="relative flex-shrink-0 w-36 h-36 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 150 150">
              <circle
                cx="75"
                cy="75"
                r={radius}
                stroke="#EFEBE4"
                strokeWidth={strokeWidth}
                fill="transparent"
              />
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

            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span className="font-serif text-3xl sm:text-4xl font-bold text-sage-900 leading-none">
                {displayScore}%
              </span>
              <span className="text-[11px] font-medium text-[#7E8B85] uppercase tracking-wider mt-1">
                Wellness Score
              </span>
            </div>
          </div>

          {/* Primary State & 2-Sentence Plain-Language Meaning */}
          <div className="space-y-3 text-center sm:text-left flex-1">
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${badgeStyle}`}>
                <Activity className="w-3.5 h-3.5 mr-1.5" />
                {displayState}
              </span>
              <span className="inline-flex items-center text-xs text-[#7E8B85]">
                <ShieldCheck className="w-3.5 h-3.5 mr-1 text-sage-600" />
                Non-Diagnostic Self-Reflection
              </span>
            </div>

            <div className="space-y-2 text-xs sm:text-sm text-[#4A5550] leading-relaxed">
              {displayExplanation.split('\n\n').slice(0, 2).map((paragraph, idx) => (
                <p key={idx}>{paragraph}</p>
              ))}
            </div>
          </div>
        </div>

        {/* Quiet non-medical notice */}
        <div className="p-3 rounded-xl bg-parchment-50 border border-parchment-200 text-xs text-[#6B7770] flex items-start space-x-2">
          <Info className="w-4 h-4 text-sage-600 flex-shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            {disclaimer || "This assessment reflects self-reported wellness tendencies. It is not a clinical diagnosis."}
          </p>
        </div>
      </section>

      {/* Safety / Crisis Support Notice (Displayed when elevated strain is detected) */}
      {is_high_distress && (
        <section aria-label="Support Guidance">
          <CrisisSupportNotice />
        </section>
      )}

      {/* 2. Indian Psychology Perspective: Triguna Profile & Chitta Vikṣepa */}
      <section className="space-y-5">
        <TrigunaChart
          sattvaScore={displaySattva}
          rajasScore={displayRajas}
          tamasScore={displayTamas}
          dominantPattern={displayDominant}
        />

        {/* Chitta Vikṣepa (Mental Stillness / Scattering) Status */}
        <div className="p-5 rounded-2xl bg-white border border-parchment-300/80 shadow-soft space-y-2 print-border-subtle print-break-inside-avoid">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-parchment-200 pb-2.5">
            <div className="flex items-center space-x-2">
              <Award className="w-4 h-4 text-sage-600" />
              <h3 className="font-serif text-base font-semibold text-sage-900">
                Mental Clarity &amp; Stillness (Chitta Vikṣepa)
              </h3>
            </div>
            <span className="self-start sm:self-auto text-xs font-semibold px-2.5 py-1 rounded-full bg-sage-50 text-sage-800 border border-sage-200">
              {displayVikshepa}
            </span>
          </div>

          <p className="text-xs sm:text-sm text-[#4A5550] leading-relaxed">
            In Patanjali's Yoga Sutras, <em>Chitta Vikṣepa</em> describes the natural tendency of attention to wander. {displayVikshepaDetails}
          </p>
        </div>
      </section>

      {/* 3. Main Contributing Factors */}
      {contributing_factors && contributing_factors.length > 0 && (
        <section className="bg-white rounded-2xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-4 print-border-subtle print-break-inside-avoid">
          <div className="border-b border-parchment-200 pb-3">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-sage-600 block">
              Self-Observation Highlights
            </span>
            <h3 className="font-serif text-lg sm:text-xl font-semibold text-sage-900">
              Contributing Factors
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {contributing_factors.map((factor, idx) => (
              <ContributingFactorCard key={idx} factor={factor} />
            ))}
          </div>
        </section>
      )}

      {/* 4. Personalized Wellness Practices (IKS Recommendations) */}
      {recommendations && recommendations.length > 0 && (
        <section className="bg-white rounded-2xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6 print-border-subtle">
          <div className="border-b border-parchment-200 pb-3">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-700 block">
              Holistic Lifestyle Suggestions
            </span>
            <h2 className="font-serif text-lg sm:text-xl font-semibold text-sage-900 flex items-center space-x-2">
              <Leaf className="w-5 h-5 text-emerald-700 inline" />
              <span>Personalized Wellness Practices</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {recommendations.map((rec, idx) => (
              <div
                key={idx}
                className="p-5 rounded-xl border border-sage-200/90 bg-sage-50/40 hover:bg-sage-50/70 transition-colors space-y-3 flex flex-col justify-between print-border-subtle print-break-inside-avoid"
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-sage-700 px-2 py-0.5 rounded bg-sage-100 border border-sage-200">
                      {rec.iks_concept}
                    </span>
                    <span className="text-[11px] font-mono text-[#7E8B85]">
                      #{idx + 1}
                    </span>
                  </div>

                  <h3 className="font-serif text-base font-semibold text-sage-900 leading-snug">
                    {rec.title}
                  </h3>

                  <p className="text-xs text-[#3C4742] leading-relaxed">
                    {rec.explanation}
                  </p>

                  <div className="p-3 rounded-lg bg-white/90 border border-parchment-200 text-xs space-y-1">
                    <strong className="text-sage-900 font-semibold block text-[11px] uppercase tracking-wider">
                      Why this was selected:
                    </strong>
                    <p className="text-[#4A5550] leading-relaxed">
                      {rec.why_it_may_help}
                    </p>
                  </div>
                </div>

                <div className="pt-2 border-t border-sage-200/60 flex items-center justify-between text-[11px] text-[#6B7770]">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-sage-600" />
                    <span>{rec.suggested_duration}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Calendar className="w-3.5 h-3.5 text-sage-600" />
                    <span>{rec.frequency}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 5. Academic Non-Medical Disclaimer Footer */}
      <footer className="bg-parchment-50 rounded-2xl p-6 border border-parchment-300/80 space-y-2.5 text-xs text-[#5C6863] print-border-subtle print-break-inside-avoid">
        <div className="flex items-center space-x-2 text-sage-900 font-semibold">
          <Sparkles className="w-4 h-4 text-sage-700 flex-shrink-0" />
          <span>Academic Mini-Project Scope</span>
        </div>
        <p className="leading-relaxed">
          Manas AI is an educational exploration of Indian Psychology (Sāṁkhya-Yoga) and machine-assisted wellness self-reflection. 
          It does not diagnose, treat, or provide medical advice for psychiatric or clinical conditions. 
          If you are seeking mental health support, please consult a qualified healthcare professional.
        </p>
        <div className="text-[11px] text-[#7E8B85] pt-1 border-t border-parchment-200">
          Session: <strong className="font-mono text-sage-800">{displayId}</strong> • Sāṁkhya-Yoga Framework
        </div>
      </footer>

      {/* 6. Main Action Controls (Hidden in Print) */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2 no-print">
        <button
          type="button"
          onClick={handlePrint}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-5 py-2.5 rounded-xl bg-white hover:bg-parchment-50 border border-parchment-300 text-sage-800 text-sm font-medium transition-colors cursor-pointer shadow-sm"
        >
          <Printer className="w-4 h-4 text-sage-600" />
          <span>Print / Save PDF</span>
        </button>

        <button
          type="button"
          onClick={onRetake}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-5 py-2.5 rounded-xl border border-sage-600 bg-white hover:bg-sage-50 text-sage-800 text-sm font-medium transition-colors cursor-pointer shadow-sm"
        >
          <RotateCcw className="w-4 h-4 text-sage-600" />
          <span>Retake Assessment</span>
        </button>

        <button
          type="button"
          onClick={onHome}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-2.5 rounded-xl bg-sage-700 hover:bg-sage-800 text-white text-sm font-medium transition-colors cursor-pointer shadow-sm"
        >
          <Home className="w-4 h-4" />
          <span>Return to Welcome</span>
        </button>
      </div>
    </div>
  );
}
