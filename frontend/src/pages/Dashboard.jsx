import React, { useState } from "react";
import "../styles/Dashboard.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Dashboard = () => {
  const [docFile, setDocFile] = useState(null);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState("API documentation");

  const documentationUpload = (event) => {
    setDocFile(event.target.files[0]);
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!docFile[0]) {
      setError("Please upload a file!");
      return;
    }
    
  };

  return (
    <div className="docUpload-container">
      <h1>Documentation Dashboard</h1>
      <h2>Please upload all relevant documentation relating to your code review here:</h2>
      <form onSubmit={handleSendMessage} className="chat-form">
      <div className="doctype-selector">
          <select 
            className="doctype-dropdown" 
            value={selectedModel} 
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            <option value="API_documentation">API documentation</option>
            <option value="Security_documentation">Security documentation</option>
            <option value="Library/dependency">Library/dependency</option>
            <option value="Code_Documentation">Code Documentation</option>
            <option value="Version_Control">Version Control</option>
          </select>
        </div>
        <div className="input-container">
          <input
            type="file"
            id="file-upload"
            placeholder="Insert relevant documentation here (Optional)"
            onChange={documentationUpload}
            className="doc-input"
          />
        </div>
        <button type="submit" className="send-button">Send</button>
      </form>

      {docFile && (
        <div className="file-info">
          <p><strong>Documentation:</strong> {docFile.name}</p>
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

export default Dashboard;