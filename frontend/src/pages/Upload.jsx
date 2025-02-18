import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [codeFiles, setCodeFiles] = useState([]);
  const [APIFiles, setAPIFiles] = useState([]);
  const [SecurityFiles, setSecurityFiles] = useState([]);
  const [errorDescription, setErrorDescription] = useState("");
  const [language, setLanguage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  let numOfAPIFiles = 0;
  let numOfSecurityFiles = 0;

  const [selectedModel, setSelectedModel] = useState("gpt-3.5");
  const [selectedDoctype, setSelectedDoctype] = useState("API_Documentation");
  //
  // const handleCodeFileChange = (event) => {
  //   const selectedFiles = Array.from(event.target.files);
  //   setCodeFiles(selectedFiles);
  // };

  const codeUpload = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setCodeFiles(selectedFiles);
  };

  const documentationUpload = (event) => {
    if (selectedDoctype == "API_Documentation") {
      const selectedFiles = Array.from(event.target.files);
      setAPIFiles(selectedFiles);
    } else if (selectedDoctype == "Security_Documentation") {
      const selectedFiles = Array.from(event.target.files);
      setSecurityFiles(selectedFiles);
    } else {
    }
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (!errorDescription.trim() && codeFiles.length === 0) {
      setError("Please enter a message or upload files.");
      return;
    }

    const formData = new FormData();

    if (codeFiles.length > 0) {
      codeFiles.forEach((file) => {
        formData.append("code_files", file);
      });
    }

    if (APIFiles.length > 0) {
      APIFiles.forEach((file) => {
        formData.append("api_documentation", file);
      });
    }

    if (SecurityFiles.length > 0) {
      SecurityFiles.forEach((file) => {
        formData.append("security_documentation", file);
      });
    }

    // # api_documentation
    // # security_documentation
    // # library_dependency
    // # code_documentation
    // # version_control

    formData.append("error_description", errorDescription);
    formData.append("model", selectedModel);

    try {
      const res = await fetch(BACKEND_URL + "/code-review/file", {
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
      setCodeFiles([]);
      setAPIFiles([]);
      setSecurityFiles([]);
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
            placeholder="Enter the programming language..."
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="chat-input"
          />
          <input
            type="file"
            id="file-upload"
            onChange={codeUpload}
            className="file-input"
            multiple
          />
          <label htmlFor="file-upload" className="file-label">
            📎
          </label>
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="Enter your error description..."
            value={errorDescription}
            onChange={(e) => setErrorDescription(e.target.value)}
            className="chat-input"
          />
        </div>
        <div className="input-container">
          <div className="model-selector">
            <select
              className="model-dropdown"
              value={selectedDoctype}
              onChange={(e) => setSelectedDoctype(e.target.value)}
            >
              <option value="API_Documentation">API Documentation</option>
              <option value="Security_Documentation">
                Security Documentation
              </option>
            </select>
          </div>
          <input
            type="file"
            id="doc-upload"
            onChange={documentationUpload}
            className="file-input"
            multiple
          />
          <label htmlFor="doc-upload" className="file-label">
            📎
          </label>
        </div>
        <button type="submit" className="send-button">
          Send
        </button>
      </form>
      {codeFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Code File:</strong>
          </p>
          <ul>
            {codeFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}

      {APIFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>API Documentation:</strong>
          </p>
          <ul>
            {APIFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}

      {SecurityFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Security Documentation:</strong>
          </p>
          <ul>
            {SecurityFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
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
