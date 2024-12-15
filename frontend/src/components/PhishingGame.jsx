import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Mail, Shield, AlertTriangle, CheckCircle, XCircle, Terminal, Loader2, Bug } from 'lucide-react';

const PhishingGame = () => {
  const [emailContent, setEmailContent] = useState({
    from: '',
    subject: '',
    body: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [isDebugMode, setIsDebugMode] = useState(false);
  
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
          from_address: emailContent.from,
          subject: emailContent.subject,
          content: emailContent.body,
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

  const isFormValid = () => {
    return emailContent.from.trim() !== '' && 
           emailContent.subject.trim() !== '' && 
           emailContent.body.trim() !== '';
  };

  const renderSecurityChecks = () => {
    if (!isDebugMode || !gameState.securityChecks) return null;
    
    return (
      <Card className="mb-6 bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-emerald-400">
            <Bug className="w-6 h-6" />
            Debug Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-gray-800 p-4 rounded border border-emerald-400/20">
            <div className="space-y-4">
              {Object.entries(gameState.securityChecks || {}).map(([key, check]) => (
                <div key={key} className="flex items-start gap-3">
                  {check.passed ? 
                    <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" /> :
                    <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  }
                  <div className="flex-1">
                    <h4 className="font-medium text-emerald-400">{check.name || key}</h4>
                    <p className="text-sm text-gray-300">{check.description || ''}</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Status: <span className={check.passed ? "text-emerald-400" : "text-red-400"}>
                        {check.passed ? "Passed" : "Failed"}
                      </span>
                    </p>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Input and Processing Details */}
            <div className="mt-6 pt-6 border-t border-emerald-400/20">
              <h4 className="font-medium text-emerald-400 mb-3">Input and Processing Details</h4>
              <div className="space-y-6 font-mono text-sm">
                <div>
                  <h5 className="text-emerald-400 mb-2">Email Input</h5>
                  <pre className="bg-gray-900 p-3 rounded overflow-auto max-h-48">
                    <code className="text-gray-300">{gameState.debugInfo?.input?.email || 'No email sent yet'}</code>
                  </pre>
                </div>
                <div>
                  <h5 className="text-emerald-400 mb-2">AI Prompt</h5>
                  <pre className="bg-gray-900 p-3 rounded overflow-auto max-h-48">
                    <code className="text-gray-300">{gameState.debugInfo?.input?.prompt || 'No prompt generated yet'}</code>
                  </pre>
                </div>
                <div>
                  <h5 className="text-emerald-400 mb-2">Raw Response</h5>
                  <pre className="bg-gray-900 p-3 rounded overflow-auto max-h-48">
                    <code className="text-gray-300">{gameState.debugInfo?.raw_response || 'No response yet'}</code>
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Game Header */}
        <Card className="mb-6 bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10">
          <CardHeader>
            <CardTitle className="text-emerald-400">
              <Terminal className="w-6 h-6 inline-block mr-2 align-text-top" />
              Social Engineering Training Simulation v1.0
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-2 font-mono">
              <p><span className="text-emerald-400">[TARGET]</span> <span className="text-gray-200">{gameState.targetEmail}</span></p>
            </div>
            <div className="mt-4 bg-gray-800 p-4 rounded-lg border border-emerald-400/20">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="w-5 h-5 text-emerald-400" />
                <h3 className="font-medium text-emerald-400">INTEL</h3>
              </div>
              <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
                {gameState.tips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Email Composer */}
        <Card className="mb-6 bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-emerald-400">
              <Mail className="w-6 h-6" />
              Email Payload Constructor
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 font-mono">
              <div>
                <label className="block text-sm font-medium mb-1 text-emerald-400">FROM:</label>
                <input
                  type="search"
                  id="sender"
                  name="phishgame_sender_field"
                  autoComplete="off"
                  className="w-full p-2 rounded bg-gray-800 border border-emerald-400/20 text-gray-200 focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-gray-500"
                  value={emailContent.from}
                  onChange={(e) => setEmailContent(prev => ({ ...prev, from: e.target.value }))}
                  placeholder="your.email@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1 text-emerald-400">SUBJECT:</label>
                <input
                  type="search"
                  id="subject"
                  name="phishgame_subject_field"
                  autoComplete="off"
                  className="w-full p-2 rounded bg-gray-800 border border-emerald-400/20 text-gray-200 focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 placeholder-gray-500"
                  value={emailContent.subject}
                  onChange={(e) => setEmailContent(prev => ({ ...prev, subject: e.target.value }))}
                  placeholder="Email subject"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1 text-emerald-400">CONTENT:</label>
                <textarea
                  className="w-full p-2 rounded bg-gray-800 border border-emerald-400/20 text-gray-200 focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 h-32 placeholder-gray-500"
                  value={emailContent.body}
                  onChange={(e) => setEmailContent(prev => ({...prev, body: e.target.value}))}
                  placeholder="Write your email content here..."
                />
              </div>
              <button
                className="w-full bg-emerald-400/20 text-emerald-400 py-2 rounded hover:bg-emerald-400/30 transition-colors border border-emerald-400/40 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                onClick={sendEmail}
                disabled={isLoading || !isFormValid()}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    PLEASE WAIT...
                  </>
                ) : (
                  'SEND EMAIL'
                )}
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Response Display */}
        {gameState.lastResponse && (
          <Card className="mb-6 bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-emerald-400">
                <Mail className="w-6 h-6" />
                Target Response
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-800 p-4 rounded border border-emerald-400/20">
                <p className="whitespace-pre-wrap font-mono text-gray-300">
                  {typeof gameState.lastResponse === 'string' ? gameState.lastResponse : JSON.stringify(gameState.lastResponse, null, 2)}
                </p>
                <div className={`mt-4 p-2 rounded text-center font-bold ${gameState.success ? 'bg-emerald-400/20 text-emerald-400' : 'bg-red-400/20 text-red-400'}`}>
                  {gameState.success ? 'FLAG OBTAINED!' : 'FAILED TO OBTAIN FLAG!'}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Debug Analysis */}
        {renderSecurityChecks()}
      </div>
    </div>
  );
};

export default PhishingGame;
