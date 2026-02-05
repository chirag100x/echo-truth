/**
 * Loader.tsx
 * Animated loading spinner with scanning effect
 * Used during audio analysis
 */

import { cn } from "@/lib/utils";

interface LoaderProps {
  className?: string;
  text?: string;
}

export function Loader({ className, text = "Analyzing audio..." }: LoaderProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center gap-6", className)}>
      {/* Waveform visualization */}
      <div className="relative w-32 h-32">
        {/* Outer ring */}
        <div className="absolute inset-0 rounded-full border-2 border-primary/20 animate-pulse" />
        
        {/* Middle ring with rotation */}
        <div className="absolute inset-2 rounded-full border-2 border-primary/40 animate-spin" 
             style={{ animationDuration: '3s' }} />
        
        {/* Inner glowing core */}
        <div className="absolute inset-4 rounded-full gradient-primary opacity-30 animate-pulse-glow" />
        
        {/* Center waveform bars */}
        <div className="absolute inset-0 flex items-center justify-center gap-1">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="w-1.5 bg-primary rounded-full"
              style={{
                height: '20px',
                animation: `waveform 1s ease-in-out ${i * 0.1}s infinite`,
              }}
            />
          ))}
        </div>
        
        {/* Scanning line */}
        <div className="absolute inset-0 overflow-hidden rounded-full">
          <div className="w-full h-1 gradient-primary animate-scan" />
        </div>
      </div>

      {/* Loading text */}
      <div className="flex flex-col items-center gap-2">
        <p className="text-foreground font-medium">{text}</p>
        <div className="flex gap-1">
          {[...Array(3)].map((_, i) => (
            <span
              key={i}
              className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"
              style={{ animationDelay: `${i * 0.2}s` }}
            />
          ))}
        </div>
      </div>

      <style>{`
        @keyframes waveform {
          0%, 100% { height: 10px; }
          50% { height: 30px; }
        }
      `}</style>
    </div>
  );
}

export default Loader;
