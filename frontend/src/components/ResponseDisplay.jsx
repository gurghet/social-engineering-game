import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Mail } from 'lucide-react';

const ResponseDisplay = ({ response, success }) => {
  if (!response) return null;

  return (
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
            {typeof response === 'string' ? response : JSON.stringify(response, null, 2)}
          </p>
          <div className={`mt-4 p-2 rounded text-center font-bold ${success ? 'bg-emerald-400/20 text-emerald-400' : 'bg-red-400/20 text-red-400'}`}>
            {success ? 'FLAG OBTAINED!' : 'FAILED TO OBTAIN FLAG!'}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ResponseDisplay;
