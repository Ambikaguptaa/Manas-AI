import React from 'react';
import { Check } from 'lucide-react';

const SCALE_OPTIONS = [
  { value: 1, label: 'Never', description: 'Not experienced recently' },
  { value: 2, label: 'Rarely', description: 'Infrequently or once in a while' },
  { value: 3, label: 'Sometimes', description: 'Occasionally or moderate frequency' },
  { value: 4, label: 'Often', description: 'Frequent or noticeable pattern' },
  { value: 5, label: 'Almost Always', description: 'Very frequent or constant state' },
];

export default function QuestionCard({ question, selectedValue, onSelect }) {
  if (!question) return null;

  return (
    <div className="bg-white rounded-2xl p-6 sm:p-10 border border-parchment-300/80 shadow-soft space-y-8">
      {/* Question Prompt */}
      <div className="space-y-2">
        <h2 className="text-xl sm:text-2xl lg:text-[26px] font-serif font-semibold text-sage-900 leading-snug">
          {question.question}
        </h2>
        <p className="text-xs text-[#7E8B85]">
          Select the option that best reflects your recent experience.
        </p>
      </div>

      {/* 5-Point Response Scale */}
      <div className="space-y-3" role="radiogroup" aria-label={question.question}>
        {SCALE_OPTIONS.map((opt) => {
          const isSelected = selectedValue === opt.value;

          return (
            <button
              key={opt.value}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onSelect(opt.value)}
              className={`w-full flex items-center justify-between p-4 rounded-xl border text-left transition-all duration-150 cursor-pointer ${
                isSelected
                  ? 'border-sage-600 bg-sage-50/80 text-sage-900 ring-1 ring-sage-600 shadow-sm'
                  : 'border-parchment-200/90 hover:border-sage-300 bg-white hover:bg-parchment-50/60 text-[#3C4742]'
              }`}
            >
              <div className="flex items-center space-x-3.5">
                <span
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold transition-colors ${
                    isSelected
                      ? 'bg-sage-700 text-white'
                      : 'border border-parchment-300 text-[#6B7770] bg-parchment-50'
                  }`}
                >
                  {opt.value}
                </span>
                <div>
                  <span className="text-sm font-medium block text-sage-900">
                    {opt.label}
                  </span>
                  <span className="text-xs text-[#7E8B85] hidden sm:block mt-0.5">
                    {opt.description}
                  </span>
                </div>
              </div>

              {isSelected && (
                <div className="flex items-center justify-center w-5 h-5 rounded-full bg-sage-700 text-white flex-shrink-0">
                  <Check className="w-3 h-3 stroke-[2.5]" />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
