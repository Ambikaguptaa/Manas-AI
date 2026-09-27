import React from 'react';
import { ArrowRight, Compass, ShieldCheck, Heart, Sparkles } from 'lucide-react';
import DisclaimerBanner from '../components/DisclaimerBanner';

export default function LandingPage({ onStartAssessment }) {
  return (
    <div className="space-y-10 max-w-3xl mx-auto py-4 sm:py-8">
      {/* Gentle Non-Medical Notice */}
      <DisclaimerBanner />

      {/* Hero Welcome Card */}
      <section className="bg-white rounded-2xl p-8 sm:p-12 border border-parchment-200/90 shadow-soft text-center sm:text-left space-y-6">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sage-50 border border-sage-200 text-xs font-medium text-sage-700">
          <Sparkles className="w-3.5 h-3.5 text-sage-600" />
          <span>Indian Knowledge Systems • Wellness Reflection</span>
        </div>

        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-sage-900 leading-[1.15]">
          Understand your mental rhythm with Indian Psychology.
        </h1>

        <p className="text-base sm:text-lg text-[#4A5550] leading-relaxed max-w-2xl font-light">
          A gentle, 3-minute self-reflection designed to help you observe your current state of balance, mental activity, and stillness through classical concepts of <em>Triguna</em> and <em>Chitta</em>.
        </p>

        {/* Primary Call to Action */}
        <div className="pt-2 flex flex-col sm:flex-row items-center gap-4 justify-center sm:justify-start">
          <button
            type="button"
            onClick={onStartAssessment}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-8 py-3.5 rounded-xl bg-sage-700 hover:bg-sage-800 text-white font-medium text-base transition-colors shadow-sm cursor-pointer"
          >
            <span>Begin Assessment</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <span className="text-xs text-[#7E8B85]">
            16 simple questions • Approximately 3 minutes
          </span>
        </div>
      </section>

      {/* 3 Simple, Calm Highlights */}
      <section className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white p-6 rounded-2xl border border-parchment-200/80 shadow-soft space-y-2.5">
          <div className="w-9 h-9 rounded-lg bg-sage-50 border border-sage-200/70 flex items-center justify-center text-sage-700">
            <Compass className="w-4 h-4" />
          </div>
          <h3 className="font-serif text-base font-semibold text-sage-900">
            Triguna Perspective
          </h3>
          <p className="text-xs text-[#5C6863] leading-relaxed">
            Reflect on current tendencies of calmness (<em>Sattva</em>), mental activity (<em>Rajas</em>), and sluggishness (<em>Tamas</em>).
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-parchment-200/80 shadow-soft space-y-2.5">
          <div className="w-9 h-9 rounded-lg bg-sage-50 border border-sage-200/70 flex items-center justify-center text-sage-700">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <h3 className="font-serif text-base font-semibold text-sage-900">
            Non-Diagnostic &amp; Safe
          </h3>
          <p className="text-xs text-[#5C6863] leading-relaxed">
            An educational self-observation tool that never labels you with psychiatric or medical diagnoses.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-parchment-200/80 shadow-soft space-y-2.5">
          <div className="w-9 h-9 rounded-lg bg-sage-50 border border-sage-200/70 flex items-center justify-center text-sage-700">
            <Heart className="w-4 h-4" />
          </div>
          <h3 className="font-serif text-base font-semibold text-sage-900">
            Holistic Suggestions
          </h3>
          <p className="text-xs text-[#5C6863] leading-relaxed">
            Receive personalized, gentle daily practices—including soothing breathwork, routine harmony, and mindfulness.
          </p>
        </div>
      </section>
    </div>
  );
}
