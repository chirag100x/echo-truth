/**
 * Index.tsx
 * Main page component for EchoTruth
 * Handles the detection flow and displays results
 */

import { useState } from "react";
import { UploadCard } from "@/components/UploadCard";
import { ResultCard, type DetectionResult } from "@/components/ResultCard";
import { Loader } from "@/components/Loader";
import { useAppState } from "@/state/useAppState";
import { detectVoice, type ApiError } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Waves, Github, ShieldCheck, Zap, Globe, RefreshCw } from "lucide-react";

// Demo/mock detection for frontend testing without backend
const mockDetection = async (): Promise<DetectionResult> => {
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const isAI = Math.random() > 0.5;
  return {
    classification: isAI ? "AI_GENERATED" : "HUMAN",
    confidence: 0.65 + Math.random() * 0.3,
    explanation: isAI
      ? "Audio exhibits consistent pitch patterns and lacks natural micro-pauses typically found in human speech. Spectral analysis indicates synthetic generation patterns."
      : "Audio shows natural pitch variations and breathing patterns consistent with authentic human speech. Micro-pauses and tonal fluctuations align with organic voice characteristics.",
  };
};

const Index = () => {
  const [state, actions] = useAppState();
  const [useMock, setUseMock] = useState(true); // Toggle for demo mode

  const handleSubmit = async (data: { audioUrl?: string; audioBase64?: string; language: string }) => {
    actions.startDetection();

    try {
      let result: DetectionResult;

      if (useMock) {
        // Use mock data for demo/testing
        result = await mockDetection();
      } else {
        // Real API call
        result = await detectVoice({
          audio_url: data.audioUrl,
          audio_base64: data.audioBase64,
          language: data.language,
        });
      }

      actions.setResult(result);
    } catch (error) {
      const apiError = error as ApiError;
      actions.setError(apiError.detail || apiError.message || "An unexpected error occurred");
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-accent/5 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full opacity-20"
          style={{ background: 'var(--gradient-glow)' }} />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-border/50 glass">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg gradient-primary glow">
              <Waves className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground glow-text">EchoTruth</h1>
              <p className="text-xs text-muted-foreground">AI Voice Detection</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setUseMock(!useMock)}
              className={useMock ? "text-warning" : "text-success"}
            >
              {useMock ? "Demo Mode" : "Live Mode"}
            </Button>
            <a
              href="https://chirag100x.github.io/Echo_Truth/
"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg hover:bg-muted transition-colors"
            >
              <Github className="w-5 h-5 text-muted-foreground hover:text-foreground" />
            </a>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="relative z-10 container mx-auto px-4 py-12">
        {/* Hero section */}
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Detect <span className="text-primary glow-text">AI-Generated</span> Voices
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Analyze audio clips to determine if they contain synthetic or authentic human speech.
            Multi-language support with real-time analysis.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {[
            { icon: ShieldCheck, title: "Accurate Detection", desc: "Advanced audio analysis using spectral features" },
            { icon: Zap, title: "Fast Processing", desc: "Results in seconds, not minutes" },
            { icon: Globe, title: "Multi-Language", desc: "Supports English, Hindi, Tamil, Telugu, Malayalam" },
          ].map((feature, i) => (
            <div
              key={i}
              className="glass glass-hover p-6 rounded-xl text-center animate-slide-up"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <feature.icon className="w-10 h-10 text-primary mx-auto mb-4" />
              <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.desc}</p>
            </div>
          ))}
        </div>

        {/* Detection interface */}
        <div className="max-w-xl mx-auto">
          {state.status === "idle" && (
            <UploadCard
              onSubmit={handleSubmit}
              isLoading={false}
            />
          )}

          {state.status === "loading" && (
            <div className="glass p-12 rounded-xl">
              <Loader text="Analyzing voice patterns..." />
            </div>
          )}

          {state.status === "success" && state.result && (
            <div className="space-y-6">
              <ResultCard result={state.result} />
              <Button
                variant="outline"
                onClick={actions.reset}
                className="w-full glass glass-hover"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Analyze Another Audio
              </Button>
            </div>
          )}

          {state.status === "error" && (
            <div className="glass p-8 rounded-xl text-center animate-fade-in">
              <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">⚠️</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">
                Detection Failed
              </h3>
              <p className="text-muted-foreground mb-6">{state.error}</p>
              <Button
                variant="outline"
                onClick={actions.reset}
                className="glass glass-hover"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </Button>
            </div>
          )}
        </div>

        {/* API info */}
        {useMock && (
          <div className="mt-12 p-4 rounded-lg bg-warning/10 border border-warning/30 max-w-xl mx-auto">
            <p className="text-sm text-warning text-center">
              <strong>Demo Mode:</strong> Results are simulated. Connect the Python backend for real detection.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border/50 mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>EchoTruth • AI Voice Detection</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;