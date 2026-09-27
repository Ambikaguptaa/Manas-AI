import React from 'react';
import { Info } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div className="bg-parchment-50 border border-parchment-300/80 p-3.5 sm:p-4 rounded-xl text-xs text-[#5C6863] leading-relaxed flex items-start space-x-2.5">
      <Info className="w-4 h-4 text-sage-600 flex-shrink-0 mt-0.5" />
      <div>
        <strong className="font-semibold text-sage-800">Academic Self-Reflection:</strong>{' '}
        This assessment is a wellness-oriented self-reflection tool grounded in traditional Indian Psychology. It is not a clinical psychiatric diagnosis or medical treatment.
      </div>
    </div>
  );
}
