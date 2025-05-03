
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { MessageSquare, Link, Send } from 'lucide-react';
import { toast } from 'sonner';
import { ScamResult } from './ChatMessage';

interface ScamDetectorFormProps {
  onResultReceived: (result: ScamResult) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const ScamDetectorForm = ({ 
  onResultReceived, 
  isLoading, 
  setIsLoading 
}: ScamDetectorFormProps) => {
  const [activeTab, setActiveTab] = useState<string>('text');
  const [inputValue, setInputValue] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) {
      toast.error("Please enter some text or a URL");
      return;
    }

    setIsLoading(true);
    try {
      // Determine which endpoint to call based on active tab
      const isUrl = activeTab === 'url';
      const endpoint = isUrl 
        ? `http://localhost:8000/url/?url=${encodeURIComponent(inputValue.trim())}`
        : `http://localhost:8000/scam/?text=${encodeURIComponent(inputValue.trim())}`;

      const response = await fetch(endpoint);
      
      if (!response.ok) {
        throw new Error('Failed to fetch results');
      }

      const data = await response.json();
      
      // Create result object and pass it up
      const result: ScamResult = {
        inputText: inputValue.trim(),
        score: data.score,
        scam_indicators: data.scam_indicators,
        isUrl,
        timestamp: new Date()
      };
      
      onResultReceived(result);
      setInputValue('');
      
    } catch (error) {
      console.error('Error:', error);
      toast.error("Failed to check for scam. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mb-6 border-scamSensei-primary/20">
      <CardContent className="p-4">
        <form onSubmit={handleSubmit}>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-4 bg-scamSensei-light/50">
              <TabsTrigger 
                value="text" 
                className="flex items-center gap-2 data-[state=active]:bg-scamSensei-primary data-[state=active]:text-white"
              >
                <MessageSquare size={16} />
                <span>Text</span>
              </TabsTrigger>
              <TabsTrigger 
                value="url" 
                className="flex items-center gap-2 data-[state=active]:bg-scamSensei-primary data-[state=active]:text-white"
              >
                <Link size={16} />
                <span>URL</span>
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="text" className="mt-0">
              <Input
                placeholder="Enter WhatsApp message to check..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                className="mb-4 border-scamSensei-primary/20 focus-visible:ring-scamSensei-primary/30"
              />
            </TabsContent>
            
            <TabsContent value="url" className="mt-0">
              <Input
                placeholder="Enter URL to check..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                type="url"
                className="mb-4 border-scamSensei-primary/20 focus-visible:ring-scamSensei-primary/30"
              />
            </TabsContent>
          </Tabs>
          
          <Button 
            type="submit" 
            className="w-full bg-scamSensei-primary hover:bg-scamSensei-secondary text-white"
            disabled={isLoading}
          >
            {isLoading ? (
              <>Checking<span className="loading">...</span></>
            ) : (
              <>
                <Send size={16} className="mr-2" /> 
                Check for Scams
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ScamDetectorForm;
