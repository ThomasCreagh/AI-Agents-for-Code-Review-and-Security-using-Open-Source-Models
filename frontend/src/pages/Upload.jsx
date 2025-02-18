import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [codeFiles, setCodeFiles] = useState([]);
  const [docFiles, setDocFiles] = useState([]);
  // const [message, setMessage] = useState("");
  const [errorDescription, setErrorDescription] = useState("");
  const [language, setLanguage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState("gpt-3.5");

  const handleCodeFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setCodeFiles(selectedFiles);
  };

  const handleDocFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setDocFiles(selectedFiles);
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (
      !errorDescription.trim() &&
      codeFiles.length === 0 &&
      docFiles.length === 0
    ) {
      setError("Please enter a message or upload files.");
      return;
    }

    const formData = new FormData();

    if (codeFiles.length > 0) {
      codeFiles.forEach((file) => {
        formData.append("code_files", file);
      });
    }

    if (docFiles.length > 0) {
      docFiles.forEach((file) => {
        formData.append("documentation_files", file);
      });
    }

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
            placeholder="Enter your error description..."
            value={errorDescription}
            onChange={(e) => setErrorDescription(e.target.value)}
            className="chat-input"
          />
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="Enter the programming language..."
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="chat-input"
          />
        </div>
        <div className="input-container">
          <input
            type="file"
            id="code-file-upload"
            onChange={handleCodeFileChange}
            className="file-input"
            multiple
          />
          <label htmlFor="code-file-upload" className="send-button">
            📂 Upload Code Files
          </label>
        </div>
        <div className="input-container">
          <input
            type="file"
            id="doc-file-upload"
            onChange={handleDocFileChange}
            className="file-input"
            multiple
          />
          <label htmlFor="doc-file-upload" className="send-button">
            📄 Upload Document Files
          </label>
        </div>
        <button type="submit" className="send-button">
          Send
        </button>
      </form>

      {codeFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Code Files:</strong>
          </p>
          <ul>
            {codeFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}

      {docFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Document Files:</strong>
          </p>
          <ul>
            {docFiles.map((file, index) => (
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
