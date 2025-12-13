'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Loader2, Mic, MicOff, Video, VideoOff } from 'lucide-react';

interface AnamPersonaProps {
    personaName?: string;
    systemPrompt?: string;
    autoStart?: boolean;
}

export default function AnamPersona({ 
    personaName = 'Priya',
    systemPrompt = 'You are Priya, a helpful loan advisor at Tata Capital. You assist customers with loan inquiries, provide information about loan products, and guide them through the loan application process. Be friendly, professional, and concise in your responses.',
    autoStart = true 
}: AnamPersonaProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [status, setStatus] = useState('Initializing...');
    const [isLoading, setIsLoading] = useState(true);
    const [isConnected, setIsConnected] = useState(false);
    const [isMuted, setIsMuted] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [anamClient, setAnamClient] = useState<any>(null);

    const createSessionToken = async () => {
        try {
            const response = await fetch('/api/anam/session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    personaName,
                    systemPrompt,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to create session token');
            }

            const data = await response.json();
            return data.sessionToken;
        } catch (err) {
            console.error('Error creating session token:', err);
            throw err;
        }
    };

    const startPersona = async () => {
        try {
            setIsLoading(true);
            setStatus('Creating session...');
            setError(null);

            const sessionToken = await createSessionToken();
            setStatus('Connecting to persona...');

            // Dynamically import the Anam SDK
            const { createClient } = await import('@anam-ai/js-sdk');
            
            const client = createClient(sessionToken);
            
            // Listen to events
            client.addListener('connectionEstablished', () => {
                setStatus('Connected! Start speaking...');
                setIsConnected(true);
                setIsLoading(false);
            });

            client.addListener('personaSpeakingStarted', () => {
                setStatus('Priya is speaking...');
            });

            client.addListener('personaSpeakingEnded', () => {
                setStatus('Listening...');
            });

            client.addListener('connectionClosed', () => {
                setStatus('Connection closed');
                setIsConnected(false);
            });

            client.addListener('error', (error: any) => {
                console.error('Anam client error:', error);
                setError(error.message || 'An error occurred');
                setIsLoading(false);
            });

            // Stream to video element
            if (videoRef.current) {
                await client.streamToVideoElement('persona-video');
            }

            setAnamClient(client);
        } catch (err: any) {
            console.error('Failed to start persona:', err);
            setError(err.message || 'Failed to start persona. Please check your configuration.');
            setStatus('Failed to connect');
            setIsLoading(false);
        }
    };

    const stopPersona = () => {
        if (anamClient) {
            anamClient.stopStreaming();
            setAnamClient(null);
            setIsConnected(false);
            setStatus('Disconnected');
        }
    };

    const toggleMute = () => {
        if (anamClient) {
            if (isMuted) {
                anamClient.unmute();
            } else {
                anamClient.mute();
            }
            setIsMuted(!isMuted);
        }
    };

    useEffect(() => {
        if (autoStart) {
            startPersona();
        }

        return () => {
            stopPersona();
        };
    }, []);

    return (
        <div className="flex flex-col items-center justify-center gap-4 p-6 bg-white rounded-lg shadow-lg">
            <div className="w-full max-w-2xl">
                <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
                    AI Loan Advisor - {personaName}
                </h2>

                {/* Video Container */}
                <div className="relative w-full aspect-video bg-gray-900 rounded-lg overflow-hidden">
                    <video
                        id="persona-video"
                        ref={videoRef}
                        autoPlay
                        playsInline
                        className="w-full h-full object-cover"
                    />

                    {/* Loading Overlay */}
                    {isLoading && (
                        <div className="absolute inset-0 flex items-center justify-center bg-gray-900/80">
                            <div className="flex flex-col items-center gap-4">
                                <Loader2 size={48} className="animate-spin text-tata-blue" />
                                <p className="text-white text-lg">{status}</p>
                            </div>
                        </div>
                    )}

                    {/* Error Overlay */}
                    {error && (
                        <div className="absolute inset-0 flex items-center justify-center bg-red-900/80">
                            <div className="flex flex-col items-center gap-4 p-6 text-center">
                                <p className="text-white text-lg font-semibold">Error</p>
                                <p className="text-white">{error}</p>
                                <button
                                    onClick={startPersona}
                                    className="px-6 py-2 bg-white text-red-900 rounded-lg hover:bg-gray-100 transition-colors"
                                >
                                    Retry
                                </button>
                            </div>
                        </div>
                    )}
                </div>

                {/* Status Bar */}
                <div className="mt-4 p-3 bg-gray-100 rounded-lg">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
                            <span className="text-sm text-gray-700">{status}</span>
                        </div>

                        {/* Controls */}
                        <div className="flex gap-2">
                            {isConnected && (
                                <>
                                    <button
                                        onClick={toggleMute}
                                        className="p-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition-colors"
                                        title={isMuted ? 'Unmute' : 'Mute'}
                                    >
                                        {isMuted ? <MicOff size={20} /> : <Mic size={20} />}
                                    </button>
                                    <button
                                        onClick={stopPersona}
                                        className="p-2 rounded-lg bg-red-100 hover:bg-red-200 transition-colors text-red-600"
                                        title="End Session"
                                    >
                                        <VideoOff size={20} />
                                    </button>
                                </>
                            )}

                            {!isConnected && !isLoading && !error && (
                                <button
                                    onClick={startPersona}
                                    className="px-4 py-2 rounded-lg bg-tata-blue hover:bg-blue-700 text-white transition-colors flex items-center gap-2"
                                >
                                    <Video size={20} />
                                    Start Session
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                {/* Instructions */}
                <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <h3 className="font-semibold text-blue-900 mb-2">How to use:</h3>
                    <ul className="text-sm text-blue-800 space-y-1">
                        <li>• Allow microphone access when prompted</li>
                        <li>• Speak naturally to ask questions about loans</li>
                        <li>• The AI advisor will respond with voice and video</li>
                        <li>• You can mute or end the session anytime</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
