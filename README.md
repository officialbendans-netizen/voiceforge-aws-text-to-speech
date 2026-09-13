# 🎙️ VoiceForge — Serverless Text-to-Speech Application

A fully serverless text-to-speech web application built entirely on AWS. Type any text, choose from multiple neural voices, and hear it spoken instantly in your browser — no servers, no infrastructure to manage, zero downtime.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange?style=flat-square&logo=amazon-aws)
![Lambda](https://img.shields.io/badge/AWS-Lambda-orange?style=flat-square)
![Polly](https://img.shields.io/badge/Amazon-Polly-blue?style=flat-square)
![S3](https://img.shields.io/badge/Amazon-S3-green?style=flat-square)
![API Gateway](https://img.shields.io/badge/API-Gateway-purple?style=flat-square)

---

## 🌟 Live Demo

> Hosted on Amazon S3 Static Website Hosting — accessible from any browser worldwide.

---

## 🎯 What It Does

VoiceForge converts written text into natural-sounding human speech using Amazon Polly's neural voice engine. Users simply:

1. **Type or paste** any text into the input box
2. **Choose a voice** — Joanna, Matthew, Amy or Brian
3. **Click Convert** — Amazon Polly processes the text
4. **Listen instantly** — audio plays directly in the browser
5. **Download** the MP3 file for offline use

**Real world use cases:**
- 📚 Audiobook generation
- ♿ Accessibility tools for visually impaired users
- 🎓 E-learning and educational content
- 📢 Voice announcements and notifications
- 🌍 Multilingual content delivery

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Browser (S3 Static Frontend)       │
│  User types text → selects voice → clicks   │
│  Convert → audio player appears in browser  │
└──────────────────┬──────────────────────────┘
                   │ HTTP POST (JSON)
                   ▼
┌─────────────────────────────────────────────┐
│         Amazon API Gateway (REST API)        │
│  Receives request → triggers Lambda         │
│  Handles CORS → routes to backend           │
└──────────────────┬──────────────────────────┘
                   │ Invoke
                   ▼
┌─────────────────────────────────────────────┐
│           AWS Lambda (Python 3.12)           │
│  Validates input → calls Amazon Polly        │
│  Saves MP3 to S3 → returns public URL       │
└────────┬─────────────────────┬──────────────┘
         │ SynthesizeSpeech    │ PutObject
         ▼                     ▼
┌──────────────────┐  ┌───────────────────────┐
│  Amazon Polly    │  │  Amazon S3            │
│  Neural TTS      │  │  Audio Output Bucket  │
│  Returns MP3     │  │  Stores MP3 files     │
└──────────────────┘  └───────────────────────┘
```

---

## ☁️ AWS Services Used

| Service | Purpose | Why This Service |
|---|---|---|
| **Amazon S3** | Frontend hosting + audio file storage | Durable, scalable, serverless — perfect for static sites and file storage |
| **AWS Lambda** | Serverless backend logic | No servers to manage — runs only when called — pay per execution |
| **Amazon API Gateway** | REST API endpoint | Managed, scalable API front door — handles auth, routing and CORS |
| **Amazon Polly** | Neural text-to-speech engine | AWS native AI — 60+ voices — neural engine for natural sound |
| **AWS IAM** | Secure permissions between services | Least privilege — Lambda only gets access to what it needs |
| **Amazon CloudWatch** | Logging and monitoring | Real-time logs — debug Lambda executions — set alarms |

---

## ✨ Features

- 🎙️ **Neural voice quality** — powered by Amazon Polly's neural engine
- 👥 **4 voice options** — Joanna (Female US), Matthew (Male US), Amy (Female UK), Brian (Male UK)
- 🔊 **In-browser playback** — audio player loads automatically after conversion
- ⬇️ **MP3 download** — save audio file for offline use
- 📝 **3000 character limit** — with live character counter
- ⚡ **Fast conversion** — typically under 3 seconds
- 📊 **Conversion counter** — tracks how many conversions in the session
- 🆓 **AWS Free Tier** — runs within free tier limits
- 🔒 **Fully serverless** — zero server management

---

## 📁 Project Structure

```
voiceforge-aws-text-to-speech/
│
├── frontend/
│   └── index.html                  # Complete single-file frontend
│                                   # HTML + CSS + JavaScript
│
├── lambda/
│   ├── lambda_api.py               # API Gateway handler
│   │                               # Handles browser requests
│   └── lambda_s3_trigger.py        # S3 event trigger handler
│                                   # Processes text files uploaded to S3
│
├── architecture/
│   └── architecture.md             # Detailed architecture documentation
│
└── README.md
```

---

## 🚀 How to Deploy — Step by Step

### Prerequisites
- AWS Account (Free Tier works perfectly)
- AWS Console access
- Basic understanding of AWS services

---

### Step 1 — Create S3 Buckets

Create **two S3 buckets** in us-east-1:

**Bucket 1 — Text Input (Private)**
```
Name: tts-text-input-{yourname}
Block all public access: ON
Versioning: Enable
Encryption: SSE-S3
```

**Bucket 2 — Audio Output (Public)**
```
Name: tts-audio-output-{yourname}
Block all public access: OFF (uncheck all)
Add bucket policy — replace {yourname}:
```
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::tts-audio-output-{yourname}/*"
        }
    ]
}
```

---

### Step 2 — Create Lambda Function

```
Name: text-to-speech-api
Runtime: Python 3.12
Architecture: x86_64
Timeout: 60 seconds
```

**Attach these IAM policies to the Lambda role:**
```
AmazonPollyFullAccess
AmazonS3FullAccess
CloudWatchLogsFullAccess
```

Paste code from `lambda/lambda_api.py`

---

### Step 3 — Create API Gateway

```
Type: REST API
Name: text-to-speech-api
Endpoint: Regional
```

**Create resource and method:**
```
Resource: /convert
Method: POST
Integration: Lambda function (with proxy integration)
Lambda: text-to-speech-api
CORS: Enable on /convert
```

**Deploy:**
```
Stage name: prod
```

**Copy the Invoke URL** — you will need it for the frontend.

---

### Step 4 — Update Frontend

Open `frontend/index.html` and find this line:

```javascript
const API_URL = 'YOUR_API_GATEWAY_URL/prod/convert';
```

Replace with your actual Invoke URL:

```javascript
const API_URL = 'https://abc123.execute-api.us-east-1.amazonaws.com/prod/convert';
```

---

### Step 5 — Host Frontend on S3

```
Name: voiceforge-frontend-{yourname}
Block all public access: OFF
Enable static website hosting: ON
Index document: index.html
```

Add public read bucket policy then upload `index.html`.

Your app is now live at the S3 website endpoint URL! 🎉

---

## 🔧 How It Works — Technical Details

### Text Conversion Flow

1. User submits text via POST request to API Gateway
2. API Gateway invokes Lambda with the request body
3. Lambda validates text length (max 3000 characters)
4. Lambda calls `polly.synthesize_speech()` with neural engine
5. Polly returns an audio stream in MP3 format
6. Lambda saves the MP3 to S3 output bucket with a UUID filename
7. Lambda returns the public S3 URL to the frontend
8. Frontend sets the audio player source to the URL and auto-plays

### Voice Options

| Voice ID | Name | Gender | Accent | Engine |
|---|---|---|---|---|
| Joanna | Joanna | Female | American English | Neural |
| Matthew | Matthew | Male | American English | Neural |
| Amy | Amy | Female | British English | Neural |
| Brian | Brian | Male | British English | Neural |

### Error Handling
- Empty text → 400 Bad Request
- Text over 3000 chars → 400 Bad Request
- Polly or S3 failure → 500 Internal Server Error with error message
- All errors logged to CloudWatch for debugging

---

## 🐛 Common Issues and Fixes

| Issue | Cause | Fix |
|---|---|---|
| CORS error in browser | CORS not enabled on API Gateway | Enable CORS on /convert resource and redeploy |
| Something went wrong | Nested JSON response not parsed | Check API returns body as string — parse twice |
| AccessDeniedException Polly | Lambda missing Polly permission | Add AmazonPollyFullAccess to Lambda IAM role |
| AccessDeniedException S3 | Lambda missing S3 permission | Add AmazonS3FullAccess to Lambda IAM role |
| Audio not playing | Output bucket not public | Add public read policy to audio output bucket |

---

## 🧠 What I Learned Building This

- **Serverless architecture** — designing systems with zero server management
- **AWS Lambda** — writing Python functions triggered by API Gateway
- **Amazon Polly** — integrating neural text-to-speech AI into applications
- **API Gateway** — building and deploying REST APIs with CORS
- **S3 static hosting** — hosting web applications without a web server
- **IAM permissions** — securing service-to-service access with least privilege
- **CloudWatch** — debugging and monitoring serverless applications
- **Real-world debugging** — fixing CORS, nested JSON, permission errors

---

## 📈 Cost Estimate (Free Tier)

| Service | Free Tier | Typical Usage |
|---|---|---|
| Lambda | 1M requests/month free | Very low cost |
| API Gateway | 1M calls/month free | Very low cost |
| Amazon Polly | 5M characters/month free | Very low cost |
| S3 | 5GB storage free | Very low cost |
| **Total** | **Within free tier** | **~$0/month** |

---

## 🔮 Future Improvements

- [ ] Add more languages — French, Spanish, German, Swahili
- [ ] Add Amazon Cognito user authentication
- [ ] Store conversion history in DynamoDB
- [ ] Add SSML support for advanced speech control
- [ ] Add CloudFront CDN for faster global delivery
- [ ] Add custom domain with Route 53

---

## 👨‍💻 Author

**Benjamin Asare Danquah**
- 🏆 AWS Certified Cloud Practitioner
- 🌍 Based in Ghana, West Africa
- 💼 GitHub: [@officialbendans-netizen](https://github.com/officialbendans-netizen)
- ☁️ Preparing for AWS Solutions Architect Associate

---

## 📄 License

MIT License — feel free to use, modify and share.

---

*This is Project 1 of my AWS Cloud Portfolio — building real serverless applications while preparing for the AWS Solutions Architect Associate certification.*
