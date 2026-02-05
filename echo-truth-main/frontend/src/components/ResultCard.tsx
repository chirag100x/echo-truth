/**
 * ResultCard.tsx
 * Displays AI detection results with confidence meter
 * Shows classification, confidence score, and explanation
 */

import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bot, User, AlertTriangle, CheckCircle2 } from "lucide-react";

export interface DetectionResult {
  classification: "AI_GENERATED" | "HUMAN";
  confidence: number;
  explanation: string;
}

interface ResultCardProps {
  result: DetectionResult;
  className?: string;
}

export function ResultCard({ result, className }: ResultCardProps) {
  const isAI = result.classification === "AI_GENERATED";
  const confidencePercent = Math.round(result.confidence * 100);
  
  // Determine confidence level for styling
  const getConfidenceLevel = () => {
    if (result.confidence >= 0.8) return "high";
    if (result.confidence >= 0.6) return "medium";
    return "low";
  };
  
  const confidenceLevel = getConfidenceLevel();

  return (
    <Card className={cn(
      "glass overflow-hidden animate-scale-in",
      isAI ? "border-warning/50" : "border-success/50",
      className
    )}>
      {/* Colored top bar */}
      <div className={cn(
        "h-1 w-full",
        isAI ? "bg-warning" : "bg-success"
      )} />
      
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center justify-between">
          <span className="text-lg font-semibold text-foreground">
            Detection Result
          </span>
          {isAI ? (
            <AlertTriangle className="w-5 h-5 text-warning" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-success" />
          )}
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Classification badge */}
        <div className="flex items-center gap-4">
          <div className={cn(
            "p-4 rounded-xl",
            isAI ? "bg-warning/10" : "bg-success/10"
          )}>
            {isAI ? (
              <Bot className={cn("w-10 h-10", "text-warning")} />
            ) : (
              <User className={cn("w-10 h-10", "text-success")} />
            )}
          </div>
          
          <div className="flex-1">
            <p className={cn(
              "text-2xl font-bold",
              isAI ? "text-warning" : "text-success"
            )}>
              {isAI ? "AI Generated" : "Human Voice"}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              {isAI 
                ? "This audio appears to be synthetically generated"
                : "This audio appears to be authentic human speech"
              }
            </p>
          </div>
        </div>

        {/* Confidence meter */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-muted-foreground">
              Confidence Score
            </span>
            <span className={cn(
              "text-lg font-bold font-mono",
              confidenceLevel === "high" && (isAI ? "text-warning" : "text-success"),
              confidenceLevel === "medium" && "text-primary",
              confidenceLevel === "low" && "text-muted-foreground"
            )}>
              {confidencePercent}%
            </span>
          </div>
          
          {/* Progress bar */}
          <div className="h-3 bg-muted rounded-full overflow-hidden">
            <div 
              className={cn(
                "h-full rounded-full transition-all duration-1000 ease-out",
                isAI ? "bg-warning" : "bg-success"
              )}
              style={{ width: `${confidencePercent}%` }}
            />
          </div>
          
          {/* Confidence label */}
          <p className="text-xs text-muted-foreground text-right">
            {confidenceLevel === "high" && "High confidence"}
            {confidenceLevel === "medium" && "Moderate confidence"}
            {confidenceLevel === "low" && "Low confidence - results may vary"}
          </p>
        </div>

        {/* Explanation */}
        <div className="p-4 rounded-lg bg-muted/50 border border-border/50">
          <p className="text-sm font-medium text-muted-foreground mb-2">
            Analysis
          </p>
          <p className="text-foreground leading-relaxed">
            {result.explanation}
          </p>
        </div>

        {/* Technical note */}
        <p className="text-xs text-muted-foreground text-center">
          Analysis based on pitch variance, silence patterns, and audio characteristics
        </p>
      </CardContent>
    </Card>
  );
}

export default ResultCard;
