import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import QuestionnairePage from './pages/QuestionnairePage';
import { checkHealth } from './services/api';

export default function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing' | 'questionnaire'
  const [systemStatus, setSystemStatus] = useState('checking');
  const [backendData, setBackendData] = useState(null);
  const [latency, setLatency] = useState(null);

  useEffect(() => {
    const verifyBackend = async () => {
      const startTime = performance.now();
      try {
        const data = await checkHealth();
        const endTime = performance.now();
        setLatency(Math.round(endTime - startTime));
        setBackendData(data);
        setSystemStatus('online');
      } catch (err) {
        console.error('Backend connection failed:', err);
        setSystemStatus('offline');
      }
    };

    verifyBackend();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#FAF7F0] text-[#2C3531]">
      <Navbar onHome={() => setCurrentView('landing')} />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {currentView === 'landing' ? (
          <LandingPage 
            onStartAssessment={() => setCurrentView('questionnaire')}
          />
        ) : (
          <QuestionnairePage
            onBackToHome={() => setCurrentView('landing')}
          />
        )}
      </main>

      <footer className="border-t border-parchment-300/80 bg-parchment-50 py-6 text-center text-xs text-[#6B7770]">
        <div className="max-w-5xl mx-auto px-4 space-y-1">
          <p className="font-medium text-sage-800">
            Manas AI — AI Mental Wellness System Using Indian Psychology
          </p>
          <p className="text-[11px] text-[#7E8B85]">
            Academic IKS Mini-Project • Strictly non-medical self-reflection tool
          </p>
        </div>
      </footer>
    </div>
  );
}
