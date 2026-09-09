# VoiceForge — Architecture Details

## Overview
VoiceForge is a fully serverless application with zero server management.

## Flow
1. User opens web app hosted on S3
2. User types text and selects a voice
3. Frontend sends POST request to API Gateway
4. API Gateway triggers Lambda function
5. Lambda sends text to Amazon Polly
6. Polly returns MP3 audio stream
7. Lambda saves MP3 to S3 output bucket
8. Lambda returns public S3 URL to frontend
9. Frontend plays audio in browser

## Services
- Amazon S3 — Frontend + Audio storage
- AWS Lambda — Backend logic
- Amazon API Gateway — REST API
- Amazon Polly — Neural TTS Engine
- AWS IAM — Permissions
- Amazon CloudWatch — Logging

## Cost
Runs entirely on AWS Free Tier
