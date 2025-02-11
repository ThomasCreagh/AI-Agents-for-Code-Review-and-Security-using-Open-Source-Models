import React, { useState } from "react";
import "../styles/Upload.css";

const API_KEY = process.env.REACT_APP_API_KEY;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Upload = () => {
  const [file, setFile] = useState(null);
  const [errorDescription, setErrorDescription] = useState("");
  const [language, setLanguage] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const fileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const fileSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("error_description", errorDescription);
      formData.append("language", language);

      try {
        const res = await fetch(BACKEND_URL + "/api/v1/code-review/file", {
          method: "POST",
          headers: {
            Authorization: API_KEY,
          },
          body: formData,
        });

        if (!res.ok) {
          throw new Error("File upload failed.");
        }

        const data = await res.json();
        setResponse(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
      console.log("File to be uploaded:", file);
    } else {
      console.log("No file detected.");
    }
  };

  return (
    <div className="upload-box">
      <h1>Upload Your File</h1>
      <form onSubmit={fileSubmit}>
        <input type="file" onChange={fileChange} required />

        <input
          type="text"
          placeholder="Enter Error Description (optional)"
          value={errorDescription}
          onChange={(e) => setErrorDescription(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter Programming Language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          required
        />

        <button type="submit" className="upload-button">
          Upload
        </button>
      </form>

      {file && (
        <div className="file-info">
          <p>
            <strong>File Name:</strong> {file.name}
          </p>
          <p>
            <strong>File Size:</strong> {file.size} bytes
          </p>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}

      {response && (
        <div className="response-box">
          <h2>Response code suggestion:</h2>
          <p>{JSON.stringify(response.suggestion, null, 2)}</p>
        </div>
      )}
    </div>
  );
};

export default Upload;
