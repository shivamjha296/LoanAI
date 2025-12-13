# Anam.ai Integration for LoanAI

This directory contains the integration with Anam.ai's AI persona platform, enabling video-based AI conversations.

## Setup Instructions

### 1. Get Your Anam API Key
Visit https://docs.anam.ai/api-key to get your API key.

### 2. Add API Key to Environment
Add your API key to the `.env` file in the root directory:
```
ANAM_API_KEY=your_anam_api_key_here
```

### 3. Install Dependencies
```bash
cd frontend
npm install @anam-ai/js-sdk
```

### 4. Run the Application
```bash
npm run dev
```

### 5. Access the AI Persona
Navigate to: http://localhost:3000/persona

## Features

- **Real-time Video Avatar**: AI-powered digital human with facial expressions
- **Voice Interaction**: Natural voice conversations with speech-to-text and text-to-speech
- **Customizable Persona**: Configure name, appearance, voice, and personality
- **Session Management**: Secure token-based sessions with configurable duration
- **Event Handling**: React to speaking, listening, and connection events

## Components

### AnamPersona Component
Located at: `frontend/components/AnamPersona.tsx`

Props:
- `personaName` (optional): Name of the AI persona
- `systemPrompt` (optional): Personality and behavior instructions
- `autoStart` (optional): Whether to start the session automatically

### API Route
Located at: `frontend/app/api/anam/session/route.ts`

Handles secure session token creation using your API key.

### Demo Page
Located at: `frontend/app/persona/page.tsx`

Full-featured demo page showcasing the AI persona.

## Customization

### Change Avatar
Visit https://lab.anam.ai/ to browse available avatars and get avatar IDs.
Update the `avatarId` in `frontend/app/api/anam/session/route.ts`.

### Change Voice
Browse the voice gallery at https://docs.anam.ai/resources/voice-gallery
Update the `voiceId` in `frontend/app/api/anam/session/route.ts`.

### Customize Personality
Modify the `systemPrompt` in the AnamPersona component or in the persona page.

## Session Configuration

Default session length: 30 minutes
To change, modify `maxSessionLengthSeconds` in the API route.

## Browser Requirements

- Modern browser with WebRTC support
- Microphone access permission
- HTTPS (for production)

## Troubleshooting

### "Failed to create session token"
- Check that your ANAM_API_KEY is set correctly in .env
- Verify the API key is valid at https://docs.anam.ai/

### "Microphone access denied"
- Allow microphone permissions in your browser
- Check browser security settings

### Connection issues
- Ensure you're on a secure connection (HTTPS in production)
- Check network/firewall settings
- Verify WebRTC is supported in your browser

## Documentation

Full Anam.ai documentation: https://docs.anam.ai/
