import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Terminal, AlertTriangle, Target } from 'lucide-react';

const GameHeader = ({ targetEmail, tips, objective }) => {
  return (
    <Card className="mb-6 bg-gray-900 border border-emerald-400/20 shadow-lg shadow-emerald-400/10">
      <CardHeader>
        <CardTitle className="text-emerald-400">
          <Terminal className="w-6 h-6 inline-block mr-2 align-text-top" />
          Social Engineering Training Simulation v1.0
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2 font-mono">
          <p><span className="text-emerald-400">[TARGET]</span> <span className="text-gray-200">{targetEmail}</span></p>
          {objective && (
            <p><span className="text-emerald-400">[OBJECTIVE]</span> <span className="text-gray-200">{objective}</span></p>
          )}
        </div>
        <div className="mt-4 bg-gray-800 p-4 rounded-lg border border-emerald-400/20">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-emerald-400" />
            <h3 className="font-medium text-emerald-400">INTEL</h3>
          </div>
          <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
            {tips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};

export default GameHeader;
