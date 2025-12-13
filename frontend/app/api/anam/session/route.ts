import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    try {
        const { personaName, systemPrompt } = await request.json();

        // Get Anam API key from environment variables
        const anamApiKey = process.env.ANAM_API_KEY;

        if (!anamApiKey) {
            return NextResponse.json(
                { error: 'Anam API key not configured' },
                { status: 500 }
            );
        }

        // Create session token with Anam API
        const response = await fetch('https://api.anam.ai/v1/auth/session-token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${anamApiKey}`,
            },
            body: JSON.stringify({
                personaConfig: {
                    name: personaName || 'Rakesh',
                    // Avatar ID - Custom avatar
                    avatarId: '6cc28442-cccd-42a8-b6e4-24b7210a09c5',
                    // Voice ID - Custom voice
                    voiceId: '79abfccb-e83b-4ad4-9d80-f8d3e6e3141d',
                    // LLM ID - GPT-4.1 Mini for fast, cost-effective responses
                    llmId: '0934d97d-0c3a-4f33-91b0-5e136a0ef466',
                    systemPrompt: systemPrompt || 'You are a helpful AI assistant.',
                    // Optional: Set max session length (in seconds)
                    maxSessionLengthSeconds: 1800, // 30 minutes
                },
            }),
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error('Anam API error:', errorData);
            return NextResponse.json(
                { error: 'Failed to create session token', details: errorData },
                { status: response.status }
            );
        }

        const data = await response.json();
        return NextResponse.json({ sessionToken: data.sessionToken });
    } catch (error: any) {
        console.error('Error creating Anam session:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}
