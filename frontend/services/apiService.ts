const API_KEY: string | undefined = process.env.NEXT_PUBLIC_API_KEY;
const BACKEND_URL: string =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:broken/api/v1";

interface ApiRequestOptions {
  endpoint: string;
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: Record<string, any> | null;
  files?: {
    code_files?: File[];
    code_file?: File;
    document_file?: File;
  } | null;
}

const apiRequest = async <T>({
  endpoint,
  method = "GET",
  body = null,
  files = null,
}: ApiRequestOptions): Promise<T> => {
  const headers: HeadersInit = {
    Authorization: API_KEY || "hello",
  };

  let requestOptions: RequestInit = {
    method,
    headers,
  };

  if (files) {
    const formData = new FormData();

    if (files.code_files) {
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
    delete (requestOptions.headers as Record<string, string>)["Content-Type"];
  } else if (body) {
    requestOptions.body = JSON.stringify(body);
    requestOptions.headers = {
      ...headers,
      "Content-Type": "application/json",
    };
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
  codeFile: File,
  securityContext: string | null = null,
  language: string = "python",
  referenceDocuments: string = "false",
): Promise<any> => {
  const formData = {
    language,
    security_context: securityContext || "",
    reference_docs: referenceDocuments,
  };

  return apiRequest({
    endpoint: "/ast-analysis/submit-code-for-review",
    method: "POST",
    body: formData,
    files: { code_file: codeFile },
  });
};

export const reviewCodeFile = async (
  codeFiles: File[],
  errorDescription: string = "",
  language: string = "python",
  model: string | null = null,
): Promise<any> => {
  const formData: Record<string, any> = {
    error_description: errorDescription,
    language,
  };

  if (model) {
    formData.model = model;
  }

  return apiRequest({
    endpoint: "/code-review/file",
    method: "POST",
    body: formData,
    files: { code_files: codeFiles },
  });
};

export const getDatabaseStats = async (): Promise<any> => {
  return apiRequest({ endpoint: "/database/stats" });
};

export const clearDatabase = async (): Promise<any> => {
  return apiRequest({ endpoint: "/database/clear", method: "POST" });
};

export const uploadDocument = async (documentFile: File): Promise<any> => {
  return apiRequest({
    endpoint: "/documents/upload",
    method: "POST",
    body: {},
    files: { document_file: documentFile },
  });
};
