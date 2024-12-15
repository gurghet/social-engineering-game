import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Bug, CheckCircle, XCircle } from 'lucide-react';

const DebugAnalysis = ({ securityChecks, debugInfo, lastResponse }) => {
  if (!securityChecks) return null;

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
            {Object.entries(securityChecks || {}).map(([key, check]) => (
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
                  <code className="text-gray-300">{debugInfo?.email || 'No email sent yet'}</code>
                </pre>
              </div>
              <div>
                <h5 className="text-emerald-400 mb-2">AI Prompt</h5>
                <pre className="bg-gray-900 p-3 rounded overflow-auto max-h-48">
                  <code className="text-gray-300">{debugInfo?.system_prompt || 'No prompt generated yet'}</code>
                </pre>
              </div>
              <div>
                <h5 className="text-emerald-400 mb-2">Raw Response</h5>
                <pre className="bg-gray-900 p-3 rounded overflow-auto max-h-48">
                  <code className="text-gray-300">{lastResponse || 'No response yet'}</code>
                </pre>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default DebugAnalysis;
