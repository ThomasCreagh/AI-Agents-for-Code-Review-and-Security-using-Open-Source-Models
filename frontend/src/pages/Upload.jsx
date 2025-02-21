import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [codeFile, setCodeFile] = useState(null);
  const [APIFiles, setAPIFiles] = useState([]);
  const [SecurityFiles, setSecurityFiles] = useState([]);
  const [LibraryFiles, setLibraryFiles] = useState([]);
  const [CodeDocumentationFiles, setCodeDocumentationFiles] = useState([]);
  const [versionControlFiles, setVersionControlFiles] = useState([]);

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const [selectedModel, setSelectedModel] = useState("gpt-3.5");
  const [selectedDoctype, setSelectedDoctype] = useState("API_Documentation");


  const codeUpload = (event) => {
    setCodeFile(event.target.files[0]);
  };

  const documentationUpload = (event) => {
    const files = Array.from(event.target.files);
    if (selectedDoctype === "API_Documentation") {
      setAPIFiles((prev) => [...prev, ...files]);
    } else if (selectedDoctype === "Security_Documentation") {
      setSecurityFiles((prev) => [...prev, ...files]);
    } else if (selectedDoctype === "Librarys/Dependencies") {
      setLibraryFiles((prev) => [...prev, ...files]);
    } else if (selectedDoctype === "Code_Documentation") {
      setCodeDocumentationFiles((prev) => [...prev, ...files]);
    } else if (selectedDoctype === "Version_Control") {
      setVersionControlFiles((prev) => [...prev, ...files]);
    }
  };


  const handleSendMessage = async (event) => {
    event.preventDefault();

    if (
      !message.trim() &&
      !codeFile &&
      APIFiles.length === 0 &&
      SecurityFiles.length === 0 &&
      LibraryFiles.length === 0 &&
      CodeDocumentationFiles.length === 0 &&
      versionControlFiles.length === 0
    ) {
      setError("Please enter a message or upload a file.");
      return;
    }

    const formData = new FormData();
    if (codeFile) formData.append("file", codeFile);
    formData.append("message", message);

    APIFiles.forEach((file) => formData.append("API_documentation", file));
    SecurityFiles.forEach((file) =>
      formData.append("Security_documentation", file)
    );
    LibraryFiles.forEach((file) =>
      formData.append("Library_dependencies", file)
    );
    CodeDocumentationFiles.forEach((file) =>
      formData.append("Code_documentation", file)
    );
    versionControlFiles.forEach((file) =>
      formData.append("Version_Control", file)
    );

    formData.append("model", selectedModel);

    try {
      const res = await fetch(BACKEND_URL + "/api/v1/code-review", {
        method: "POST",
        headers: {
          Authorization: API_KEY,
        },
        body: formData,
      });

      if (!res.ok) throw new Error("Error processing request.");
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
    setAPIFiles([]);
    setSecurityFiles([]);
    setLibraryFiles([]);
    setCodeDocumentationFiles([]);
    setVersionControlFiles([]);
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
          <label htmlFor="file-upload" className="file-label">
            📎
          </label>
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
            <option value="Code_Documentation">Code Documentation</option>
            <option value="Version_Control">Version Control</option>
          </select>
        </div>

        <div className="input-container">
          <input
            type="file"
            multiple
            onChange={documentationUpload}
            className="chat-input"
          />
        </div>

        <button type="submit" className="send-button">Send</button>
        <button onClick={clearAll} type="button" className="clear-button">Clear All</button>
      </form>

      {codeFile && (
        <div className="file-info">
          <p>
            <strong>File:</strong> {codeFile.name}
          </p>
        </div>
      )}

      {APIFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>API Documentation:</strong>{" "}
            {APIFiles.map((file) => file.name).join(", ")}
          </p>
        </div>
      )}

      {SecurityFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Security Documentation:</strong>{" "}
            {SecurityFiles.map((file) => file.name).join(", ")}
          </p>
        </div>
      )}

      {LibraryFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Library Dependencies:</strong>{" "}
            {LibraryFiles.map((file) => file.name).join(", ")}
          </p>
        </div>
      )}

      {CodeDocumentationFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Code Documentation:</strong>{" "}
            {CodeDocumentationFiles.map((file) => file.name).join(", ")}
          </p>
        </div>
      )}

      {versionControlFiles.length > 0 && (
        <div className="file-info">
          <p>
            <strong>Version Control:</strong>{" "}
            {versionControlFiles.map((file) => file.name).join(", ")}
          </p>
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
