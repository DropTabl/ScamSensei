
import React from 'react';

interface ScoreBarProps {
  score: number;
}

const ScoreBar = ({ score }: ScoreBarProps) => {
  // Calculate the width percentage based on score (0-10)
  const percentage = (score / 10) * 100;
  
  // Determine the color based on score
  const getColor = () => {
    if (score <= 3) return 'bg-safe';
    if (score <= 6) return 'bg-warning';
    return 'bg-danger';
  };
  
  // Get text description based on score
  const getText = () => {
    if (score <= 3) return 'Safe';
    if (score <= 6) return 'Suspicious';
    return 'Dangerous';
  };

  return (
    <div className="w-full mt-1">
      <div className="flex justify-between items-center mb-1 text-xs">
        <span className="font-medium">{getText()}</span>
        <span className="font-medium">{score}/10</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div 
          className={`h-2.5 rounded-full ${getColor()}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ScoreBar;
