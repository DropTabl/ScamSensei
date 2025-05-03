
import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import ScoreBar from './ScoreBar';
import { MessageSquare, Link } from 'lucide-react';
import { Badge } from "@/components/ui/badge";

export interface ScamResult {
  inputText: string;
  score: number;
  scam_indicators: string[];
  isUrl: boolean;
  timestamp: Date;
}

const ChatMessage = ({ result }: { result: ScamResult }) => {
  return (
    <Card className="mb-4 border-none shadow-sm bg-scamSensei-light/50 rounded-lg">
      <CardContent className="pt-4">
        <div className="flex items-start gap-3">
          <div className="p-2 bg-scamSensei-primary text-white rounded-full">
            {result.isUrl ? <Link size={16} /> : <MessageSquare size={16} />}
          </div>
          <div className="flex-1">
            <div className="mb-2">
              <p className="break-all mb-1 font-medium text-sm">{result.inputText}</p>
              <p className="text-xs text-gray-600">
                {result.timestamp.toLocaleTimeString()} • {result.isUrl ? 'URL' : 'Text'} scan
              </p>
            </div>
            
            <ScoreBar score={result.score} />
            
            {result.scam_indicators.length > 0 && (
              <div className="mt-3">
                <p className="text-xs text-gray-600 mb-1">Scam indicators:</p>
                <div className="flex flex-wrap gap-1">
                  {result.scam_indicators.map((indicator, index) => (
                    <Badge key={index} variant="outline" className="text-xs bg-white/80 border-scamSensei-primary/20">
                      {indicator}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ChatMessage;
