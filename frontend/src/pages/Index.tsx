
import React, { useState } from 'react';
import NavBar from '@/components/NavBar';
import ScamDetectorForm from '@/components/ScamDetectorForm';
import ChatMessage, { ScamResult } from '@/components/ChatMessage';
import Footer from '@/components/Footer';
import { ScrollArea } from '@/components/ui/scroll-area';

const Index = () => {
  const [results, setResults] = useState<ScamResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleNewResult = (result: ScamResult) => {
    setResults(prevResults => [result, ...prevResults]);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <NavBar />
      
      <main className="container mx-auto flex-1 p-4 max-w-2xl">
        <ScamDetectorForm 
          onResultReceived={handleNewResult} 
          isLoading={isLoading} 
          setIsLoading={setIsLoading}
        />
        
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2 text-scamSensei-teal">Scan Results</h2>
          
          {results.length === 0 ? (
            <div className="text-center py-10 text-gray-500 bg-white/50 rounded-lg border border-scamSensei-light">
              <p>No scans yet. Enter a message or URL to check.</p>
            </div>
          ) : (
            <ScrollArea className="h-[calc(100vh-300px)]">
              {results.map((result, index) => (
                <ChatMessage key={index} result={result} />
              ))}
            </ScrollArea>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
