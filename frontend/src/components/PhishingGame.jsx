import React, { useState, useEffect } from 'react';
import { HelpCircle } from 'lucide-react';
import RulesCard from './RulesCard';
import EmailComposer from './EmailComposer';
import ResponseDisplay from './ResponseDisplay';
import GameHeader from './GameHeader';
import DebugAnalysis from './DebugAnalysis';

const PhishingGame = () => {
  const [emailContent, setEmailContent] = useState({
    from: '',
    subject: '',
    body: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [isDebugMode, setIsDebugMode] = useState(false);
  useEffect(() => {
    console.log('isDebugMode state:', isDebugMode);
  }, [isDebugMode]);
  const [showRules, setShowRules] = useState(false);
  const [hasReadRules, setHasReadRules] = useState(() => {
    return localStorage.getItem('hasReadRules') === 'true';
  });
  
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const debugParam = urlParams.get('debug');
    console.log('Debug parameter:', debugParam);
    console.log('URL search:', window.location.search);
    setIsDebugMode(debugParam === 'true');
  }, []);
  
  const [gameState, setGameState] = useState({
    supervisorName: 'Mark Davidson',
    supervisorEmail: 'mark.davidson@whitecorp.com',
    targetEmail: 'janet.thompson@whitecorp.com',
    tips: [
      'Social engineering often involves creating a sense of urgency or authority',
      'Try gathering information before going for the password directly'
    ],
    lastResponse: null,
    success: false,
    securityChecks: null,
    debugInfo: null,
    objective: null
  });

  useEffect(() => {
    const fetchLevelInfo = async () => {
      try {
        const response = await fetch('/api/level/janet');
        if (response.ok) {
          const data = await response.json();
          setGameState(prev => ({
            ...prev,
            objective: data.objective
          }));
        }
      } catch (error) {
        console.error('Error fetching level info:', error);
      }
    };

    fetchLevelInfo();
  }, []);

  const sendEmail = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/send_email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: emailContent.from,
          subject: emailContent.subject,
          body: emailContent.body,
          target_email: gameState.targetEmail,
          debug: isDebugMode
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Response data:', data);  // Debug log
      
      setGameState(prev => ({
        ...prev,
        lastResponse: data.response,
        success: data.success,
        securityChecks: data.securityChecks,
        debugInfo: data.debugInfo
      }));
    } catch (error) {
      console.error('Error sending email:', error);
      setGameState(prev => ({
        ...prev,
        lastResponse: `Error: ${error.message}. Please try again.`,
      }));
    } finally {
      setIsLoading(false);
    }
  };

  const handleAcceptRules = () => {
    setHasReadRules(true);
    setShowRules(false);
    localStorage.setItem('hasReadRules', 'true');
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-300">
      {!hasReadRules && !showRules && (
        <div className="fixed bottom-4 right-4 z-50">
          <button
            onClick={() => setShowRules(true)}
            className="bg-emerald-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-emerald-600 transition-colors"
          >
            Read Game Rules
          </button>
        </div>
      )}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <RulesCard isVisible={showRules} onClose={handleAcceptRules} />
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-200">Social Engineering Challenge</h1>
          <button
            onClick={() => setShowRules(true)}
            className="flex items-center gap-2 text-emerald-400 hover:text-emerald-300"
          >
            <HelpCircle className="w-5 h-5" />
            Rules
          </button>
        </div>
        <GameHeader 
          targetEmail={gameState.targetEmail} 
          tips={gameState.tips}
          objective={gameState.objective}
        />
        
        <EmailComposer 
          emailContent={emailContent}
          setEmailContent={setEmailContent}
          isLoading={isLoading}
          sendEmail={sendEmail}
        />

        <ResponseDisplay 
          response={gameState.lastResponse}
          success={gameState.success}
        />

        {isDebugMode && (
          console.log('Debug props:', { securityChecks: gameState.securityChecks, debugInfo: gameState.debugInfo, lastResponse: gameState.lastResponse }),
          <DebugAnalysis 
            securityChecks={gameState.securityChecks}
            debugInfo={gameState.debugInfo}
            lastResponse={gameState.lastResponse}
          />
        )}
      </div>
    </div>
  );
};

export default PhishingGame;
