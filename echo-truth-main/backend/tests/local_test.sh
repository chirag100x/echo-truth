#!/bin/bash
# ============================================
# EchoTruth - Local Testing Script
# ============================================
# Run this script to test the API locally
# Make sure the backend is running first:
#   uvicorn app.main:app --reload
# ============================================

# Configuration
API_URL="http://localhost:8000"
API_KEY="demo-key-12345"  # Replace with your API key

# Sample audio URLs for testing
# These are public domain audio samples
SAMPLE_MP3="https://www2.cs.uic.edu/~i101/SoundFiles/BaachRecordingPiano.mp3"

echo "============================================"
echo "EchoTruth API Test Suite"
echo "============================================"
echo ""

# Test 1: Health check
echo "1. Testing health endpoint..."
curl -s "${API_URL}/health" | python3 -m json.tool
echo ""

# Test 2: Root endpoint
echo "2. Testing root endpoint..."
curl -s "${API_URL}/" | python3 -m json.tool
echo ""

# Test 3: Detection with audio URL
echo "3. Testing detection with audio URL..."
echo "   URL: ${SAMPLE_MP3}"
echo ""
curl -s -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"audio_url\": \"${SAMPLE_MP3}\",
    \"language\": \"en\"
  }" | python3 -m json.tool
echo ""

# Test 4: Test missing auth (should fail with 401)
echo "4. Testing missing authorization (expecting 401)..."
curl -s -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -d "{
    \"audio_url\": \"${SAMPLE_MP3}\",
    \"language\": \"en\"
  }" | python3 -m json.tool
echo ""

# Test 5: Test missing audio (should fail with 400)
echo "5. Testing missing audio (expecting 400)..."
curl -s -X POST "${API_URL}/api/v1/detect" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"language\": \"en\"
  }" | python3 -m json.tool
echo ""

echo "============================================"
echo "Tests completed!"
echo "============================================"
