import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';
import Icons from './components/Icons';
import Modal from './components/Modal';
import GithubIcon from './components/GithubIcon';
import LinkedinIcon from './components/LinkedinIcon';
import EmailIcon from './components/EmailIcon';
import SendIcon from './components/SendIcon';
import SettingsIcon from './components/SettingsIcon';
import AboutIcon from './components/AboutIcon';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
      const [fullBotMessage, setFullBotMessage] = useState(''); // Stores the complete message once received
      const [streamingBotMessage, setStreamingBotMessage] = useState(''); // The message being streamed character by character
      const [currentMessageIndex, setCurrentMessageIndex] = useState(-1); // Tracks the index of the message currently being streamed, -1 means no message is streaming.
      const [showSettings, setShowSettings] = useState(false);    const [showAbout, setShowAbout] = useState(false);
  
    const [geminiApiKey, setGeminiApiKey] = useState('');
    const [openaiApiKey, setOpenaiApiKey] = useState('');
    const [ollamaUrl, setOllamaUrl] = useState('');
    const [llmProvider, setLlmProvider] = useState('gemini');
  
    const handleSend = async () => {
      if (input.trim() === '') return;
  
      const userMessage = { text: input, sender: 'user' };
          // Optimistically add user's message and a placeholder for bot's message
          setMessages(prevMessages => {
            const newMessagesArray = [...prevMessages, userMessage, { text: '', sender: 'bot' }];
            setCurrentMessageIndex(newMessagesArray.length - 1); // Index of the new bot message
            return newMessagesArray;
          });
      
          setInput('');      setIsTyping(true);
    let requestBody = {
      query: input,
      llm_provider: llmProvider,
    };

    if (llmProvider === 'gemini') {
      requestBody.api_key = geminiApiKey;
    } else if (llmProvider === 'openai') {
      requestBody.api_key = openaiApiKey;
    } else if (llmProvider === 'ollama') {
      requestBody.ollama_base_url = ollamaUrl;
    }

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedBotMessage = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          setIsTyping(false);
          setFullBotMessage(accumulatedBotMessage); // Set the full message once streaming is done
          break;
        }
        accumulatedBotMessage += decoder.decode(value, { stream: true });
      }
    } catch (error) {
      console.error('Error fetching chat response:', error);
      setIsTyping(false);
    }
  };

  const handleSaveSettings = () => {
    localStorage.setItem('geminiApiKey', geminiApiKey);
    localStorage.setItem('openaiApiKey', openaiApiKey);
    localStorage.setItem('ollamaUrl', ollamaUrl);
    localStorage.setItem('llmProvider', llmProvider);
    setShowSettings(false);
  };

  useEffect(() => {
    const savedGeminiApiKey = localStorage.getItem('geminiApiKey');
    if (savedGeminiApiKey) {
      setGeminiApiKey(savedGeminiApiKey);
    }
    const savedOpenaiApiKey = localStorage.getItem('openaiApiKey');
    if (savedOpenaiApiKey) {
      setOpenaiApiKey(savedOpenaiApiKey);
    }
    const savedOllamaUrl = localStorage.getItem('ollamaUrl');
    if (savedOllamaUrl) {
      setOllamaUrl(savedOllamaUrl);
    }
    const savedLlmProvider = localStorage.getItem('llmProvider');
    if (savedLlmProvider) {
      setLlmProvider(savedLlmProvider);
    }
  }, []);

  useEffect(() => {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]); // Keep this useEffect for scroll

  useEffect(() => {
    if (fullBotMessage && currentMessageIndex !== -1) {
      let i = 0;
      const typingInterval = setInterval(() => {
        if (i < fullBotMessage.length) {
          setMessages(prevMessages => {
            const updatedMessages = [...prevMessages];
            updatedMessages[currentMessageIndex] = { ...updatedMessages[currentMessageIndex], text: fullBotMessage.substring(0, i + 1) };
            return updatedMessages;
          });
          i++;
        } else {
          clearInterval(typingInterval);
          setFullBotMessage(''); // Clear fullBotMessage after streaming
          setCurrentMessageIndex(-1); // Reset index
          setIsTyping(false); // Ensure isTyping is false after streaming completes
        }
      }, 25); // Adjust typing speed here (milliseconds per character)

      return () => clearInterval(typingInterval); // Cleanup on unmount or fullBotMessage change
    }
  }, [fullBotMessage, currentMessageIndex]);

  return (
    <div className="App">
      <Icons
        onSettingsClick={() => setShowSettings(true)}
        onAboutClick={() => setShowAbout(true)}
      />
      <main className="main-content">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h1>Namaste,</h1>
            <p>A clear view of Nikhil Chaube starts here.</p>
          </div>
        ) : (
          <div className="chat-container">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                {msg.sender === 'bot' ? (
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                ) : (
                  <p>{msg.text}</p>
                )}
              </div>
            ))}
            {isTyping && currentMessageIndex === -1 && ( // Show "Aditi is typing..." only when actively fetching a response, not during streaming
              <div className="chat-message bot">
                <p>Aditi is typing...</p>
              </div>
            )}
          </div>
        )}
      </main>
      <footer className="footer">
        <div className="input-bar">
          <input
            type="text"
            placeholder="Ask about Nikhil Chaube..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <div className="icon" onClick={handleSend}>
            <SendIcon />
          </div>
        </div>
      </footer>

      <Modal show={showSettings} onClose={() => setShowSettings(false)}>
        <h2>Settings</h2>
        <div className="settings-form">
          <label>LLM Provider</label>
          <select value={llmProvider} onChange={(e) => setLlmProvider(e.target.value)}>
            <option value="gemini">Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="ollama">Ollama</option>
          </select>

          {llmProvider === 'gemini' && (
            <>
              <label>Gemini API Key</label>
              <input
                type="text"
                value={geminiApiKey}
                onChange={(e) => setGeminiApiKey(e.target.value)}
              />
            </>
          )}

          {llmProvider === 'openai' && (
            <>
              <label>OpenAI API Key</label>
              <input
                type="text"
                value={openaiApiKey}
                onChange={(e) => setOpenaiApiKey(e.target.value)}
              />
            </>
          )}

          {llmProvider === 'ollama' && (
            <>
              <label>Ollama URL</label>
              <input
                type="text"
                value={ollamaUrl}
                onChange={(e) => setOllamaUrl(e.target.value)}
              />
            </>
          )}

          <button onClick={handleSaveSettings}>Save</button>
        </div>
      </Modal>

      <Modal show={showAbout} onClose={() => setShowAbout(false)}>
        <h2>About</h2>
        <p>This is a project by Nikhil Chaube.</p>
        <div className="social-icons">
          <a href="mailto:nikhilchaubey.ai@gmail.com">
            <EmailIcon />
          </a>
          <a href="https://www.linkedin.com/in/nikhil-chaubey-/" target="_blank" rel="noopener noreferrer">
            <LinkedinIcon />
          </a>
          <a href="https://github.com/n-chaubey" target="_blank" rel="noopener noreferrer">
            <GithubIcon />
          </a>
        </div>
      </Modal>
    </div>
  );
}

export default App;
