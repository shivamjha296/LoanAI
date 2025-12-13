'use client';

import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import AnamPersona from '@/components/AnamPersona';

export default function PersonaPage() {
    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-blue-50">
            <Header />
            <main className="flex-1 container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">
                            Meet Your AI Loan Advisor
                        </h1>
                        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                            Experience the future of loan assistance with our AI-powered virtual advisor.
                            Get instant answers to your questions about personal loans, eligibility, and more.
                        </p>
                    </div>

                    <AnamPersona 
                        personaName="Rakesh Kumar"
                        systemPrompt={`You are Rakesh Kumar, a professional and friendly loan advisor at Tata Capital. 
                        
Your role is to:
- Help customers understand loan products (personal loans, home loans, car loans)
- Explain eligibility criteria and documentation requirements
- Guide customers through the application process
- Answer questions about interest rates, EMIs, and loan terms
- Provide personalized loan recommendations based on customer needs

Your communication style:
- Be warm, professional, and approachable
- Use simple language to explain financial concepts
- Ask clarifying questions to understand customer needs
- Keep responses concise (under 50 words unless explaining complex topics)
- Show empathy for customer concerns
- If you don't know specific details, acknowledge it and offer to connect them with a specialist

Remember: You represent Tata Capital's values of trust, transparency, and customer-first service.`}
                        autoStart={true}
                    />

                    {/* Additional Info Section */}
                    <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white p-6 rounded-lg shadow-md">
                            <h3 className="font-semibold text-lg text-gray-800 mb-2">
                                🎯 24/7 Availability
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Get instant assistance anytime, anywhere. No waiting in queues or call holds.
                            </p>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-md">
                            <h3 className="font-semibold text-lg text-gray-800 mb-2">
                                🧠 AI-Powered Intelligence
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Powered by advanced AI to understand your needs and provide personalized recommendations.
                            </p>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-md">
                            <h3 className="font-semibold text-lg text-gray-800 mb-2">
                                🔒 Secure & Private
                            </h3>
                            <p className="text-gray-600 text-sm">
                                Your conversations are encrypted and private. We prioritize your data security.
                            </p>
                        </div>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}
