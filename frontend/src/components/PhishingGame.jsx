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
  const [showRules, setShowRules] = useState(false);
  const [hasReadRules, setHasReadRules] = useState(() => {
    return localStorage.getItem('hasReadRules') === 'true';
  });
  
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    setIsDebugMode(urlParams.get('debug') === 'true');
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
    debugInfo: null
  });

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
        securityChecks: data.security_checks,
        debugInfo: data.debug_info
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

  const handleShowRules = () => {
    setShowRules(true);
    setHasReadRules(true);
    localStorage.setItem('hasReadRules', 'true');
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Help Button */}
        <div className="fixed top-4 right-4">
          <button
            onClick={handleShowRules}
            className="p-2 rounded-full bg-gray-800 hover:bg-gray-700 border border-emerald-400/20 text-emerald-400 transition-colors relative"
            title="Show Game Rules"
          >
            <HelpCircle className="w-6 h-6" />
            {!hasReadRules && (
              <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full transform translate-x-1 -translate-y-1"></span>
            )}
          </button>
        </div>

        {/* Rules Modal */}
        <RulesCard isVisible={showRules} onClose={() => setShowRules(false)} />

        {/* Game Components */}
        <GameHeader targetEmail={gameState.targetEmail} tips={gameState.tips} />
        
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
