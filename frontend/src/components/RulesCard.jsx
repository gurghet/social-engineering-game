import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Shield } from 'lucide-react';

const RulesCard = ({ isVisible, onClose }) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-start sm:items-center justify-center p-2 sm:p-4 z-50 overflow-y-auto">
      <div className="max-w-2xl w-full my-4">
        <Card className="bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10 max-h-[90vh] flex flex-col">
          <CardHeader className="flex-shrink-0">
            <CardTitle className="text-emerald-400 flex justify-between items-center">
              <div>
                <Shield className="w-6 h-6 inline-block mr-2 align-text-top" />
                Game Rules
              </div>
              <button 
                onClick={onClose}
                className="text-gray-400 hover:text-emerald-400 transition-colors"
              >
                ✕
              </button>
            </CardTitle>
          </CardHeader>
          <CardContent className="overflow-y-auto">
            <div className="space-y-4">
              <p className="text-gray-300">
                Welcome to the Social Engineering Training Simulation! Your objective is to test the security awareness of the target by crafting emails that might reveal sensitive information.
              </p>
              <div className="bg-gray-800 p-4 rounded-lg border border-emerald-400/20">
                <h3 className="font-medium text-emerald-400 mb-2">How to Play:</h3>
                <ul className="list-disc list-inside space-y-2 text-sm text-gray-300">
                  <li>Craft emails to interact with the target using the Email Payload Constructor</li>
                  <li>Try to gather information or gain access to sensitive data</li>
                  <li>Be creative with your approach - direct password requests are likely to fail</li>
                  <li>Pay attention to the security checks and response feedback</li>
                  <li>Use the provided INTEL to guide your strategy</li>
                </ul>
              </div>
              <p className="text-sm text-gray-400">
                Remember: This is a training simulation. All interactions are with an AI system designed to help you understand social engineering techniques and improve security awareness.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default RulesCard;
