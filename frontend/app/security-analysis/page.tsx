"use client";
import React, { useState } from "react";
import "../../styles/SecurityCodeAnalysis.css";
import MarkdownDisplay from "../../components/MarkdownDisplay";
import { submitCodeForReview, getDatabaseStats, clearDatabase, uploadDocument } from "../../services/apiService";
import Footer from "../../components/Footer";

export default function SecurityCodeAnalysis() {

  const [codeFile, setCodeFile] = useState<File | null>(null);
  const [securityContext, setSecurityContext] = useState("");
  const [language, setLanguage] = useState("python");
  const [referenceDocuments, setReferenceDocuments] = useState<boolean>(false);
  const [response, setResponse] = useState<Response | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<String | null>(null);

  const [documentFile, setDocumentFile] = useState<File | null>(null);
  const [dbStats, setDbStats] = useState<DbStats | null>(null);
  const [dbLoading, setDbLoading] = useState(false);
  const [dbError, setDbError] = useState<String | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<String | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setCodeFile(e.target.files[0]);
    }
  };

  const handleDocumentFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setDocumentFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (!codeFile) {
      setError("Please select a file to analyze");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await submitCodeForReview( // Issue Here: why are we initializing securityContext to null as paramater, need to replace with SecurityContext
        codeFile,
        null,
        language,
        referenceDocuments ? "true" : "false"
      );
      setResponse(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
      else {
        setError("An unknown error has occured")
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFetchStats = async () => {
    setDbLoading(true);
    setDbError(null);
    
    try {
      const stats = await getDatabaseStats();
      setDbStats(stats);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setDbError(error.message);
      }
      else {
        setDbError("An unknown error has occured with the database")
      }
    } finally {
      setDbLoading(false);
    }
  };

  const handleClearDatabase = async () => {
    if (!window.confirm("Are you sure you want to clear the database? This will remove all stored documents.")) {
      return;
    }
    
    setDbLoading(true);
    setDbError(null);
    
    try {
      const result = await clearDatabase();
      setDbStats({ total_documents: 0 });
      setUploadSuccess("Database cleared successfully");
      setTimeout(() => setUploadSuccess(null), 3000);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setDbError(error.message);
      }
      else {
        setDbError("An unknown error has occurred with the database");
      }
    } finally {
      setDbLoading(false);
    }
  };

  const handleUploadDocument = async (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (!documentFile) {
      setDbError("Please select a document to upload");
      return;
    }
    
    if (!documentFile.name.toLowerCase().endsWith('.pdf')) {
      setDbError("Only PDF files are supported");
      return;
    }
    
    setDbLoading(true);
    setDbError(null);
    
    try {
      const result = await uploadDocument(documentFile);
      setUploadSuccess(`Document "${documentFile.name}" uploaded successfully`);
      setTimeout(() => setUploadSuccess(null), 3000);
      setDocumentFile(null);
      document.getElementById("document-file").value = "";
      
      handleFetchStats();
    } catch (error) {
      setDbError(error.message);
    } finally {
      setDbLoading(false);
    }
  };

  const resetForm = () => {
    setCodeFile(null);
    setSecurityContext("");
    setLanguage("python");
    setReferenceDocuments(false);
    setResponse(null);
    setError(null);
    document.getElementById("code-file").value = "";
  };

  return (
    <>
    <div className="security-analysis-container">
      <div className="security-analysis-header">
        <h1>Code Security Analysis</h1>
        <p>Submit your code for security analysis and review</p>
      </div>

      <div className="analysis-card">
        <h3>Security Code Review</h3>
        <div className="analysis-description">
          Upload documentation below and a code file for in-depth security analysis. The system will identify potential security vulnerabilities and best practices.
        </div>
        
        <form className="analysis-form" onSubmit={handleSubmit}>
          <div className="file-input-container">
            <label htmlFor="code-file">Upload Code File:</label>
            <input
              type="file"
              id="code-file"
              onChange={handleFileChange}
            />
            {codeFile && (
              <div className="file-list">
                Selected: {codeFile.name}
              </div>
            )}
          </div>
          
          <div className="form-group">
            <label htmlFor="security-context">Security Focus (Optional):</label>
            <textarea
              id="security-context"
              value={securityContext}
              onChange={(e) => setSecurityContext(e.target.value)}
              placeholder="Specify security concerns or requirements..."
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="language">Programming Language:</label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="csharp">C#</option>
              <option value="cpp">C++</option>
            </select>
          </div>
          
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={referenceDocuments}
                onChange={(e) => setReferenceDocuments(e.target.checked)}
              />
              Reference security documentation in analysis
            </label>
          </div>
          
          <div className="button-group">
            <button
              type="submit"
              className="submit-button"
              disabled={loading || !codeFile}
            >
              {loading ? <span className="loader"></span> : "Analyze Code"}
            </button>
            
            <button
              type="button"
              className="reset-button"
              onClick={resetForm}
            >
              Reset
            </button>
          </div>
        </form>
        
        {error && <div className="error-message">{error}</div>}
        
        {response && (
          <div className="response-container">
            <h4>Security Analysis Results</h4>
            <div className="response-content">
              <MarkdownDisplay content={response.response} />
            </div>
          </div>
        )}
      </div>

      <div className="analysis-card">
        <h3>Database Management</h3>
        <div className="analysis-description">
          Manage security documentation used for code analysis. Upload security guidelines, standards, or best practices.
        </div>
        
        <div className="db-controls">
          <div className="button-group">
            <button
              type="button"
              className="db-button"
              onClick={handleFetchStats}
              disabled={dbLoading}
            >
              {dbLoading ? <span className="loader"></span> : "Get Database Stats"}
            </button>
            
            <button
              type="button"
              className="db-button danger"
              onClick={handleClearDatabase}
              disabled={dbLoading}
            >
              {dbLoading ? <span className="loader"></span> : "Clear Database"}
            </button>
          </div>
          
          {dbStats && (
            <div className="db-stats">
              <h4>Database Statistics</h4>
              <p><strong>Total Chunks:</strong> {dbStats.total_documents}</p>
              {dbStats.collection_name && <p><strong>Collection:</strong> {dbStats.collection_name}</p>}
            </div>
          )}
          
          <form className="upload-form" onSubmit={handleUploadDocument}>
            <h4>Upload Security Document</h4>
            <div className="file-input-container">
              <label htmlFor="document-file">Upload PDF Document:</label>
              <input
                type="file"
                id="document-file"
                onChange={handleDocumentFileChange}
                accept=".pdf"
              />
              {documentFile && (
                <div className="file-list">
                  Selected: {documentFile.name}
                </div>
              )}
            </div>
            
            <button
              type="submit"
              className="submit-button"
              disabled={dbLoading || !documentFile}
            >
              {dbLoading ? <span className="loader"></span> : "Upload Document"}
            </button>
          </form>
          
          {dbError && <div className="error-message">{dbError}</div>}
          {uploadSuccess && <div className="success-message">{uploadSuccess}</div>}
        </div>
      </div>
    </div>
    <div className="container"> ... </div>
    <Footer />
  </>
  );
}
