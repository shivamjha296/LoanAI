import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Upload, Paperclip, Mic, MicOff, Volume2, VolumeX, Globe } from 'lucide-react';
import clsx from 'clsx';
import axios from 'axios';
import Image from 'next/image';
import AnimatedAvatar from './AnimatedAvatar';
import { Message } from '@/types';
import { API_ENDPOINTS } from '@/lib/config';

interface ChatWindowProps {
    sessionId: string;
    userId: string;
    onStateUpdate: () => void;
    customerName?: string;
}

type Language = {
    code: string;
    name: string;
    label: string;
};

const LANGUAGES: Language[] = [
    { code: 'en-US', name: 'English', label: 'English' },
    { code: 'hi-IN', name: 'Hindi', label: 'हिंदी' },
    { code: 'mr-IN', name: 'Marathi', label: 'मराठी' },
    { code: 'gu-IN', name: 'Gujarati', label: 'ગુજરાતી' },
    { code: 'bn-IN', name: 'Bengali', label: 'বাংলা' },
    { code: 'ta-IN', name: 'Tamil', label: 'தமிழ்' },
    { code: 'te-IN', name: 'Telugu', label: 'తెలుగు' },
    { code: 'kn-IN', name: 'Kannada', label: 'ಕನ್ನಡ' },
    { code: 'ml-IN', name: 'Malayalam', label: 'മലയാളം' },
];

export default function ChatWindow({ sessionId, userId, onStateUpdate, customerName }: ChatWindowProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [uploadingFile, setUploadingFile] = useState(false);
    const [showWelcome, setShowWelcome] = useState(true);
    const [selectedLanguage, setSelectedLanguage] = useState<Language>(LANGUAGES[0]);
    const [isListening, setIsListening] = useState(false);
    const [autoSpeak, setAutoSpeak] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);

    const scrollContainerRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const recognitionRef = useRef<any>(null);
    const synthRef = useRef<SpeechSynthesis | null>(null);

    const scrollToBottom = () => {
        if (scrollContainerRef.current) {
            const { scrollHeight, clientHeight } = scrollContainerRef.current;
            scrollContainerRef.current.scrollTo({
                top: scrollHeight - clientHeight,
                behavior: 'smooth'
            });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Initialize Speech Synthesis
    useEffect(() => {
        if (typeof window !== 'undefined') {
            synthRef.current = window.speechSynthesis;
        }
    }, []);

    // Initialize Speech Recognition
    useEffect(() => {
        if (typeof window !== 'undefined') {
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = selectedLanguage.code;

                recognition.onstart = () => setIsListening(true);
                recognition.onend = () => setIsListening(false);
                recognition.onerror = (event: any) => {
                    console.error('Speech recognition error', event.error);
                    setIsListening(false);
                };
                recognition.onresult = (event: any) => {
                    const transcript = event.results[0][0].transcript;
                    setInput(transcript);
                    // Optional: Auto-send if confident? Better to let user review.
                };

                recognitionRef.current = recognition;
            }
        }
    }, [selectedLanguage]);

    const toggleListening = () => {
        if (!recognitionRef.current) {
            alert('Speech recognition is not supported in this browser.');
            return;
        }

        if (isListening) {
            recognitionRef.current.stop();
        } else {
            recognitionRef.current.start();
        }
    };

    const speakText = (text: string) => {
        if (!synthRef.current) return;

        // Stop any current speaking
        synthRef.current.cancel();

        if (!autoSpeak && !isSpeaking) return; // Only speak if autoSpeak is on or manually triggered (logic below)

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = selectedLanguage.code;

        // Try to find a voice matching the language
        const voices = synthRef.current.getVoices();
        const voice = voices.find(v => v.lang.includes(selectedLanguage.code.split('-')[0]));
        if (voice) utterance.voice = voice;

        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);

        synthRef.current.speak(utterance);
    };

    const stopSpeaking = () => {
        if (synthRef.current) {
            synthRef.current.cancel();
            setIsSpeaking(false);
        }
    };

    const toggleAutoSpeak = () => {
        if (isSpeaking) stopSpeaking();
        setAutoSpeak(!autoSpeak);
    };

    // Auto-speak new assistant messages
    useEffect(() => {
        const lastMessage = messages[messages.length - 1];
        if (autoSpeak && lastMessage && lastMessage.role === 'assistant') {
            speakText(lastMessage.content);
        }
    }, [messages, autoSpeak]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        // Hide welcome screen on first message
        if (showWelcome) {
            setShowWelcome(false);
        }

        const userMessage: Message = {
            id: `${Date.now()}-${Math.random()}`,
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post(API_ENDPOINTS.chat, {
                session_id: sessionId,
                user_id: userId,
                message: userMessage.content,
                language: selectedLanguage.name,
            });

            const assistantMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'assistant',
                content: response.data.response,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, assistantMessage]);
            onStateUpdate(); // Refresh state after interaction
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'system',
                content: axios.isAxiosError(error)
                    ? `Connection error: ${error.message}. Please check your connection.`
                    : "Sorry, I encountered an error. Please try again.",
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Validate file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            const errorMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'system',
                content: "File size exceeds 10MB limit. Please upload a smaller file.",
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
            if (fileInputRef.current) fileInputRef.current.value = '';
            return;
        }

        // Validate file type
        const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            const errorMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'system',
                content: "Invalid file type. Please upload a PDF, JPG, or PNG file.",
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
            if (fileInputRef.current) fileInputRef.current.value = '';
            return;
        }

        setUploadingFile(true);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post(
                API_ENDPOINTS.uploadSalarySlip(sessionId, userId),
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            // Automatically send message to agent about the uploaded file
            const uploadMessage = response.data.message || `I uploaded my salary slip at ${response.data.file_path}`;

            const userMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'user',
                content: uploadMessage,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, userMessage]);

            // Process the file with the agent
            const chatResponse = await axios.post(API_ENDPOINTS.chat, {
                session_id: sessionId,
                user_id: userId,
                message: uploadMessage,
                language: selectedLanguage.name,
            });

            const assistantMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'assistant',
                content: chatResponse.data.response,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, assistantMessage]);
            onStateUpdate();
        } catch (error) {
            console.error('Error uploading file:', error);
            const errorMessage: Message = {
                id: `${Date.now()}-${Math.random()}`,
                role: 'system',
                content: axios.isAxiosError(error)
                    ? `Upload failed: ${error.message}. Please try again.`
                    : "Sorry, there was an error uploading your file. Please try again.",
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setUploadingFile(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    return (
        <div className="flex flex-col h-[85vh] min-h-[600px] bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden">
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-tata-blue to-blue-600 text-white p-3 flex items-center justify-between shadow-md">
                <div className="flex items-center gap-3">
                    <div className="relative">
                        <div className="bg-white/20 p-2 rounded-full backdrop-blur-sm">
                            <Image src="/Tia-icon.svg" alt="TIA" width={32} height={32} className="w-8 h-8" />
                        </div>
                        <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse" />
                    </div>
                    <div>
                        <h3 className="font-bold text-lg">TIA</h3>
                        <p className="text-xs text-blue-100">
                            {customerName ? `Helping ${customerName}` : 'Your Loan Assistant'} • Online
                        </p>
                    </div>
                </div>

                {/* Language & Voice Controls */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={toggleAutoSpeak}
                        className={clsx(
                            "p-2 rounded-full transition-colors",
                            autoSpeak ? "bg-white/20 text-white" : "text-blue-100 hover:bg-white/10"
                        )}
                        title={autoSpeak ? "Turn off text-to-speech" : "Turn on text-to-speech"}
                    >
                        {autoSpeak ? <Volume2 size={20} /> : <VolumeX size={20} />}
                    </button>

                    <div className="relative group">
                        <button className="flex items-center gap-1 bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-full transition-colors text-sm">
                            <Globe size={16} />
                            <span>{selectedLanguage.label}</span>
                        </button>

                        <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-100 py-1 hidden group-hover:block z-20">
                            {LANGUAGES.map((lang) => (
                                <button
                                    key={lang.code}
                                    onClick={() => setSelectedLanguage(lang)}
                                    className={clsx(
                                        "w-full text-left px-4 py-2 text-sm hover:bg-gray-50 transition-colors",
                                        selectedLanguage.code === lang.code ? "text-tata-blue font-bold bg-blue-50" : "text-gray-700"
                                    )}
                                >
                                    {lang.name} ({lang.label})
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Messages Area */}
            <div
                ref={scrollContainerRef}
                className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth relative"
                style={{
                    backgroundImage: 'url(/wallpaper.jpeg)',
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                }}
            >
                {/* Light overlay to make background lighter */}
                <div className="absolute inset-0 bg-white/70 -z-10"></div>
                {/* Welcome Screen with Animated Avatar */}
                {showWelcome && messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full space-y-6 animate-fade-in">
                        <AnimatedAvatar size="lg" showGreeting={true} />

                        <div className="bg-white rounded-xl shadow-lg p-6 max-w-md border border-gray-100">
                            <p className="text-gray-700 leading-relaxed text-center">
                                Welcome! I'm TIA, your personal loan assistant. I'll help you find the perfect loan for your needs.
                            </p>
                            <div className="mt-4 pt-4 border-t border-gray-100">
                                <p className="text-sm text-gray-500 text-center">
                                    💬 Type a message below to get started
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Chat Messages */}
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={clsx(
                            "flex gap-3 max-w-[80%]",
                            msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                        )}
                    >
                        <div className={clsx(
                            "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                            msg.role === 'user' ? "bg-gray-200 text-gray-600" : "bg-tata-blue text-white"
                        )}>
                            {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className={clsx(
                            "p-3 rounded-lg text-sm leading-relaxed shadow-sm whitespace-pre-wrap",
                            msg.role === 'user'
                                ? "bg-tata-blue text-white rounded-tr-none"
                                : msg.role === 'system'
                                    ? "bg-red-50 text-red-600 border border-red-100"
                                    : "bg-white text-gray-800 border border-gray-100 rounded-tl-none"
                        )}>
                            {msg.content}
                            {msg.role === 'assistant' && (
                                <button
                                    onClick={() => speakText(msg.content)}
                                    className="ml-2 inline-block opacity-50 hover:opacity-100 transition-opacity"
                                    title="Read aloud"
                                >
                                    <Volume2 size={14} />
                                </button>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex gap-3 mr-auto max-w-[80%]">
                        <div className="w-8 h-8 rounded-full bg-tata-blue text-white flex items-center justify-center shrink-0">
                            <Bot size={16} />
                        </div>
                        <div className="bg-white p-3 rounded-lg rounded-tl-none border border-gray-100 shadow-sm flex items-center gap-2">
                            <Loader2 size={16} className="animate-spin text-tata-blue" />
                            <span className="text-xs text-gray-500">Thinking...</span>
                        </div>
                    </div>
                )}
            </div>

            {/* Input Area */}
            <div className="p-4 bg-transparent">
                <div className="flex gap-3 items-center">
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        accept=".pdf,.jpg,.jpeg,.png"
                        className="hidden"
                    />
                    <button
                        onClick={() => fileInputRef.current?.click()}
                        disabled={isLoading || uploadingFile}
                        className="bg-white text-tata-blue p-3 rounded-full hover:bg-blue-50 transition-all shadow-sm border border-gray-200 hover:border-tata-blue disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Upload Salary Slip"
                        aria-label="Upload Salary Slip"
                    >
                        {uploadingFile ? (
                            <Loader2 size={20} className="animate-spin" />
                        ) : (
                            <Paperclip size={20} />
                        )}
                    </button>

                    <div className="flex-1 relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={`Type your message in ${selectedLanguage.name}...`}
                            className="w-full border-2 border-tata-blue/30 rounded-full pl-5 pr-12 py-3 focus:outline-none focus:border-tata-blue focus:shadow-lg focus:shadow-tata-blue/10 text-gray-900 placeholder-gray-400 bg-white transition-all"
                            disabled={isLoading || uploadingFile}
                            aria-label="Type your message"
                        />
                        <button
                            onClick={toggleListening}
                            className={clsx(
                                "absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full transition-all",
                                isListening ? "bg-red-100 text-red-600 animate-pulse" : "text-gray-400 hover:text-tata-blue hover:bg-blue-50"
                            )}
                            title={isListening ? "Stop listening" : "Start voice input"}
                            disabled={isLoading || uploadingFile}
                        >
                            {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                        </button>
                    </div>

                    <button
                        onClick={handleSend}
                        disabled={isLoading || !input.trim() || uploadingFile}
                        className="bg-gradient-to-r from-tata-blue to-blue-600 text-white p-3 rounded-full hover:shadow-lg hover:shadow-tata-blue/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        aria-label="Send message"
                    >
                        <Send size={20} />
                    </button>
                </div>
                {uploadingFile && (
                    <p className="text-xs text-gray-500 mt-2">Uploading file...</p>
                )}
                {isListening && (
                    <p className="text-xs text-tata-blue mt-2 animate-pulse">Listening ({selectedLanguage.name})...</p>
                )}
            </div>
        </div>
    );
}
