# 🚀 Quick Start - Anam.ai AI Persona

## ⚡ 3-Step Setup

### 1️⃣ Get API Key
Visit: https://docs.anam.ai/api-key

### 2️⃣ Add to .env
```bash
ANAM_API_KEY=your_actual_api_key_here
```

### 3️⃣ Restart & Test
```bash
cd frontend
npm run dev
```

Navigate to: http://localhost:3000/persona

---

## ✅ Checklist

- [ ] Got Anam API key
- [ ] Added key to `.env` file  
- [ ] Restarted frontend server
- [ ] Tested at `/persona` page
- [ ] Allowed microphone access
- [ ] Successfully chatted with AI

---

## 🎯 Access Points

**Main Homepage**: http://localhost:3000
- Click "Try Our AI Video Advisor" button

**Direct Access**: http://localhost:3000/persona

---

## 🎨 Quick Customization

### Change Avatar
1. Visit https://lab.anam.ai/
2. Copy avatar ID
3. Edit `frontend/app/api/anam/session/route.ts`

### Change Voice  
1. Browse https://docs.anam.ai/resources/voice-gallery
2. Copy voice ID
3. Edit `frontend/app/api/anam/session/route.ts`

### Change Personality
Edit `systemPrompt` in `frontend/app/persona/page.tsx`

---

## 🐛 Common Issues

**Problem**: "Failed to create session token"
**Fix**: Check `ANAM_API_KEY` in `.env` and restart

**Problem**: "Microphone access denied"  
**Fix**: Click browser's permission icon and allow microphone

**Problem**: No video appears
**Fix**: Check browser console for errors, verify API key

---

## 📊 Files Modified

✅ `frontend/components/AnamPersona.tsx` (new)
✅ `frontend/app/api/anam/session/route.ts` (new)  
✅ `frontend/app/persona/page.tsx` (new)
✅ `frontend/app/page.tsx` (updated with CTA)
✅ `.env` (added ANAM_API_KEY)
✅ Package installed: `@anam-ai/js-sdk`

---

## 📚 Documentation

Full Setup Guide: `ANAM_SETUP_COMPLETE.md`
Integration Docs: `ANAM_INTEGRATION.md`
Official Docs: https://docs.anam.ai/

---

**Status**: 🟢 Ready (just need API key!)
