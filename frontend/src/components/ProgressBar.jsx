import React from 'react';

export default function ProgressBar({ current, total }) {
  const percentage = Math.round((current / total) * 100);

  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between text-xs text-[#5C6863]">
        <span className="font-medium text-sage-800">
          Question <strong className="text-sage-900 font-semibold">{current}</strong> of {total}
        </span>
        <span className="text-[#7E8B85] font-medium">
          {percentage}% completed
        </span>
      </div>

      <div className="w-full h-2 bg-parchment-200 rounded-full overflow-hidden">
        <div
          className="h-full bg-sage-600 transition-all duration-300 ease-out rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
