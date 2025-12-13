
'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ChatWindow from '@/components/ChatWindow';
import StatusPanel from '@/components/StatusPanel';
import { Loader2 } from 'lucide-react';

function ChatContent() {
    const searchParams = useSearchParams();
    const sessionId = searchParams.get('session_id');
    const userId = searchParams.get('user_id');

    const [state, setState] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const fetchState = async () => {
        if (!sessionId || !userId) return;
        try {
            const response = await axios.get(`http://localhost:8000/api/state/${sessionId}?user_id=${userId}`);
            setState(response.data.state);
        } catch (error) {
            console.error('Error fetching state:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchState();
        // Poll for state updates every 5 seconds
        const interval = setInterval(fetchState, 5000);
        return () => clearInterval(interval);
    }, [sessionId, userId]);

    if (!sessionId || !userId) {
        return <div className="p-8 text-center text-red-600">Invalid Session</div>;
    }

    if (loading && !state) {
        return (
            <div className="flex justify-center items-center h-[600px]">
                <Loader2 size={48} className="animate-spin text-tata-blue" />
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
                <ChatWindow
                    sessionId={sessionId}
                    userId={userId}
                    onStateUpdate={fetchState}
                />
            </div>
            <div className="lg:col-span-1">
                <StatusPanel state={state} />
            </div>
        </div>
    );
}

export default function ChatPage() {
    return (
        <div className="min-h-screen flex flex-col bg-gray-50">
            <Header />
            <main className="flex-1 container mx-auto px-4 py-8">
                <Suspense fallback={<div className="text-center p-8">Loading...</div>}>
                    <ChatContent />
                </Suspense>
            </main>
            <Footer />
        </div>
    );
}
