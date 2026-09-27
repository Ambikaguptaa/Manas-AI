import React, { useState } from 'react';
import { 
  CheckCircle2, 
  RotateCcw, 
  Home, 
  Layers, 
  Activity, 
  Sparkles,
  ChevronDown,
  ChevronUp,
  Info,
  Compass,
  Feather,
  Flame,
  Moon,
  BookOpen,
  Brain,
  BarChart3,
  Clock,
  Calendar,
  Leaf
} from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';

export default function FeatureScoresDevView({ result, onRetake, onHome }) {
  const [showRaw, setShowRaw] = useState(false);
  const { 
    feature_scores, 
    overall_wellness_score, 
    overall_distress_score, 
    raw_responses,
    iks_interpretation,
    ml_prediction,
    recommendations
  } = result;

  const featuresList = [
    {
      key: 'restlessness_score',
      label: 'Mental Restlessness',
      val: feature_scores.restlessness_score,
      desc: 'Overthinking & internal restlessness (Negative direction)',
      type: 'negative',
    },
    {
      key: 'emotional_reactivity_score',
      label: 'Emotional Reactivity',
      val: feature_scores.emotional_reactivity_score,
      desc: 'Irritation & trigger sensitivity (Negative direction)',
      type: 'negative',
    },
    {
      key: 'overwhelm_score',
      label: 'Mental Overwhelm',
      val: feature_scores.overwhelm_score,
      desc: 'Pressure & mental load accumulation (Negative direction)',
      type: 'negative',
    },
    {
      key: 'energy_score',
      label: 'Energy & Vitality',
      val: feature_scores.energy_score,
      desc: 'Vitality vs. lethargy (Reverse scored from sluggishness)',
      type: 'positive',
    },
    {
      key: 'motivation_score',
      label: 'Motivation & Drive',
      val: feature_scores.motivation_score,
      desc: 'Enthusiasm for daily activities & goals',
      type: 'positive',
    },
    {
      key: 'concentration_score',
      label: 'Concentration & Focus',
      val: feature_scores.concentration_score,
      desc: 'Attention span & present-moment focus',
      type: 'positive',
    },
    {
      key: 'calmness_score',
      label: 'Calmness & Composure',
      val: feature_scores.calmness_score,
      desc: 'Inner peace & emotional composure (Samatvam)',
      type: 'positive',
    },
    {
      key: 'routine_score',
      label: 'Sleep & Routine Discipline',
      val: feature_scores.routine_score,
      desc: 'Sleep schedule & daily habit regularity (Dinacharya)',
      type: 'positive',
    },
    {
      key: 'mental_clarity_score',
      label: 'Mental Clarity & Awareness',
      val: feature_scores.mental_clarity_score,
      desc: 'Orderly thinking & self-observation (Sakshi Bhava)',
      type: 'positive',
    },
  ];

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <DisclaimerBanner />

      {/* Header Notice */}
      <section className="bg-white rounded-xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-4">
        <div className="flex items-center space-x-2 text-emerald-700">
          <CheckCircle2 className="w-5 h-5" />
          <span className="text-xs font-semibold uppercase tracking-wider">
            Stage 5: Curated IKS Recommendations Active
          </span>
        </div>

        <h1 className="text-2xl sm:text-3xl font-serif font-bold text-sage-800">
          Mental Wellness Assessment &amp; IKS Roadmap
        </h1>

        <p className="text-sm text-[#4A5550] leading-relaxed">
          Your questionnaire responses have been converted into psychological features, evaluated by our 
          <strong> Random Forest Classifier (Stage 4)</strong>, and interpreted through <strong>Indian Psychology (IKS)</strong> frameworks to generate personalized, non-medical lifestyle practices.
        </p>

        {/* Academic Disclaimer Note */}
        <div className="p-3.5 rounded-lg bg-amber-50/70 border border-amber-200 text-xs text-amber-900 flex items-start space-x-2.5">
          <Info className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
          <span>
            <strong>Academic Self-Reflection:</strong> These suggestions are gentle lifestyle and self-reflection practices from traditional Indian Knowledge Systems. They do NOT replace professional medical or psychological therapy.
          </span>
        </div>
      </section>

      {/* Actionable IKS Wellness Recommendations (Stage 5) */}
      {recommendations && recommendations.length > 0 && (
        <section className="bg-white rounded-xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-parchment-200 pb-4 gap-2">
            <div className="flex items-center space-x-2">
              <Leaf className="w-5 h-5 text-emerald-700" />
              <h2 className="font-serif text-lg font-semibold text-sage-800">
                Personalized IKS Wellness Recommendations
              </h2>
            </div>
            <span className="text-xs text-[#6B7770]">
              {recommendations.length} Prioritized Practices
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, idx) => (
              <div 
                key={idx}
                className="p-5 rounded-xl border border-sage-200 bg-sage-50/40 hover:bg-sage-50/70 transition-colors space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-sage-700 px-2 py-0.5 rounded bg-sage-100 border border-sage-200">
                      {rec.iks_concept}
                    </span>
                    <span className="text-[11px] font-mono text-[#7E8B85]">
                      Step {idx + 1}
                    </span>
                  </div>

                  <h3 className="font-serif text-base font-semibold text-sage-900">
                    {rec.title}
                  </h3>

                  <p className="text-xs text-[#3C4742] leading-relaxed">
                    {rec.explanation}
                  </p>

                  <div className="p-2.5 rounded-lg bg-white/80 border border-parchment-200 text-xs text-[#5C6863] leading-snug">
                    <strong className="text-sage-800 block mb-0.5">Why it may help:</strong>
                    {rec.why_it_may_help}
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

      {/* Machine Learning Classification Result Card (Stage 4) */}
      {ml_prediction && (
        <section className="bg-white rounded-xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-parchment-200 pb-4 gap-2">
            <div className="flex items-center space-x-2">
              <Brain className="w-5 h-5 text-ochre-600" />
              <h2 className="font-serif text-lg font-semibold text-sage-800">
                Machine Learning Prediction (Random Forest)
              </h2>
            </div>
            <span className="text-xs font-mono font-medium px-2.5 py-1 rounded bg-parchment-100 text-sage-800 border border-parchment-300">
              Model: {ml_prediction.model_type}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Primary Classification */}
            <div className="p-5 rounded-xl border border-ochre-200 bg-ochre-50/40 space-y-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-ochre-700 block">
                Predicted Wellness State
              </span>
              <div className="flex items-baseline space-x-2">
                <span className="text-2xl font-serif font-bold text-sage-800">
                  {ml_prediction.predicted_label}
                </span>
                <span className="text-xs font-mono text-[#7E8B85]">
                  (Class {ml_prediction.predicted_class})
                </span>
              </div>
              <p className="text-xs text-[#5C6863]">
                Model Confidence: <strong className="text-sage-800 font-mono">{(ml_prediction.confidence * 100).toFixed(1)}%</strong>
              </p>
            </div>

            {/* Probability Distribution */}
            <div className="p-5 rounded-xl border border-parchment-200 bg-parchment-50/60 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-sage-700">
                  Class Probabilities
                </span>
                <BarChart3 className="w-3.5 h-3.5 text-sage-600" />
              </div>

              <div className="space-y-1.5 pt-1">
                {Object.entries(ml_prediction.class_probabilities).map(([label, prob]) => {
                  const isPredicted = label === ml_prediction.predicted_label;
                  const pct = (prob * 100).toFixed(1);

                  return (
                    <div key={label} className="text-xs space-y-0.5">
                      <div className="flex justify-between text-[11px]">
                        <span className={isPredicted ? 'font-semibold text-sage-900' : 'text-[#6B7770]'}>
                          {label}
                        </span>
                        <span className="font-mono text-[#5C6863]">{pct}%</span>
                      </div>
                      <div className="w-full bg-parchment-200 h-1.5 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            isPredicted ? 'bg-ochre-600' : 'bg-parchment-400'
                          }`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          <p className="text-[11px] text-[#7E8B85] italic">
            * {ml_prediction.disclaimer}
          </p>
        </section>
      )}

      {/* IKS Interpretation Highlights (Stage 3 Module) */}
      {iks_interpretation && (
        <section className="bg-white rounded-xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-parchment-200 pb-4 gap-2">
            <div className="flex items-center space-x-2">
              <Compass className="w-5 h-5 text-sage-600" />
              <h2 className="font-serif text-lg font-semibold text-sage-800">
                Indian Psychology Interpretation
              </h2>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-medium px-2.5 py-1 rounded bg-sage-100 text-sage-800 border border-sage-200">
                {iks_interpretation.overall_wellness_state}
              </span>
              <span className="text-xs font-medium px-2.5 py-1 rounded bg-ochre-100 text-ochre-800 border border-ochre-200">
                {iks_interpretation.dominant_pattern}
              </span>
            </div>
          </div>

          {/* Triguna Tendency Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Sattva */}
            <div className="p-4 rounded-xl border border-sattva-border bg-sattva-light/40 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1.5 text-sattva">
                  <Feather className="w-4 h-4" />
                  <span className="font-serif text-sm font-semibold">Sattva (सत्त्व)</span>
                </div>
                <span className="font-mono text-sm font-bold text-sattva">
                  {iks_interpretation.sattva_score}%
                </span>
              </div>
              <div className="w-full bg-sattva-border/40 h-2 rounded-full overflow-hidden">
                <div 
                  className="bg-sattva h-full rounded-full"
                  style={{ width: `${iks_interpretation.sattva_score}%` }}
                />
              </div>
              <p className="text-[11px] text-[#4A5550]">
                Clarity, serenity, equilibrium, and lightness of mind.
              </p>
            </div>

            {/* Rajas */}
            <div className="p-4 rounded-xl border border-rajas-border bg-rajas-light/40 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1.5 text-rajas">
                  <Flame className="w-4 h-4" />
                  <span className="font-serif text-sm font-semibold">Rajas (रजस्)</span>
                </div>
                <span className="font-mono text-sm font-bold text-rajas">
                  {iks_interpretation.rajas_score}%
                </span>
              </div>
              <div className="w-full bg-rajas-border/50 h-2 rounded-full overflow-hidden">
                <div 
                  className="bg-rajas h-full rounded-full"
                  style={{ width: `${iks_interpretation.rajas_score}%` }}
                />
              </div>
              <p className="text-[11px] text-[#4A5550]">
                Restlessness, high mental motion, passion, and emotional drive.
              </p>
            </div>

            {/* Tamas */}
            <div className="p-4 rounded-xl border border-tamas-border bg-tamas-light/40 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1.5 text-tamas">
                  <Moon className="w-4 h-4" />
                  <span className="font-serif text-sm font-semibold">Tamas (तमस्)</span>
                </div>
                <span className="font-mono text-sm font-bold text-tamas">
                  {iks_interpretation.tamas_score}%
                </span>
              </div>
              <div className="w-full bg-tamas-border/50 h-2 rounded-full overflow-hidden">
                <div 
                  className="bg-tamas h-full rounded-full"
                  style={{ width: `${iks_interpretation.tamas_score}%` }}
                />
              </div>
              <p className="text-[11px] text-[#4A5550]">
                Inertia, fatigue, heaviness, and routine irregularity.
              </p>
            </div>
          </div>

          {/* Chitta Vikṣepa Indicator Card */}
          <div className="p-4 rounded-xl bg-parchment-50 border border-parchment-300 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-sage-800">
                Chitta Vikṣepa (Mental Distraction / Scattering Indicator)
              </span>
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-white border border-parchment-300 text-sage-800">
                {iks_interpretation.chitta_vikshepa_indicator}
              </span>
            </div>
            <p className="text-xs text-[#5C6863] leading-relaxed">
              {iks_interpretation.chitta_vikshepa_details}
            </p>
          </div>

          {/* Accessible Narrative Explanation */}
          <div className="space-y-3 pt-2">
            <h3 className="font-serif text-sm font-semibold text-sage-800">
              Reflective Narrative &amp; Suggestions
            </h3>
            <div className="text-xs sm:text-sm text-[#4A5550] leading-relaxed space-y-3 bg-parchment-50/60 p-4 sm:p-5 rounded-xl border border-parchment-200">
              {iks_interpretation.explanation.split('\n\n').map((para, idx) => (
                <p key={idx}>{para}</p>
              ))}
            </div>
          </div>

          {/* Classical Grounding Note */}
          <div className="flex items-start space-x-2 text-[11px] text-[#6B7770] italic pt-1 border-t border-parchment-200">
            <BookOpen className="w-4 h-4 flex-shrink-0 mt-0.5 text-sage-600" />
            <span>{iks_interpretation.philosophical_context}</span>
          </div>
        </section>
      )}

      {/* Overall Composite Indices */}
      <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-white p-6 rounded-xl border border-parchment-300/80 shadow-soft space-y-2">
          <span className="text-xs font-medium uppercase tracking-wider text-sage-600 block">
            Composite Wellness Index
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-bold font-serif text-sage-800">
              {overall_wellness_score}%
            </span>
            <span className="text-xs text-[#6B7770]">positive wellness orientation</span>
          </div>
          <div className="w-full bg-parchment-200 h-2 rounded-full overflow-hidden mt-2">
            <div 
              className="bg-emerald-600 h-full rounded-full" 
              style={{ width: `${overall_wellness_score}%` }} 
            />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-parchment-300/80 shadow-soft space-y-2">
          <span className="text-xs font-medium uppercase tracking-wider text-ochre-600 block">
            Composite Distress Index
          </span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-bold font-serif text-ochre-700">
              {overall_distress_score}%
            </span>
            <span className="text-xs text-[#6B7770]">restlessness / overload indicators</span>
          </div>
          <div className="w-full bg-parchment-200 h-2 rounded-full overflow-hidden mt-2">
            <div 
              className="bg-ochre-500 h-full rounded-full" 
              style={{ width: `${overall_distress_score}%` }} 
            />
          </div>
        </div>
      </section>

      {/* 9 Standardized Feature Scores Breakdown */}
      <section className="bg-white rounded-xl p-6 sm:p-8 border border-parchment-300/80 shadow-soft space-y-6">
        <div className="flex items-center justify-between border-b border-parchment-200 pb-3">
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-sage-600" />
            <h2 className="font-serif text-base font-semibold text-sage-800">
              Internal Psychological Feature Vector (Scale: 1.0 – 5.0)
            </h2>
          </div>
          <span className="text-xs text-[#7E8B85]">
            9 Core Psychological Features
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {featuresList.map((f) => {
            const pct = Math.round(((f.val - 1.0) / 4.0) * 100);

            return (
              <div 
                key={f.key}
                className="bg-parchment-50 p-4 rounded-lg border border-parchment-200 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-sage-800">
                    {f.label}
                  </span>
                  <span className="font-mono text-sm font-bold text-sage-900 bg-white px-2 py-0.5 rounded border border-parchment-300">
                    {f.val.toFixed(2)}
                  </span>
                </div>

                <div className="w-full bg-parchment-200 h-1.5 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${
                      f.type === 'positive' ? 'bg-sage-600' : 'bg-ochre-500'
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>

                <p className="text-[11px] text-[#6B7770] leading-snug">
                  {f.desc}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Raw Response Inspector (Collapsible) */}
      <section className="bg-white rounded-xl border border-parchment-300/80 shadow-soft overflow-hidden">
        <button
          type="button"
          onClick={() => setShowRaw(!showRaw)}
          className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-parchment-50 transition-colors cursor-pointer"
        >
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-sage-600" />
            <span className="text-xs font-semibold uppercase tracking-wider text-sage-800">
              Inspect Raw Responses (16 Items)
            </span>
          </div>
          {showRaw ? <ChevronUp className="w-4 h-4 text-sage-600" /> : <ChevronDown className="w-4 h-4 text-sage-600" />}
        </button>

        {showRaw && (
          <div className="px-6 pb-6 pt-2 border-t border-parchment-200 bg-parchment-50/50">
            <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-8 gap-2 pt-2">
              {Object.entries(raw_responses).map(([qid, val]) => (
                <div key={qid} className="p-2 bg-white rounded border border-parchment-300 text-center">
                  <span className="block text-[10px] text-[#7E8B85] uppercase">Q{qid}</span>
                  <span className="font-mono text-sm font-bold text-sage-800">{val}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
        <button
          type="button"
          onClick={onRetake}
          className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-lg border border-sage-600 bg-white hover:bg-sage-50 text-sage-800 font-medium text-sm transition-colors cursor-pointer"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Retake Assessment</span>
        </button>

        <button
          type="button"
          onClick={onHome}
          className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-lg bg-sage-700 hover:bg-sage-800 text-white font-medium text-sm transition-colors cursor-pointer shadow-sm"
        >
          <Home className="w-4 h-4" />
          <span>Back to Landing Page</span>
        </button>
      </div>
    </div>
  );
}
