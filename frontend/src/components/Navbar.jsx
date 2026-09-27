import React from 'react';
import { Feather } from 'lucide-react';

export default function Navbar({ onHome }) {
  return (
    <header className="border-b border-parchment-200/90 bg-[#FAF7F0]/90 backdrop-blur sticky top-0 z-40">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand & Project Identity */}
        <button
          type="button"
          onClick={onHome}
          className="flex items-center space-x-3 text-left group cursor-pointer focus:outline-none"
        >
          <div className="w-9 h-9 rounded-full bg-sage-50 border border-sage-200 flex items-center justify-center text-sage-700 transition-colors group-hover:bg-sage-100">
            <Feather className="w-4 h-4 text-sage-600" />
          </div>
          <div>
            <span className="text-lg font-serif font-semibold text-sage-900 leading-none block">
              Manas
            </span>
            <span className="text-[11px] text-[#6B7770] font-normal block mt-0.5">
              Wellness Assessment • Indian Psychology
            </span>
          </div>
        </button>

        {/* Quiet status tag */}
        <span className="text-[11px] text-[#7E8B85] px-2.5 py-1 rounded-full bg-parchment-200/60 border border-parchment-300/60">
          Academic IKS Project
        </span>
      </div>
    </header>
  );
}
