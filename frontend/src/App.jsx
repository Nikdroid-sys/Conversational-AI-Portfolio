import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';
import Icons from './components/Icons';
import Modal from './components/Modal';
import aditiIcon from '/aditi.svg';
import GithubIcon from './components/GithubIcon';
import LinkedinIcon from './components/LinkedinIcon';
import EmailIcon from './components/EmailIcon';
import SendIcon from './components/SendIcon';
import SettingsIcon from './components/SettingsIcon';
import AboutIcon from './components/AboutIcon';
import ErrorIcon from './components/ErrorIcon';
import HomeIcon from './components/HomeIcon';
import ContactModal from './components/ContactModal';
import UAParser from 'ua-parser-js';

// Define a custom renderer for links
//Deployment trigger

const LinkRenderer = ({ href, children }) => (

  <a href={href} target="_blank" rel="noopener noreferrer" className="citation-link">

    {children}

  </a>

);



function App() {

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState('');

  const [isTyping, setIsTyping] = useState(false);

  const [fullBotMessage, setFullBotMessage] = useState('');

  const [currentMessageIndex, setCurrentMessageIndex] = useState(-1); // Tracks the index of the message currently being streamed, -1 means no message is streaming.

  const [showSettings, setShowSettings] = useState(false);

  const [showAbout, setShowAbout] = useState(false);

    const [showContactModal, setShowContactModal] = useState(false);

    const [contactModalShown, setContactModalShown] = useState(false);

    const [pendingLog, setPendingLog] = useState(null);

    const [contactInfo, setContactInfo] = useState(null);

  const [geminiApiKey, setGeminiApiKey] = useState('');
  const [ollamaUrl, setOllamaUrl] = useState('');
  const [ollamaModel, setOllamaModel] = useState('');
  const [llmProvider, setLlmProvider] = useState('gemini');
  const [geminiModel, setGeminiModel] = useState('gemini-2.5-flash-lite');
  const [latency, setLatency] = useState(0);
  const [sessionId, setSessionId] = useState('');

  const handleContactSubmit = (contactData) => {
    setContactInfo(contactData);
    setShowContactModal(false);
    if (pendingLog) {
      sendDataToGoogleSheet(pendingLog.question, pendingLog.answer, pendingLog.latency, contactData);
      setPendingLog(null);
    }
    // We can optionally send the data again here, but it's better to wait for the next message
  };

  const handleContactModalClose = () => {
    setShowContactModal(false);
    if (pendingLog) {
      sendDataToGoogleSheet(pendingLog.question, pendingLog.answer, pendingLog.latency);
      setPendingLog(null);
    }
  };

  const handleSend = async () => {
    if (input.trim() === '') return;

    if (pendingLog) {
      sendDataToGoogleSheet(pendingLog.question, pendingLog.answer, pendingLog.latency);
      setPendingLog(null);
    }

    const isFirstMessage = messages.length === 0;

    if (isFirstMessage && !contactModalShown) {
      setShowContactModal(true);
      setContactModalShown(true);
    }

    proceedWithApiCall(input, isFirstMessage);
    setInput('');
  };

  const proceedWithApiCall = async (question, isFirstMessage) => {
    if (question.trim() === '') return;
    const userMessage = { text: question, sender: 'user' };
    let botMessageIndex;
    // Optimistically add user's message and a placeholder for bot's message
    setMessages(prevMessages => {
      const newMessagesArray = [...prevMessages, userMessage, { text: 'Aditi is typing', sender: 'bot', isTyping: true }];
      botMessageIndex = newMessagesArray.length - 1;
      setCurrentMessageIndex(botMessageIndex); // Index of the new bot message
      return newMessagesArray;
    });

    // setIsTyping is no longer the primary driver of the "typing" message, but we can keep it for other potential uses.
    setIsTyping(true);
    let requestBody = {
      query: question,
      llm_provider: llmProvider,
    };

    if (llmProvider === 'gemini') {
      requestBody.api_key = geminiApiKey;
      requestBody.llm_model = geminiModel;
    } else if (llmProvider === 'ollama') {
      requestBody.ollama_base_url = ollamaUrl;
      requestBody.ollama_model = ollamaModel;
    }

    const startTime = Date.now();

    try {
      // Use the environment variable injected by GitHub Actions, 
      // or fall back to localhost for your local development.
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

      if (import.meta.env.DEV) {
        console.log('Aditi is in Dev Mode. Connecting to:', API_BASE_URL);
      }

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'An error occurred on the server.');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedBotMessage = '';
      let firstChunk = true;

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          const endTime = Date.now();
          const latencyInSeconds = (endTime - startTime) / 1000;
          setLatency(latencyInSeconds);

          setMessages(prev => {
            const newMessages = [...prev];
            if (newMessages[botMessageIndex]) {
              newMessages[botMessageIndex] = { ...newMessages[botMessageIndex], isTyping: false };
            }
            return newMessages;
          });

          setFullBotMessage(accumulatedBotMessage);
          if (isFirstMessage) {
            setPendingLog({ question, answer: accumulatedBotMessage, latency: latencyInSeconds });
          } else {
            sendDataToGoogleSheet(question, accumulatedBotMessage, latencyInSeconds);
          }


          setIsTyping(false);
          setCurrentMessageIndex(-1);
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        accumulatedBotMessage += chunk;
      }
    } catch (error) {
      console.error('Error fetching chat response:', error);
      setIsTyping(false);

      let userFacingErrorMessage;

      // Prioritize specific backend error messages
      if (error.message && error.message.includes('API rate limit exceeded')) {
        userFacingErrorMessage = "It seems I've been a bit too chatty! My connection to the language model is taking a short rest. You can wait a moment and try again, or feel free to provide your own API key in the settings.";
      } else if (error.message && error.message.includes('API key not valid')) {
        userFacingErrorMessage = "The API key you've provided doesn't seem to be quite right. Could you please double-check it for me in the settings?";
      } else if (error.message && error.message.includes('The default API key is missing')) {
        userFacingErrorMessage = "It looks like a default API key is not set up. To chat, could you please provide your own in the settings?";
      } else if (error instanceof TypeError) { // General network-level errors
        userFacingErrorMessage = "I'm experiencing a network error. This might be due to a rate limit on the default API key or a problem with the connection. Please try setting up your own API key using the settings icon. If the issue persists, please check your internet connection.";
      } else {
        // For other errors, use the message if available, otherwise a generic fallback
        userFacingErrorMessage = error.message || "I've encountered a little hiccup. I'd appreciate it if you could try your request again.";
      }

      setMessages(prevMessages => {
        // Replace the "Aditi is typing..." message or append if not present
        const updatedMessages = [...prevMessages];
        const lastMessageIndex = updatedMessages.length - 1;

        // Check if the last message is a bot message placeholder
        if (lastMessageIndex >= 0 && updatedMessages[lastMessageIndex].sender === 'bot' && updatedMessages[lastMessageIndex].isTyping) {
          updatedMessages[lastMessageIndex] = { text: userFacingErrorMessage, sender: 'bot', isError: true, isTyping: false };
        } else {
          // Otherwise, just append the error message
          updatedMessages.push({ text: userFacingErrorMessage, sender: 'bot', isError: true, isTyping: false });
        }
        return updatedMessages;
      });
    }
  };

  const sendDataToGoogleSheet = async (question, answer, latency, submittedContactInfo) => {
    const parser = new UAParser();
    const result = parser.getResult();
    const device = result.device.type || 'desktop';
    const browser = result.browser.name;
    const finalContactInfo = submittedContactInfo || contactInfo;

    const data = {
      timestamp: new Date().toISOString(),
      sessionId,
      name: finalContactInfo?.name || '',
      llmModel: llmProvider === 'gemini' ? geminiModel : ollamaModel,
      apiKey: llmProvider === 'gemini' ? geminiApiKey : '',
      geminiQuestion: question,
      geminiAnswer: answer,
      device,
      browser,
      latency: latency.toFixed(2),
      contact: finalContactInfo?.contact || '',
    };

    try {
      // IMPORTANT: Replace with your actual Google Apps Script Web App URL
      const sheetUrl = import.meta.env.VITE_GOOGLE_SCRIPT_URL;

      await fetch(sheetUrl, {
        method: 'POST',
        mode: 'no-cors', // Important for sending to Google Apps Script from a different origin
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
    } catch (error) {
      console.error('Error sending data to Google Sheet:', error);
    }
  };


  const handleHomeClick = () => {
    setMessages([]);
  };


  const handleCloseSettings = () => {
    const savedGeminiApiKey = localStorage.getItem('geminiApiKey') || '';
    setGeminiApiKey(savedGeminiApiKey);

    const savedOllamaUrl = localStorage.getItem('ollamaUrl') || '';
    setOllamaUrl(savedOllamaUrl);

    const savedOllamaModel = localStorage.getItem('ollamaModel') || '';
    setOllamaModel(savedOllamaModel);

    const savedLlmProvider = localStorage.getItem('llmProvider') || 'gemini';
    setLlmProvider(savedLlmProvider);

    const savedGeminiModel = localStorage.getItem('geminiModel') || 'gemini-2.5-flash-lite';
    setGeminiModel(savedGeminiModel);

    setShowSettings(false);
  };

  const handleSaveSettings = () => {
    localStorage.setItem('geminiApiKey', geminiApiKey);
    localStorage.setItem('ollamaUrl', ollamaUrl);
    localStorage.setItem('ollamaModel', ollamaModel);
    localStorage.setItem('llmProvider', llmProvider);
    localStorage.setItem('geminiModel', geminiModel);
    setShowSettings(false);
  };

  const handleResetSettings = () => {
    localStorage.removeItem('geminiApiKey');
    localStorage.removeItem('ollamaUrl');
    localStorage.removeItem('ollamaModel');
    localStorage.removeItem('llmProvider');
    localStorage.removeItem('geminiModel');

    setGeminiApiKey('');
    setOllamaUrl('');
    setOllamaModel('');
    setLlmProvider('gemini'); // Reset to default provider
    setGeminiModel('gemini-2.5-flash-lite');

    setShowSettings(false);
  };

  useEffect(() => {
    setSessionId('session-' + Date.now());
  }, []);

  useEffect(() => {
    const savedGeminiApiKey = localStorage.getItem('geminiApiKey');
    if (savedGeminiApiKey) {
      setGeminiApiKey(savedGeminiApiKey);
    }
    const savedOllamaUrl = localStorage.getItem('ollamaUrl');
    if (savedOllamaUrl) {
      setOllamaUrl(savedOllamaUrl);
    }
    const savedOllamaModel = localStorage.getItem('ollamaModel');
    if (savedOllamaModel) {
      setOllamaModel(savedOllamaModel);
    }
    const savedLlmProvider = localStorage.getItem('llmProvider');
    if (savedLlmProvider) {
      setLlmProvider(savedLlmProvider);
    }
    const savedGeminiModel = localStorage.getItem('geminiModel');
    if (savedGeminiModel) {
      setGeminiModel(savedGeminiModel);
    }
  }, []);

  useEffect(() => {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]); // Keep this useEffect for scroll

  useEffect(() => {
    if (fullBotMessage) {
      let i = 0;
      const typingInterval = setInterval(() => {
        if (i < fullBotMessage.length) {
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = {
              ...newMessages[newMessages.length - 1],
              text: fullBotMessage.substring(0, i + 1),
            };
            return newMessages;
          });
          i++;
        } else {
          clearInterval(typingInterval);
          setMessages(prev => {
            const newMessages = [...prev];
            let finalMessage = fullBotMessage;
            if (finalMessage.includes('[RESUME]')) {
              finalMessage = finalMessage.replace('[RESUME]', '[Resume](https://drive.google.com/file/d/1xw7USgq9j1MDpDDjVbc8xgicROMZYOLx/view?usp=sharing)');
            }
            newMessages[newMessages.length - 1] = {
              ...newMessages[newMessages.length - 1],
              text: finalMessage,
            };
            return newMessages;
          });
          setFullBotMessage('');
        }
      }, 25); // Adjust typing speed here

      return () => clearInterval(typingInterval);
    }
  }, [fullBotMessage]);



  //const backgroundImageUrl = `${import.meta.env.BASE_URL}${import.meta.env.VITE_BACKGROUND_IMAGE_NAME}`;
  // 1. Sanitize the base path (remove trailing slash)
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");

  // 2. Sanitize the file name (remove leading slash)
  const fileName = (import.meta.env.VITE_BACKGROUND_IMAGE_NAME || "").replace(/^\//, "");

  // 3. Combine them safely
  const backgroundImageUrl = `${base}/${fileName}`;
  return (
    <div
      className="App"
      style={{
        backgroundImage: `url(${backgroundImageUrl})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
        backgroundAttachment: 'fixed',
      }}
    >
      <div className="home-icon-container" onClick={handleHomeClick} title="Click to Home">
        <HomeIcon />
      </div>
      <Icons
        onSettingsClick={() => setShowSettings(true)}
        onAboutClick={() => setShowAbout(true)}
      />
      <main className="main-content">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h1>Curious about Nikhil?</h1>
            <p>Ask me anything about his resume.</p>
          </div>
        ) : (
          <div className="chat-container">
            {messages.map((msg, index) => {
              if (!msg) return null;
              return (
                <div key={index} className={`chat-message ${msg.sender}${msg.isError ? ' error' : ''}${msg.isTyping ? ' typing' : ''}`}>
                  {msg.sender === 'bot' ? (
                    <div className="bot-message-content">
                      {msg.isError && <ErrorIcon />}
                      {msg.isTyping ? (
                        <div className="typing-indicator">
                          <img src={aditiIcon} alt="Aditi icon" className="typing-icon" />
                          <span></span>
                        </div>
                      ) : (
                        <ReactMarkdown components={{ a: LinkRenderer }}>{msg.text || ''}</ReactMarkdown>
                      )}
                    </div>
                  ) : (
                    <p>{msg.text || ''}</p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </main>
      <footer className="footer">
        <div className="input-bar">
          <input
            type="text"
            placeholder="What would you like to know about Nikhil Chaube's resume?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <div className="icon" onClick={handleSend}>
            <SendIcon />
          </div>
        </div>
      </footer>

      <Modal show={showSettings} onClose={handleCloseSettings}>
        <h2>Settings</h2>
        <div className="settings-form">
          <label>LLM Provider</label>
          <select value={llmProvider} onChange={(e) => setLlmProvider(e.target.value)}>
            <option value="gemini">Gemini</option>
            <option value="ollama">Ollama</option>
          </select>

          {llmProvider === 'gemini' && (
            <>
              <label>Gemini API Key</label>
              <input
                type="text"
                value={geminiApiKey}
                onChange={(e) => setGeminiApiKey(e.target.value)}
                placeholder="Your Gemini API Key (e.g., AIza...)"
              />
              <label>Gemini Model</label>
              <input
                type="text"
                value={geminiModel}
                onChange={(e) => setGeminiModel(e.target.value)}
                placeholder="gemini-2.5-flash-lite"
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
                placeholder="http://localhost:11434"
              />
              <label>Ollama Model</label>
              <input
                type="text"
                value={ollamaModel}
                onChange={(e) => setOllamaModel(e.target.value)}
                placeholder="llama3.2 (or other model name)"
              />
            </>
          )}

          <button onClick={handleSaveSettings}>Save</button>
          <button onClick={handleResetSettings} className="reset-button">Reset to Default</button>
        </div>
      </Modal>

      <Modal show={showAbout} onClose={() => setShowAbout(false)}>
        <h2>About This Project</h2>
        <p>This project is a conversational chatbot designed to provide insights into Nikhil Chaube's resume and professional portfolio. Built using modern web technologies and AI, it serves as an interactive way to explore his skills and experiences.</p>
        <div className="social-icons">
          <a href="mailto:nikhilchaube26@gmail.com">
            <EmailIcon />
          </a>
          <a href="https://www.linkedin.com/in/nikhilchaube26/" target="_blank" rel="noopener noreferrer">
            <LinkedinIcon />
          </a>
          <a href="https://github.com/Nikdroid-sys/" target="_blank" rel="noopener noreferrer">
            <GithubIcon />
          </a>
        </div>
      </Modal>

      <ContactModal
        show={showContactModal}
        onClose={handleContactModalClose}
        onSubmit={handleContactSubmit}
      />

    </div>
  );
}

export default App;
