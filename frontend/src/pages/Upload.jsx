import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [codeFile, setCodeFile] = useState(null);
  const [APIFile, setAPIFile] = useState(null);
  const [SecurityFile, setSecurityFile] = useState(null);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  let numOfAPIFiles = 0;
  let numOfSecurityFiles = 0;

  const [selectedModel, setSelectedModel] = useState("gpt-3.5");
  const [selectedDoctype, setSelectedDoctype] = useState("API_Documentation");

  const codeUpload = (event) => {
    setCodeFile(event.target.files[0]);
  };

  const documentationUpload = (event) => {
    if (selectedDoctype == "API_Documentation") {
      setAPIFile(event.target.files[numOfAPIFiles++]);
    }
    else if (selectedDoctype == "Security_Documentation") {
      setSecurityFile(event.target.files[numOfSecurityFiles++]);
    }
    else {
      
    }
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!message.trim() && !codeFile) {
      setError("Please enter a message or upload a file.");
      return;
    }
    
    const formData = new FormData();
    if (codeFile[0]) formData.append("file", codeFile[0]);
    formData.append("message", message);
    for (let i = 0; i < numOfAPIFiles; i++)  {
      formData.append("API_documentation", APIFile[i]);
    }
    for (let i = 0; i < numOfSecurityFiles; i++)  {
      formData.append("Security_documentation", SecurityFile[i]);
    }
    formData.append("model", selectedModel);

    try {
      const res = await fetch(BACKEND_URL + "/api/v1/code-review", {
        method: "POST",
        headers: {
          Authorization: API_KEY,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Error processing request.");
      }

      const data = await res.json();
      setResponse(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };
  const clearAll = () => {
    setMessage("");        
    setCodeFile(null);     
    setAPIFile(null);      
    setSecurityFile(null); 
    setResponse(null);     
    setError(null);        
  };


  return (
    <div className="chat-container">
      <h1>Ask AI for Code Review and Security</h1>
      <form onSubmit={handleSendMessage} className="chat-form">
      <div className="model-selector">
          <select 
            className="model-dropdown" 
            value={selectedModel} 
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            <option value="gpt-3.5">GPT-3.5</option>
            <option value="gpt-4">GPT-4</option>
            <option value="custom-model">Custom Model</option>
          </select>
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="Enter your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="chat-input"
          />
          <input
            type="file"
            id="file-upload"
            onChange={codeUpload}
            className="file-input"
          />
          <label htmlFor="file-upload" className="file-label">📎</label>
        </div>
        <div className="model-selector">
          <select 
            className="model-dropdown" 
            value={selectedDoctype} 
            onChange={(e) => setSelectedDoctype(e.target.value)}
          >
            <option value="API_Documentation">API Documentation</option>
            <option value="Security_Documentation">Security Documentation</option>
            <option value="Librarys/Dependencies">Librarys/Dependencies</option>
          </select>
        </div>
        <div className="input-container">
          <input
            type="file"
            id="file-upload"
            placeholder="Include documentation... (Optional)"
            onChange={documentationUpload}
            className="chat-input"
          />
        </div>
        <button type="submit" className="send-button">Send</button>
        <button onClick={clearAll} type="button" className="clear-button">Clear All</button>
      </form>

      {codeFile && (
        <div className="file-info">
          <p><strong>File:</strong> {codeFile.name}</p>
        </div>
      )}

      {APIFile && (
        <div className="file-info">
          <p><strong>API Documentation:</strong> {APIFile.name}</p>
        </div>
      )}

      {SecurityFile && (
        <div className="file-info">
          <p><strong>Security Documentation:</strong> {SecurityFile.name}</p>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}

      {response && (
        <div className="response-box">
          <h2>Response:</h2>
          <p>{response.reply}</p>
        </div>
      )}
    </div>
  );
};

export default Upload;
