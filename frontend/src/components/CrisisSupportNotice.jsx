import React from 'react';
import { HeartHandshake, PhoneCall, ShieldAlert, UserCheck } from 'lucide-react';

export default function CrisisSupportNotice() {
  return (
    <div className="p-6 rounded-2xl bg-rose-50/70 border border-rose-200/90 space-y-4 print-border-subtle print-break-inside-avoid">
      <div className="flex items-start space-x-3">
        <div className="p-2 rounded-xl bg-rose-100 text-rose-700 flex-shrink-0 mt-0.5">
          <HeartHandshake className="w-5 h-5" />
        </div>
        <div className="space-y-1 flex-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-rose-700 block">
            Caring Support &amp; Guidance
          </span>
          <h3 className="font-serif text-base sm:text-lg font-semibold text-rose-900">
            Support is Available
          </h3>
          <p className="text-xs sm:text-sm text-rose-950/80 leading-relaxed">
            Your responses indicate that you may currently be experiencing noticeable mental strain, exhaustion, or emotional weight. 
            Please remember that you do not have to navigate difficult moments by yourself. We warmly encourage you to reach out 
            to a trusted friend, family member, or a qualified mental-health professional.
          </p>
        </div>
      </div>

      {/* Resource & Helpline Badges */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
        <div className="p-3 rounded-xl bg-white/90 border border-rose-200 flex items-start space-x-2.5 text-xs text-rose-900">
          <PhoneCall className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
          <div>
            <strong className="block font-semibold text-sage-900">Tele-MANAS (India 24/7)</strong>
            <span className="text-[11px] text-[#4A5550]">Toll-Free Govt Helpline: </span>
            <a href="tel:14416" className="font-mono font-bold text-rose-700 underline ml-1">
              14416 / 1800-891-4416
            </a>
          </div>
        </div>

        <div className="p-3 rounded-xl bg-white/90 border border-rose-200 flex items-start space-x-2.5 text-xs text-rose-900">
          <UserCheck className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
          <div>
            <strong className="block font-semibold text-sage-900">Consult a Professional</strong>
            <span className="text-[11px] text-[#4A5550]">
              Reach out to your university counselor, local clinic, or licensed psychologist.
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-2 text-[11px] text-rose-800/80 pt-1 border-t border-rose-200/60">
        <ShieldAlert className="w-3.5 h-3.5 flex-shrink-0" />
        <span>
          This assessment is an educational self-reflection project and cannot provide clinical diagnosis or emergency crisis response.
        </span>
      </div>
    </div>
  );
}
