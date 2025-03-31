"use client";
import React, { useState, useRef, useEffect } from "react";
import "../../styles/SecurityCodeAnalysis.css";
import MarkdownDisplay from "../../components/MarkdownDisplay";
import Image from "next/image";
import Footer from "../../components/Footer";
import {
  submitCodeForReview,
  getDatabaseStats,
  clearDatabase,
  uploadDocument,
} from "../../services/apiService";

interface Response {
  response: string;
}

interface DBResponse {
  collection_name: string | undefined;
  total_documents: number;
}

export default function SecurityCodeAnalysis() {
  const [codeFile, setCodeFile] = useState<File | null>(null);
  const [securityContext, setSecurityContext] = useState<String | null>("");
  const [language, setLanguage] = useState("python");
  const [referenceDocuments, setReferenceDocuments] = useState<string>("");

  const [response, setResponse] = useState<Response | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<String | null>(null);

  const [documentFile, setDocumentFile] = useState<File | null>(null);
  const [dbStats, setDbStats] = useState<DBResponse | null>(null);
  const [dbLoading, setDbLoading] = useState(false);
  const [dbError, setDbError] = useState<String | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<String | null>(null);

  const [gravity, setGravity] = useState<boolean | null>(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  class Particle {
    x: number;
    y: number;
    size: number;
    speedX: number;
    speedY: number;
    color: string;
    gravity: number;
    isGravity: boolean;
  
    constructor(canvasWidth, canvasHeight) {
      this.x = Math.random() * canvasWidth;
      this.y = Math.random() * canvasHeight;
      this.size = Math.random() * 3 + 1;
      this.speedX = (Math.random() - 0.5) * 0.5;
      this.speedY = (Math.random() - 0.5) * 0.5;
      this.color = "#0f62fe";
      this.gravity = 0.98;
      this.isGravity = false;
    }
  
    update(canvasWidth, canvasHeight) {
      if (!this.isGravity) {
        if (this.speedX > 4 || this.speedX < -4) { // reinitialize speed
          if (this.speedX > 2 || this.speedX < -2) {
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
          }
          else {
            this.speedX = this.speedX * 0.95;      // take down by factor of 0.95 for smoother transistion
            this.speedY *= 1.01;
          }
        }
        this.x += this.speedX;
        this.y += this.speedY;
      } else {
        this.x += this.gravity * this.speedX;
        this.y += this.speedY;
        this.speedY *= 0.99;
        if (this.speedX < 4 && this.speedX > -4) {
          this.speedX *= 1.01;
        }
      }
  
      // Keep particles within bounds
      if (this.x > canvasWidth) this.x = 0;
      else if (this.x < 0) this.x = canvasWidth;
      if (this.y > canvasHeight) this.y = canvasHeight; // Let it fall down
      else if (this.y < 0) this.y = canvasHeight;
    }
  
    draw(ctx) {
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }
  
  const particlesRef = useRef<Particle[]>([]);
  
  useEffect(() => {
    particlesRef.current.forEach((p) => {
      p.isGravity = gravity;
    });
  }, [gravity]);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
  
    const setCanvasDimensions = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
  
    setCanvasDimensions();
    window.addEventListener("resize", setCanvasDimensions);
  
    // Initialize particles only once
    if (particlesRef.current.length === 0) {
      for (let i = 0; i < 60; i++) {
        particlesRef.current.push(new Particle(canvas.width, canvas.height));
      }
    }
  
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particlesRef.current.forEach((p) => {
        p.update(canvas.width, canvas.height);
        p.draw(ctx);
      });
      requestAnimationFrame(animate);
    }
  
    animate();
  
    return () => {
      window.removeEventListener("resize", setCanvasDimensions);
    };
  }, []);

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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!codeFile) {
      setError("Please select a file to analyze");
      return;
    }
    setGravity(true);
    setLoading(true);
    setError(null);

    try {
      const result = await submitCodeForReview(
        // Issue Here: why are we initializing securityContext to null as paramater, need to replace with SecurityContext
        codeFile,
        securityContext,
        language,
        referenceDocuments ? "true" : "false",
      );
      setResponse(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unknown error has occured");
      }
    } finally {
      setGravity(false);
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
      } else {
        setDbError("An unknown error has occured with the database");
      }
    } finally {
      setDbLoading(false);
    }
  };

  const handleClearDatabase = async () => {
    if (
      !window.confirm(
        "Are you sure you want to clear the database? This will remove all stored documents.",
      )
    ) {
      return;
    }

    setDbLoading(true);
    setDbError(null);

    try {
      const result = await clearDatabase();
      setDbStats({
        collection_name: dbStats?.collection_name,
        total_documents: 0,
      });
      setUploadSuccess("Database cleared successfully");
      setTimeout(() => setUploadSuccess(null), 3000);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setDbError(error.message);
      } else {
        setDbError("An unknown error has occurred with the database");
      }
    } finally {
      setDbLoading(false);
    }
  };

  const handleUploadDocument = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!documentFile) {
      setDbError("Please select a document to upload");
      return;
    }

    if (!documentFile.name.toLowerCase().endsWith(".pdf")) {
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
      const fileInputElement = document.getElementById(
        "document-file",
      ) as HTMLInputElement;
      fileInputElement.value = "";

      handleFetchStats();
    } catch (error) {
      if (error instanceof Error) {
        setDbError(error.message);
      } else {
        setDbError("An unknown error occurred");
      }
    } finally {
      setDbLoading(false);
    }
  };

  const resetForm = () => {
    setCodeFile(null);
    setSecurityContext("");
    setLanguage("python");
    setReferenceDocuments("");
    setResponse(null);
    setError(null);

    const fileInput = document.getElementById("code-file") as HTMLInputElement | null;
    if (fileInput) {
      fileInput.value = "";
    }
    const fileInputElement = document.getElementById(
      "document-file",
    ) as HTMLInputElement;
    fileInputElement.value = "";
  };


  return (
    <>
      <div className="security-analysis-container">

      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full -z-5 opacity-70 pointer-events-none"></canvas>

        <div className="security-analysis-header relative z-20">
          <h1 className="-mt-25 text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-[#161616] leading-tight mb-10">Code Security Analysis</h1>
          <p className="text-1xl md:text-2xl text-[#393939] max-w-2xl mx-auto mb-12">Submit your code for security analysis and review</p>
        </div>

        <div className="analysis-card relative z-20">
          <h3 className="text-1xl md:text-2xl text-[#393939] mb-5">Security Code Review</h3>
          <div className="analysis-description text-m md:text-l text-[#393939] mb-10">
            Upload documentation below and a code file for in-depth security
            analysis. The system will identify potential security vulnerabilities
            and best practices.
          </div>

          <form className="analysis-form" onSubmit={handleSubmit}>

            <div className="flex justify-center items-center border-2 border-dashed border-[#0f62fe] rounded-lg py-10 mb-6 cursor-pointer hover:bg-[#e6f0ff] transition-all">
              <label className="flex flex-col items-center text-[#0f62fe] space-y-2 cursor-pointer">
                <span className="text-lg font-medium">Drag and Drop your code file here: </span>
                <input type="file" className="hidden" onChange={handleFileChange}/>
                <button className="text-sm text-[#0f62fe] bg-white px-4 py-2 rounded-md hover:bg-[#e0e0e0] transition-all">
                  Or click to browse...
                </button>
                {codeFile && (
                <div className="file-list text-lg font-medium">Selected: {codeFile.name}</div>
                )}
              </label>
            </div>

            <div className="form-group">
              <label htmlFor="security-context" className="text-l md:text-1xl text-[#393939] mb-2">Security Focus (Optional):</label>
              <textarea
                id="security-context"
                value={securityContext}
                onChange={(e) => setSecurityContext(e.target.value)}
                placeholder="Specify security concerns or requirements..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="language" className="text-l md:text-1xl text-[#393939] mb-2">Programming Language:</label>
              <select
                className="bg-white border border-[#0f62fe] text-[#393939] rounded-lg px-4 py-2 appearance-none focus:outline-none focus:ring-3 focus:ring-[#0f62fe] transition-all hover:bg-[#f1f9ff] cursor-pointer"
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
                  className="text-lg font-medium"
                />
                Reference security documentation in analysis
              </label>
            </div>

            <div className="button-group justify-center mx-auto">
              <button
                type="submit"
                className="submit-button flex border-2 border-dashed border-[#0f62fe] rounded-lg"
                disabled={loading || !codeFile}
              >
                {loading ? (<span className="loader"></span>) :
                    (<>
                      <span className="mr-4">Analyze Code</span>
                      <Image 
                        src="/magnifying-glass.png" 
                        alt="magnifying-glass"
                        width={25} 
                        height={22}
                      />
                    </>)}
              </button>

              <button type="button" className="reset-button mx-auto" onClick={resetForm}>
                Reset
              </button>
            </div>
          </form >

          {error && <div className="error-message">{error}</div>
          }

          {
            response && (
              <div className="response-container">
                <h4>Security Analysis Results</h4>
                <div className="response-content">
                  <MarkdownDisplay content={response.response} />
                </div>
              </div>
            )
          }
        </div >

        <div className="analysis-card relative z-20">
          <h3 className="text-1xl md:text-2xl text-[#393939] mb-5">Database Management</h3>
          <div className="analysis-description text-m md:text-l text-[#393939] mb-10">
            Manage security documentation used for code analysis. Upload security
            guidelines, standards, or best practices.
          </div>

          <div className="db-controls">
            <div className="button-group">
              <button
                type="button"
                className="db-button bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-10 py-5 transition-all flex items-center justify-center group text-lg"
                onClick={handleFetchStats}
                disabled={dbLoading}
              >
                {dbLoading ? (
                  <span className="loader"></span>
                ) : (
                  "Get Database Stats"
                )}
              </button>

              <button
                type="button"
                className="db-button danger bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-10 py-5 transition-all flex items-center justify-center group text-lg"
                onClick={handleClearDatabase}
                disabled={dbLoading}
              >
                {dbLoading ? <span className="loader"></span> : "Clear Database"}
              </button>
            </div>

            {dbStats && (
              <div className="db-stats">
                <h4>Database Statistics</h4>
                <p>
                  <strong>Total Chunks:</strong> {dbStats.total_documents}
                </p>
                {dbStats.collection_name && (
                  <p>
                    <strong>Collection:</strong> {dbStats.collection_name}
                  </p>
                )}
              </div>
            )}

            <form className="upload-form" onSubmit={handleUploadDocument}>
              <h4>Upload Security Document</h4>

              <div className="form-group">
                <label htmlFor="security-doc">Select Security Document:</label>
                <div className="flex flex-col gap-3 mt-2">
                  {[
                    "OWASP",
                    "NIST",
                    "CERT Secure Coding Standards",
                    "NASA Rules",
                    "ISO/IEC 27001 & 27002",
                    "Custom",
                  ].map((doc) => (
                    <label key={doc} className="flex items-center gap-2">
                      <input
                        type="radio"
                        name="security-doc"
                        value={doc}
                        checked={referenceDocuments === doc}
                        onChange={(e) => setReferenceDocuments(e.target.value)}
                      />
                      {doc}
                    </label>
                  ))}
                </div>
              </div>

              <div className="file-input-container">
                <label htmlFor="document-file">Upload PDF Document:</label>
                <input
                  type="file"
                  id="document-file"
                  onChange={handleDocumentFileChange}
                  accept=".pdf"
                />
                {documentFile && (
                  <div className="file-list">Selected: {documentFile.name}</div>
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
            {uploadSuccess && (
              <div className="success-message">{uploadSuccess}</div>
            )}
          </div>
        </div>
      </div >
      <div className="container"> ... </div>
      <Footer />
    </>
  );
}
