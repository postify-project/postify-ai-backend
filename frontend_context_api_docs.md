# Postify Context API - Frontend Documentation

This document provides examples and expected payloads for the new `/api/ai/context` endpoints.

## 1. Get Onboarding Questions
**Endpoint:** `GET /api/ai/context/questions`

Fetches the list of questions to ask the user during onboarding. The `type` field tells you what kind of input to render (e.g., text box vs. dropdown select).

**Example Response:**
```json
[
  {
    "id": "accountType",
    "question": "What is your account type?",
    "options": [
      "Influencer / Creator",
      "Brand / Business",
      "Personal"
    ],
    "type": "select"
  },
  {
    "id": "brandName",
    "question": "What is your brand or creator name?",
    "options": null,
    "type": "text"
  }
  // ... more questions
]
```

---

## 2. Get User Context
**Endpoint:** `GET /api/ai/context/`

Fetches the currently saved context for the user.

**Example Response:**
```json
{
  "accountType": "Influencer / Creator",
  "brandDescription": "social media automation",
  "brandName": "postify",
  "brandTagline": "automate your social media",
  "contentFormat": "Text Threads & Short Tips",
  "creatorNiche": "Software Development & AI",
  "creatorPersona": "The Curious Builder (Raw & Behind-the-Scenes)",
  "emojiRule": "Minimal (1-2 total in caption)",
  "hashtags": "#buildinpublic #indiehackers #postify",
  "imageryStyle": "Real Photography & Clean",
  "industry": "B2B SaaS & Tech",
  "keywords": "saas, nextjs, ai tools, webdev",
  "logoUrl": "",
  "primaryCTA": "DM me 'GROWTH' to start",
  "primaryColor": "#8b5cf6",
  "secondaryColor": "#ec4899",
  "tone": "Professional & Corporate",
  "website": ""
}
```

---

## 3. Update User Context
**Endpoint:** `POST /api/ai/context/`

Use this endpoint to save the user's answers. You don't have to send all fields; just send the fields you want to update.

**Example Request Payload:**
```json
{
  "accountType": "Brand / Business",
  "brandName": "Postify AI",
  "primaryColor": "#000000"
}
```

**Example Response (Returns the fully updated context object):**
```json
{
  "accountType": "Brand / Business",
  "brandDescription": "social media automation",
  "brandName": "Postify AI",
  // ... rest of the fields
  "primaryColor": "#000000"
}
```
