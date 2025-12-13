# 🎭 Anam.ai AI Persona Integration - Complete Setup Guide

## ✅ What's Been Implemented

I've integrated Anam.ai's AI persona platform into your LoanAI frontend. This enables **real-time video conversations** with an AI-powered digital human that can:
- Speak and listen with natural voice
- Display facial expressions and emotions
- Understand context and provide personalized loan advice
- Operate 24/7 without human intervention

## 📁 Files Created/Modified

### New Files:
1. **`frontend/components/AnamPersona.tsx`** - Main React component for the AI persona
2. **`frontend/app/api/anam/session/route.ts`** - Backend API to securely create session tokens
3. **`frontend/app/persona/page.tsx`** - Full demo page for the AI persona
4. **`ANAM_INTEGRATION.md`** - Detailed integration documentation

### Modified Files:
1. **`frontend/app/page.tsx`** - Added prominent CTA button to access AI persona
2. **`.env`** - Added ANAM_API_KEY placeholder
3. **`frontend/package.json`** - Added @anam-ai/js-sdk dependency ✅ (installed)

## 🚀 Setup Steps

### Step 1: Get Your Anam API Key
1. Visit: https://docs.anam.ai/api-key
2. Sign up for an Anam account
3. Copy your API key

### Step 2: Configure Environment Variable
Open `.env` file and add your API key:
```bash
ANAM_API_KEY=your_actual_api_key_here
```

### Step 3: Restart Your Frontend Server
```bash
cd frontend
npm run dev
```

### Step 4: Test the Integration
1. Navigate to: http://localhost:3000
2. Click the "Try Our AI Video Advisor" button
3. Or go directly to: http://localhost:3000/persona
4. Allow microphone access when prompted
5. Start talking to Priya, your AI loan advisor!

## 🎨 Customization Options

### Change Avatar Appearance
1. Visit the Anam Lab: https://lab.anam.ai/
2. Browse 100+ avatars in different styles, genders, ages
3. Copy the avatar ID
4. Update in `frontend/app/api/anam/session/route.ts`:
```typescript
avatarId: 'your-chosen-avatar-id',
```

### Change Voice
1. Browse voices: https://docs.anam.ai/resources/voice-gallery
2. Preview 400+ voices with different accents, tones, speeds
3. Copy the voice ID
4. Update in `frontend/app/api/anam/session/route.ts`:
```typescript
voiceId: 'your-chosen-voice-id',
```

### Customize Personality & Behavior
Edit the `systemPrompt` in `frontend/app/persona/page.tsx`:
```typescript
systemPrompt={`You are [Name], a [role] at [company].

Your role is to:
- [Responsibility 1]
- [Responsibility 2]

Your communication style:
- [Style guideline 1]
- [Style guideline 2]

Remember: [Core values/principles]
`}
```

### Adjust Session Duration
In `frontend/app/api/anam/session/route.ts`:
```typescript
maxSessionLengthSeconds: 1800, // 30 minutes (change as needed)
```

## 🎯 Features Included

### 1. Real-time Video Avatar
- AI-powered digital human with facial expressions
- Natural lip-sync with speech
- Professional appearance

### 2. Voice Interaction
- Automatic speech-to-text (user speech)
- Natural text-to-speech (AI responses)
- Real-time conversation flow

### 3. Session Management
- Secure token-based authentication
- Configurable session duration
- Auto-reconnect on disconnect

### 4. Event Handling
- Connection status monitoring
- Speaking/listening indicators
- Error handling with retry

### 5. UI Controls
- Mute/unmute microphone
- Start/stop session
- Status indicators
- Loading states

## 🔧 Component Architecture

```
┌─────────────────────────────────────────┐
│         User Browser                     │
│  ┌───────────────────────────────┐      │
│  │  AnamPersona Component        │      │
│  │  - Video element              │      │
│  │  - Controls (mute, stop)      │      │
│  │  - Status display             │      │
│  └───────────────────────────────┘      │
│           │                              │
│           ▼                              │
│  ┌───────────────────────────────┐      │
│  │  @anam-ai/js-sdk              │      │
│  │  - WebRTC connection          │      │
│  │  - Audio/video streaming      │      │
│  │  - Event listeners            │      │
│  └───────────────────────────────┘      │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│    Your Next.js Backend                 │
│  ┌───────────────────────────────┐      │
│  │  /api/anam/session            │      │
│  │  - Creates session token      │      │
│  │  - Keeps API key secure       │      │
│  └───────────────────────────────┘      │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│      Anam.ai Platform                   │
│  - AI model (GPT-4.1 Mini)              │
│  - Avatar rendering                     │
│  - Voice synthesis                      │
│  - Speech recognition                   │
└─────────────────────────────────────────┘
```

## 💡 Use Cases

1. **Customer Support**: Answer loan queries 24/7
2. **Lead Qualification**: Screen potential customers
3. **Product Education**: Explain loan products interactively
4. **Document Guidance**: Help with application process
5. **EMI Calculation**: Provide instant loan calculations

## 🔒 Security Notes

- ✅ API key stored server-side (not exposed to browser)
- ✅ Session tokens used for client-side (temporary, secure)
- ✅ HTTPS required for production (WebRTC requirement)
- ✅ Configurable session timeouts
- ✅ No sensitive data stored in conversations

## 📊 Pricing Considerations

Anam.ai pricing is based on:
- **Session duration** (per minute of conversation)
- **Number of concurrent sessions**
- Different tiers available (Starter, Pro, Enterprise)

**Tip**: Use `maxSessionLengthSeconds` to control costs.

## 🐛 Troubleshooting

### "Failed to create session token"
**Cause**: Missing or invalid API key
**Solution**: 
- Check `.env` has correct `ANAM_API_KEY`
- Restart frontend server after adding key
- Verify key is valid at Anam dashboard

### "Microphone access denied"
**Cause**: Browser blocked microphone
**Solution**: 
- Click the lock icon in browser address bar
- Allow microphone access
- Refresh the page

### Connection fails to establish
**Causes**:
- Network/firewall blocking WebRTC
- Browser doesn't support WebRTC
**Solutions**:
- Try a different browser (Chrome, Edge, Firefox recommended)
- Check firewall settings
- Ensure using HTTPS in production

### Avatar doesn't appear
**Cause**: Session token creation failed
**Solution**: 
- Check browser console for errors
- Verify API key is correct
- Check network tab for API errors

### No sound from AI
**Cause**: Browser audio policy
**Solution**: 
- Click anywhere on the page to enable audio
- Check browser volume settings
- Verify autoplay is allowed

## 🌐 Browser Compatibility

| Browser | Supported | Notes |
|---------|-----------|-------|
| Chrome  | ✅ Yes    | Recommended |
| Edge    | ✅ Yes    | Recommended |
| Firefox | ✅ Yes    | Good |
| Safari  | ⚠️ Partial | Some WebRTC limitations |
| Mobile Safari | ⚠️ Partial | Requires user interaction |
| Mobile Chrome | ✅ Yes | Good performance |

## 🚀 Production Deployment

### Requirements:
1. **HTTPS**: Mandatory for microphone access and WebRTC
2. **Environment Variables**: Set `ANAM_API_KEY` in your hosting platform
3. **CORS**: Ensure API routes allow requests from your domain

### Recommended Hosts:
- Vercel (easy Next.js deployment)
- Netlify
- AWS Amplify
- Railway

### Deployment Checklist:
- [ ] Add `ANAM_API_KEY` to environment variables
- [ ] Enable HTTPS
- [ ] Test microphone permissions
- [ ] Configure session timeout
- [ ] Test on mobile devices
- [ ] Monitor usage/costs

## 📚 Additional Resources

- **Anam Docs**: https://docs.anam.ai/
- **Quickstart**: https://docs.anam.ai/quickstart
- **Persona Concepts**: https://docs.anam.ai/concepts/personas
- **Avatar Gallery**: https://docs.anam.ai/resources/avatar-gallery
- **Voice Gallery**: https://docs.anam.ai/resources/voice-gallery
- **Playground**: https://lab.anam.ai/

## 🎉 What's Next?

### Advanced Features to Explore:
1. **Knowledge Base**: Upload company docs for context-aware responses
2. **Tool Calling**: Integrate with your backend APIs for real actions
3. **Custom LLMs**: Use your own AI models
4. **Multi-language**: Support different languages
5. **Analytics**: Track conversation metrics
6. **Custom Avatars**: Create branded avatars (Enterprise)

### Integration Ideas:
- Embed in chat widget
- Add to specific product pages
- Create appointment booking flow
- Integrate with CRM
- Add document upload/verification

## 📞 Support

If you have questions:
1. Check the documentation: https://docs.anam.ai/
2. Join Anam community/Discord
3. Contact Anam support

---

**Status**: ✅ Ready to use after adding API key
**Estimated Setup Time**: 5-10 minutes
**Difficulty**: Easy 🟢
