/**
 * useAppState.ts
 * Global application state management using React hooks
 * Manages detection state, results, and error handling
 */

import { useState, useCallback } from "react";
import type { DetectionResult } from "@/components/ResultCard";

export type AppStatus = "idle" | "loading" | "success" | "error";

export interface AppState {
  status: AppStatus;
  result: DetectionResult | null;
  error: string | null;
}

export interface AppActions {
  startDetection: () => void;
  setResult: (result: DetectionResult) => void;
  setError: (error: string) => void;
  reset: () => void;
}

const initialState: AppState = {
  status: "idle",
  result: null,
  error: null,
};

export function useAppState(): [AppState, AppActions] {
  const [state, setState] = useState<AppState>(initialState);

  const startDetection = useCallback(() => {
    setState({
      status: "loading",
      result: null,
      error: null,
    });
  }, []);

  const setResult = useCallback((result: DetectionResult) => {
    setState({
      status: "success",
      result,
      error: null,
    });
  }, []);

  const setError = useCallback((error: string) => {
    setState({
      status: "error",
      result: null,
      error,
    });
  }, []);

  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  return [
    state,
    {
      startDetection,
      setResult,
      setError,
      reset,
    },
  ];
}

export default useAppState;
