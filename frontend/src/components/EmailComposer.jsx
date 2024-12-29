import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Mail, Loader2 } from 'lucide-react';

const EmailComposer = ({ emailContent, setEmailContent, isLoading, sendEmail }) => {
  const isFormValid = () => {
    return emailContent.from.trim() !== '' && 
           emailContent.subject.trim() !== '' && 
           emailContent.body.trim() !== '';
  };

  return (
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
              id="email-composer-from"
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
              id="email-composer-subject"
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
              id="email-composer-content"
              className="w-full p-2 rounded bg-gray-800 border border-emerald-400/20 text-gray-200 focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 h-32 placeholder-gray-500"
              value={emailContent.body}
              onChange={(e) => setEmailContent(prev => ({...prev, body: e.target.value}))}
              placeholder="Write your email content here..."
            />
          </div>
          <button
            id="email-composer-send-button"
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
  );
};

export default EmailComposer;
