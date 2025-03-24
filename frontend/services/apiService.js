const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:broken/api/v1";

const apiRequest = async (
  endpoint,
  method = "GET",
  body = null,
  files = null,
) => {
  const headers = {
    Authorization: API_KEY,
  };

  let requestOptions = {
    method,
    headers,
  };

  if (files) {
    const formData = new FormData();

    if (Array.isArray(files.code_files)) {
      files.code_files.forEach((file) => {
        formData.append("code_files", file);
      });
    }

    if (files.code_file) {
      formData.append("code_file", files.code_file);
    }

    if (files.document_file) {
      formData.append("file", files.document_file);
    }

    if (body) {
      Object.keys(body).forEach((key) => {
        formData.append(key, body[key]);
      });
    }

    requestOptions.body = formData;
    delete requestOptions.headers["Content-Type"];
  } else if (body) {
    requestOptions.body = JSON.stringify(body);
    requestOptions.headers["Content-Type"] = "application/json";
  }

  try {
    const response = await fetch(`${BACKEND_URL}${endpoint}`, requestOptions);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Error: ${response.status} ${response.statusText}`,
      );
    }

    return await response.json();
  } catch (error) {
    console.error("API Request Error:", error);
    throw error;
  }
};

export const submitCodeForReview = async (
  codeFile,
  securityContext = null,
  language = "python",
  referenceDocuments = "false",
) => {
  const formData = {
    language,
    security_context: securityContext || "",
    reference_docs: referenceDocuments,
  };

  return apiRequest("/ast-analysis/submit-code-for-review", "POST", formData, {
    code_file: codeFile,
  });
};

export const reviewCodeFile = async (
  codeFiles,
  errorDescription = "",
  language = "python",
  model = null,
) => {
  const formData = {
    error_description: errorDescription,
    language,
  };

  if (model) {
    formData.model = model;
  }

  return apiRequest("/code-review/file", "POST", formData, {
    code_files: codeFiles,
  });
};

export const getDatabaseStats = async () => {
  return apiRequest("/database/stats");
};

export const clearDatabase = async () => {
  return apiRequest("/database/clear", "POST");
};

export const uploadDocument = async (documentFile) => {
  return apiRequest(
    "/documents/upload",
    "POST",
    {},
    { document_file: documentFile },
  );
};
