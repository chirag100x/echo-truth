/**
 * client.ts
 * API client for EchoTruth backend
 * Handles all communication with the detection endpoint
 * 
 * ============================================
 * CONFIGURATION - API KEYS GO HERE
 * ============================================
 * 
 * For production, replace DEMO_API_KEY with your actual API key.
 * The API key should be stored securely and never committed to git.
 * 
 * In a real deployment:
 * - Use environment variables: import.meta.env.VITE_API_KEY
 * - Or use a secrets manager
 */

import axios, { AxiosError } from "axios";
import type { DetectionResult } from "@/components/ResultCard";

// ============================================
// API CONFIGURATION
// Replace with your backend URL in production
// ============================================
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// ============================================
// DEMO API KEY - FOR DEVELOPMENT ONLY
// In production, use: import.meta.env.VITE_API_KEY
// ============================================
const DEMO_API_KEY = "demo-key-12345";

export interface DetectRequest {
  audio_url?: string;
  audio_base64?: string;
  language: string;
}

export interface ApiError {
  status: number;
  message: string;
  detail?: string;
}

/**
 * Detects if audio is AI-generated or human
 * 
 * @param request - The detection request containing audio URL or base64
 * @returns Promise<DetectionResult> - Classification result with confidence
 * @throws ApiError - On validation, auth, or server errors
 * 
 * API Endpoint: POST /api/v1/detect
 * Headers: Authorization: Bearer <API_KEY>
 */
export async function detectVoice(request: DetectRequest): Promise<DetectionResult> {
  try {
    const response = await axios.post<DetectionResult>(
      `${API_BASE_URL}/api/v1/detect`,
      request,
      {
        headers: {
          "Content-Type": "application/json",
          // ============================================
          // API KEY GOES IN AUTHORIZATION HEADER
          // Format: "Bearer <your-api-key>"
          // ============================================
          "Authorization": `Bearer ${DEMO_API_KEY}`,
        },
        timeout: 60000, // 60 second timeout for audio processing
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<{ detail?: string; message?: string }>;
      
      // Handle specific error codes
      switch (axiosError.response?.status) {
        case 400:
          throw {
            status: 400,
            message: "Missing audio",
            detail: axiosError.response.data?.detail || "Please provide audio_url or audio_base64",
          } as ApiError;
        
        case 401:
          throw {
            status: 401,
            message: "Invalid API key",
            detail: "Please check your Authorization header",
          } as ApiError;
        
        case 422:
          throw {
            status: 422,
            message: "Audio processing error",
            detail: axiosError.response.data?.detail || "Failed to process audio file",
          } as ApiError;
        
        case 500:
          throw {
            status: 500,
            message: "Server error",
            detail: axiosError.response.data?.detail || "Internal server error occurred",
          } as ApiError;
        
        default:
          throw {
            status: axiosError.response?.status || 0,
            message: "Request failed",
            detail: axiosError.message,
          } as ApiError;
      }
    }
    
    // Network error or other issues
    throw {
      status: 0,
      message: "Network error",
      detail: "Could not connect to the server. Please check if the backend is running.",
    } as ApiError;
  }
}

/**
 * Health check endpoint
 * Use to verify backend is running
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
    return response.status === 200;
  } catch {
    return false;
  }
}

export default { detectVoice, healthCheck };
