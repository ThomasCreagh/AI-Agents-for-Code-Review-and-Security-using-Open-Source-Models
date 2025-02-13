import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const [selectedModel, setSelectedModel] = useState("gpt-3.5");

  const fileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!message.trim() && !file) {
      setError("Please enter a message or upload a file.");
      return;
    }
    
    const formData = new FormData();
    if (file) formData.append("file", file);
    formData.append("message", message);

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
            onChange={fileChange}
            className="file-input"
          />
          <label htmlFor="file-upload" className="file-label">📎</label>
        </div>
        <button type="submit" className="send-button">Send</button>
      </form>

      {file && (
        <div className="file-info">
          <p><strong>File:</strong> {file.name}</p>
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
