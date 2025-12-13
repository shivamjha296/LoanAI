
import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Upload, Paperclip } from 'lucide-react';
import clsx from 'clsx';
import axios from 'axios';
import AnimatedAvatar from './AnimatedAvatar';

interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}

interface ChatWindowProps {
    sessionId: string;
    userId: string;
    onStateUpdate: () => void;
}

export default function ChatWindow({ sessionId, userId, onStateUpdate }: ChatWindowProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [uploadingFile, setUploadingFile] = useState(false);
    const [showWelcome, setShowWelcome] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        // Hide welcome screen on first message
        if (showWelcome) {
            setShowWelcome(false);
        }

        const userMessage: Message = {
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/api/chat', {
                session_id: sessionId,
                user_id: userId,
                message: userMessage.content,
            });

            const assistantMessage: Message = {
                role: 'assistant',
                content: response.data.response,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, assistantMessage]);
            onStateUpdate(); // Refresh state after interaction
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage: Message = {
                role: 'system',
                content: "Sorry, I encountered an error. Please try again.",
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

        setUploadingFile(true);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post(
                `http://localhost:8000/api/upload-salary-slip?session_id=${sessionId}&user_id=${userId}`,
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
                role: 'user',
                content: uploadMessage,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, userMessage]);

            // Process the file with the agent
            const chatResponse = await axios.post('http://localhost:8000/api/chat', {
                session_id: sessionId,
                user_id: userId,
                message: uploadMessage,
            });

            const assistantMessage: Message = {
                role: 'assistant',
                content: chatResponse.data.response,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, assistantMessage]);
            onStateUpdate();
        } catch (error) {
            console.error('Error uploading file:', error);
            const errorMessage: Message = {
                role: 'system',
                content: "Sorry, there was an error uploading your file. Please try again.",
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
        <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden">
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-tata-blue to-blue-600 text-white p-4 flex items-center gap-3 shadow-md">
                <div className="relative">
                    <div className="bg-white/20 p-2 rounded-full backdrop-blur-sm">
                        <Bot size={24} />
                    </div>
                    <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse" />
                </div>
                <div>
                    <h3 className="font-bold text-lg">Priya Sharma</h3>
                    <p className="text-xs text-blue-100">Your Loan Manager • Online</p>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
                {/* Welcome Screen with Animated Avatar */}
                {showWelcome && messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full space-y-6 animate-fade-in">
                        <AnimatedAvatar size="lg" showGreeting={true} />
                        
                        <div className="bg-white rounded-xl shadow-lg p-6 max-w-md border border-gray-100">
                            <p className="text-gray-700 leading-relaxed text-center">
                                Welcome! I'm here to help you with your personal loan journey. 
                                Whether you need funds for travel, medical expenses, weddings, or any other purpose, 
                                I'll guide you through every step.
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
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
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
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t border-gray-100">
                <div className="flex gap-2">
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
                        className="bg-gray-100 text-gray-600 p-2 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Upload Salary Slip"
                    >
                        {uploadingFile ? (
                            <Loader2 size={20} className="animate-spin" />
                        ) : (
                            <Paperclip size={20} />
                        )}
                    </button>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your message here..."
                        className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-tata-blue focus:border-transparent"
                        disabled={isLoading || uploadingFile}
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading || !input.trim() || uploadingFile}
                        className="bg-tata-red text-white p-2 rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send size={20} />
                    </button>
                </div>
                {uploadingFile && (
                    <p className="text-xs text-gray-500 mt-2">Uploading file...</p>
                )}
            </div>
        </div>
    );
}
