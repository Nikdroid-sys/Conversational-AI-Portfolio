import { useState, useEffect } from 'react';
import './App.css';
import { useTTS } from './hooks/useTTS';
import MatrixRain from './components/MatrixRain';

function App() {
  const [botMessage, setBotMessage] = useState('');
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isIntro, setIsIntro] = useState(true);
  const [isTtsEnabled, setIsTtsEnabled] = useState(true);
  const { speak, cancel, isSpeaking } = useTTS();

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  // Speak the intro message on load
  useEffect(() => {
    const introText = "Welcome. I am KnowMI, your guide to wisdom. How may I illuminate your path?";
    setBotMessage(introText);
    if (isTtsEnabled) {
      // A slight delay to allow voices to load
      setTimeout(() => speak(introText), 500);
    }
  }, [isTtsEnabled]); // Reruns if TTS is toggled, which is acceptable here.

  const handleSendMessage = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    setIsIntro(false);
    setInput('');
    setIsLoading(true);
    setBotMessage(''); // Clear previous message

    // If TTS is speaking the intro, cancel it
    if (isSpeaking) {
      cancel();
    }

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: trimmedInput }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';
      
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        fullResponse += chunk;
        setBotMessage(fullResponse);
      }

      // Once streaming is complete, speak the full response
      if (isTtsEnabled) {
        speak(fullResponse);
      }

    } catch (error) {
      console.error('Error fetching response:', error);
      const errorMsg = "The connection to the ether has been lost. Please try again.";
      setBotMessage(errorMsg);
      if (isTtsEnabled) speak(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleTts = () => {
    setIsTtsEnabled(!isTtsEnabled);
    if (isSpeaking) {
      cancel();
    }
  };

  return (
    <div className="app-container">
      <MatrixRain />
      <header className="app-header">
        <h1 className="app-title">KnowMI.AI</h1>
        <div className="tts-toggle" onClick={toggleTts} title="Toggle Text-to-Speech">
          {isTtsEnabled ? '🔊' : '🔇'}
        </div>
      </header>
      
      <main className="main-content">

        <div className="caption-wrapper">
          <p className="caption-text">{botMessage || (isLoading ? '...' : '')}</p>
        </div>
      </main>

      <footer className="footer-content">
        <div className="chat-input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
            placeholder={isIntro ? "..." : "Continue the dialogue..."}
            disabled={isLoading}
          />
          <button onClick={handleSendMessage} disabled={isLoading}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;