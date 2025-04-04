"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import "../../styles/SecurityCodeAnalysis.css";
import MarkdownDisplay from "../../components/MarkdownDisplay";
import Image from "next/image";
import Footer from "../../components/Footer";
import ParticleCanvas from "../../components/ParticleCanvas";
import Head from "next/head";
import {
  submitCodeForReview,
  getDatabaseStats,
  clearDatabase,
  uploadDocument,
} from "../../services/apiService";
import { supabase } from "@/src/services/supabaseClient";

interface Response {
  response: string;
}

interface DBResponse {
  collection_name: string | undefined;
  total_documents: number;
}

export default function SecurityCodeAnalysis() {
  const [codeFile, setCodeFile] = useState<File | null>(null);
  const [securityContext, setSecurityContext] = useState<string | null>(null);
  const [language, setLanguage] = useState("python");
  const [referenceDocuments, setReferenceDocuments] = useState<string | null>(
    null,
  );

  const [response, setResponse] = useState<Response | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [documentFile, setDocumentFile] = useState<File | null>(null);
  const [dbStats, setDbStats] = useState<DBResponse | null>(null);
  const [dbLoading, setDbLoading] = useState(false);
  const [dbError, setDbError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);

  const router = useRouter();
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const { data } = await supabase.auth.getSession();
      if (!data.session) {
        router.replace("/login");
      } else {
        setLoadingAuth(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loadingAuth) {
    return (
      <div className="flex justify-center items-center min-h-screen text-xl">
        Checking authentication...
      </div>
    );
  }

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
    // setGravity(true);
    setLoading(true);
    setError(null);

    try {
      const result = await submitCodeForReview(
        codeFile,
        securityContext,
        language,
        referenceDocuments ? "true" : "false",
      );

      console.log(result);
      if (result.status == "error") {
        setResponse(result.message);
      }
      setResponse(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unknown error has occurred");
      }
    } finally {
      // setGravity(false);
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
      console.log(result);
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
      console.log(result);
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
    //setGravity(!gravity);
    setSecurityContext("");
    setLanguage("python");
    setReferenceDocuments("");
    setResponse(null);
    setError(null);

    const fileInput = document.getElementById(
      "code-file",
    ) as HTMLInputElement | null;
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
      <Head>
        <title>Keysentinel Security Analysis</title>
        <meta property="og:title" content="My page title" key="title" />
      </Head>
      <div className="security-analysis-container">
        <ParticleCanvas />

        <div className="security-analysis-header relative z-20">
          <h1 className="-mt-25 text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-[#161616] leading-tight mb-10">
            Code Security Analysis
          </h1>
          <p className="text-1xl md:text-2xl text-[#393939] max-w-2xl mx-auto mb-12">
            Submit your code for security analysis and review
          </p>
        </div>

        <div className="analysis-card relative z-20">
          <h3 className="text-1xl md:text-2xl text-[#393939] mb-5">
            Security Code Review
          </h3>
          <div className="analysis-description text-m md:text-l text-[#393939] mb-10">
            Upload documentation below and a code file for in-depth security
            analysis. The system will identify potential security
            vulnerabilities and best practices.
          </div>

          <form className="analysis-form" onSubmit={handleSubmit}>
            <div className="file-drop-area relative flex justify-center items-center border-2 border-dashed border-[#0f62fe] rounded-lg py-10 mb-6 cursor-pointer hover:bg-[#e6f0ff] transition-all">
              <input
                type="file"
                className="absolute w-full h-full top-0 left-0 opacity-0 cursor-pointer"
                onChange={handleFileChange}
              />
              <label className="flex flex-col items-center text-[#0f62fe] space-y-2 cursor-pointer relative">
                <span className="text-lg font-medium">
                  Drag and Drop your code file here:{" "}
                </span>
                <button className="text-sm text-[#0f62fe] bg-white px-4 py-2 rounded-md hover:bg-[#e0e0e0] transition-all">
                  Or click to browse...
                </button>
                {codeFile && (
                  <div className="file-list text-lg font-medium">
                    Selected: {codeFile.name}
                  </div>
                )}
              </label>
            </div>

            <div className="form-group">
              <label
                htmlFor="security-context"
                className="text-l md:text-1xl text-[#393939] mb-2"
              >
                Security Focus (Optional):
              </label>
              <textarea
                id="security-context"
                value={securityContext ?? undefined}
                onChange={(e) => setSecurityContext(e.target.value)}
                placeholder="Specify security concerns or requirements..."
                className=""
              />
            </div>

            <div className="form-group">
              <label
                htmlFor="language"
                className="text-l md:text-1xl text-[#393939] mb-2"
              >
                Programming Language:
              </label>
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
                  checked={referenceDocuments != ""}
                  onChange={(e) =>
                    setReferenceDocuments(e.target.checked ? "true" : "false")
                  }
                  className="hidden"
                />
                <span
                  className={`w-5 h-5 border-2 border-gray-400 rounded-lg flex items-center justify-center transition-all duration-125 ${referenceDocuments ? "bg-blue-600 border-blue-600" : "bg-white"}`}
                >
                  {referenceDocuments && (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="w-3 h-3 text-white"
                      fill="none"
                      viewBox="0 0 25 25"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  )}
                </span>
                <span className="text-gray-600">
                  Reference security documentation in analysis
                </span>
              </label>
            </div>

            <div className="button-group justify-center mx-auto">
              <button
                type="submit"
                className="submit-button flex border-2 border-dashed border-[#0f62fe] rounded-lg"
                disabled={loading || !codeFile}
              >
                {loading ? (
                  <span className="loader"></span>
                ) : (
                  <>
                    <span className="mr-4">Analyze Code</span>
                    <Image
                      src="/magnifying-glass.png"
                      alt="magnifying-glass"
                      width={25}
                      height={22}
                    />
                  </>
                )}
              </button>

              <button
                type="button"
                className="reset-button mx-auto"
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

        <div className="analysis-card relative z-20">
          <h3 className="text-1xl md:text-2xl text-[#393939] mb-5">
            Database Management
          </h3>
          <div className="analysis-description text-m md:text-l text-[#393939] mb-10">
            Manage security documentation used for code analysis. Upload
            security guidelines, standards, or best practices.
          </div>

          <div className="db-controls">
            <div className="button-group justify-center mx-auto">
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
                {dbLoading ? (
                  <span className="loader"></span>
                ) : (
                  "Clear Database"
                )}
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
              <h4 className="text-l md:text-1xl text-[#393938] mb-2">
                Upload Security Document
              </h4>

              <div className="form-group">
                <label
                  htmlFor="security-doc"
                  className="block text-lg font-semibold text-gray-800 mb-2"
                >
                  Select Security Document:
                </label>
                <div className="flex flex-col gap-4 mt-2 bg-blue-50 p-4 rounded-lg">
                  {[
                    "OWASP",
                    "NIST",
                    "CERT Secure Coding Standards",
                    "NASA Rules",
                    "ISO/IEC 27001 & 27002",
                    "Custom",
                  ].map((doc) => (
                    <label
                      key={doc}
                      className="flex items-center gap-2 cursor-pointer hover:bg-[#f1f9ff] p-3 rounded-lg transition duration-175"
                    >
                      <input
                        type="radio"
                        className="hidden"
                        name="security-doc"
                        value={doc}
                        checked={referenceDocuments === doc}
                        onChange={(e) => setReferenceDocuments(e.target.value)}
                      />
                      <span className="w-4 h-4 rounded-full border-1 border-gray-400 flex items-center justify-center relative">
                        <span
                          className={`w-2.5 h-2.5 rounded-full bg-blue-600 transition-all duration-200 ${referenceDocuments === doc
                              ? "opacity-100"
                              : "opacity-0"
                            }`}
                        />
                      </span>
                      <span className="text-lg text-gray-700">{doc}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="file-drop-area relative flex justify-center items-center border-2 border-dashed border-[#0f62fe] rounded-lg py-10 mb-6 cursor-pointer hover:bg-[#e6f0ff] transition-all">
                <input
                  type="file"
                  id="document-file"
                  className="absolute w-full h-full top-0 left-0 opacity-0 cursor-pointer"
                  onChange={handleDocumentFileChange}
                />
                <label className="flex flex-col items-center text-[#0f62fe] space-y-2 cursor-pointer relative">
                  <span className="text-lg font-medium">
                    Drag and Drop your Security Documentation here:{" "}
                  </span>
                  <button className="text-sm text-[#0f62fe] bg-white px-4 py-2 rounded-md hover:bg-[#e0e0e0] transition-all">
                    Or click to browse...
                  </button>
                  {documentFile && (
                    <div className="file-list text-lg font-medium">
                      Selected: {documentFile.name}
                    </div>
                  )}
                </label>
              </div>

              <button
                type="submit"
                className="submit-button"
                disabled={dbLoading || !documentFile}
              >
                {dbLoading ? (
                  <span className="loader"></span>
                ) : (
                  "Upload Document"
                )}
              </button>
            </form>

            {dbError && <div className="error-message">{dbError}</div>}
            {uploadSuccess && (
              <div className="success-message">{uploadSuccess}</div>
            )}
          </div>
        </div>
      </div>
      <div className="container"> ... </div>
      <Footer />
    </>
  );
}
