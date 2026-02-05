/**
 * UploadCard.tsx
 * Main input component for audio upload/URL
 * Handles file selection and URL input with validation
 */

import { useState, useRef } from "react";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LanguageSelector } from "./LanguageSelector";
import { Upload, Link, Play, X, FileAudio } from "lucide-react";

interface UploadCardProps {
  onSubmit: (data: { audioUrl?: string; audioBase64?: string; language: string }) => void;
  isLoading: boolean;
  className?: string;
}

export function UploadCard({ onSubmit, isLoading, className }: UploadCardProps) {
  const [audioUrl, setAudioUrl] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("en");
  const [activeTab, setActiveTab] = useState("url");
  const [error, setError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateUrl = (url: string): boolean => {
    try {
      new URL(url);
      return url.match(/\.(mp3|wav|ogg|m4a|webm)(\?.*)?$/i) !== null || 
             url.includes("audio") ||
             url.includes("mp3");
    } catch {
      return false;
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("audio/")) {
        setError("Please select an audio file (MP3, WAV, etc.)");
        return;
      }
      if (file.size > 50 * 1024 * 1024) { // 50MB limit
        setError("File size must be less than 50MB");
        return;
      }
      setSelectedFile(file);
      setError("");
    }
  };

  const handleSubmit = async () => {
    setError("");

    if (activeTab === "url") {
      if (!audioUrl.trim()) {
        setError("Please enter an audio URL");
        return;
      }
      if (!validateUrl(audioUrl)) {
        setError("Please enter a valid audio URL (mp3, wav, ogg, m4a)");
        return;
      }
      onSubmit({ audioUrl, language });
    } else {
      if (!selectedFile) {
        setError("Please select an audio file");
        return;
      }
      
      // Convert file to base64
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = (reader.result as string).split(",")[1];
        onSubmit({ audioBase64: base64, language });
      };
      reader.onerror = () => {
        setError("Failed to read file");
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <Card className={cn("glass glow animate-fade-in", className)}>
      <CardHeader>
        <CardTitle className="flex items-center gap-3 text-xl">
          <div className="p-2 rounded-lg gradient-primary">
            <FileAudio className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="text-foreground">Analyze Voice</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-6">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="w-full bg-muted/50">
            <TabsTrigger 
              value="url" 
              className="flex-1 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
            >
              <Link className="w-4 h-4 mr-2" />
              URL
            </TabsTrigger>
            <TabsTrigger 
              value="upload"
              className="flex-1 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
            >
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </TabsTrigger>
          </TabsList>

          <TabsContent value="url" className="mt-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">
                Audio URL
              </label>
              <Input
                type="url"
                placeholder="https://example.com/audio.mp3"
                value={audioUrl}
                onChange={(e) => setAudioUrl(e.target.value)}
                disabled={isLoading}
                className="glass glass-hover font-mono text-sm"
              />
              <p className="text-xs text-muted-foreground">
                Supported formats: MP3, WAV, OGG, M4A, WebM
              </p>
            </div>
          </TabsContent>

          <TabsContent value="upload" className="mt-4">
            <div className="space-y-4">
              <input
                ref={fileInputRef}
                type="file"
                accept="audio/*"
                onChange={handleFileSelect}
                className="hidden"
                disabled={isLoading}
              />
              
              {selectedFile ? (
                <div className="flex items-center gap-3 p-4 rounded-lg bg-muted/50 border border-border/50">
                  <FileAudio className="w-8 h-8 text-primary" />
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-foreground truncate">
                      {selectedFile.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={clearFile}
                    disabled={isLoading}
                    className="hover:bg-destructive/10 hover:text-destructive"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ) : (
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className={cn(
                    "w-full p-8 rounded-lg border-2 border-dashed transition-all duration-300",
                    "border-border/50 hover:border-primary/50 hover:bg-primary/5",
                    "flex flex-col items-center gap-3",
                    isLoading && "opacity-50 cursor-not-allowed"
                  )}
                >
                  <Upload className="w-10 h-10 text-muted-foreground" />
                  <div className="text-center">
                    <p className="font-medium text-foreground">
                      Click to upload audio
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      MP3, WAV, OGG up to 50MB
                    </p>
                  </div>
                </button>
              )}
            </div>
          </TabsContent>
        </Tabs>

        {/* Language selector */}
        <LanguageSelector
          value={language}
          onChange={setLanguage}
          disabled={isLoading}
        />

        {/* Error message */}
        {error && (
          <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {/* Submit button */}
        <Button
          onClick={handleSubmit}
          disabled={isLoading}
          className="w-full gradient-primary text-primary-foreground font-semibold h-12 text-base hover:opacity-90 transition-opacity"
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
              Analyzing...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <Play className="w-5 h-5" />
              Detect Voice Type
            </span>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}

export default UploadCard;
