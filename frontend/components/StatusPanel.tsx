
import React from 'react';
import { CheckCircle, Clock, AlertCircle, FileText, CreditCard, UserCheck, Download } from 'lucide-react';
import clsx from 'clsx';
import axios from 'axios';

interface StatusPanelProps {
    state: any;
    sessionId?: string;
    userId?: string;
}

export default function StatusPanel({ state, sessionId, userId }: StatusPanelProps) {
    if (!state) return null;

    const handleDownloadSanctionLetter = async () => {
        if (!sessionId || !userId) return;
        
        try {
            const response = await axios.get(
                `http://localhost:8000/api/download-sanction-letter/${sessionId}?user_id=${userId}`,
                { responseType: 'blob' }
            );
            
            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `sanction_letter_${state.sanction_letter?.sanction_reference || 'document'}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error downloading sanction letter:', error);
            alert('Failed to download sanction letter. Please try again.');
        }
    };

    const steps = [
        {
            id: 'kyc',
            label: 'KYC Verification',
            icon: UserCheck,
            status: state.kyc_verified ? 'completed' : 'pending',
        },
        {
            id: 'eligibility',
            label: 'Credit Check',
            icon: CreditCard,
            status: state.credit_score ? 'completed' : 'pending',
            details: state.credit_score ? `Score: ${state.credit_score}` : null,
        },
        {
            id: 'approval',
            label: 'Loan Approval',
            icon: CheckCircle,
            status: state.application_status === 'APPROVED' || state.application_status === 'SANCTION_GENERATED' ? 'completed' : (state.application_status === 'REJECTED' ? 'error' : 'pending'),
        },
        {
            id: 'sanction',
            label: 'Sanction Letter',
            icon: FileText,
            status: state.sanction_letter?.sanction_reference ? 'completed' : 'pending',
        },
    ];

    return (
        <div className="bg-white rounded-lg shadow-lg p-6 h-full border border-gray-100">
            <h2 className="text-xl font-bold text-gray-800 mb-6 border-b pb-2">Application Status</h2>

            {/* Customer Info Card */}
            <div className="bg-blue-50 rounded-md p-4 mb-6">
                <h3 className="text-sm font-semibold text-tata-blue mb-2">Applicant Details</h3>
                <div className="text-sm text-gray-700">
                    <p><span className="font-medium">Name:</span> {state.customer_name}</p>
                    <p><span className="font-medium">ID:</span> {state.customer_id}</p>
                    {state.pre_approved_limit && (
                        <p className="mt-2 text-green-700 font-medium">
                            Pre-approved Limit: ₹{state.pre_approved_limit.toLocaleString()}
                        </p>
                    )}
                </div>
            </div>

            {/* Progress Steps */}
            <div className="space-y-6">
                {steps.map((step, index) => (
                    <div key={step.id} className="flex gap-4">
                        <div className="flex flex-col items-center">
                            <div className={clsx(
                                "w-8 h-8 rounded-full flex items-center justify-center z-10",
                                step.status === 'completed' ? "bg-green-100 text-green-600" :
                                    step.status === 'error' ? "bg-red-100 text-red-600" :
                                        "bg-gray-100 text-gray-400"
                            )}>
                                <step.icon size={16} />
                            </div>
                            {index < steps.length - 1 && (
                                <div className={clsx(
                                    "w-0.5 h-full mt-2",
                                    step.status === 'completed' ? "bg-green-200" : "bg-gray-100"
                                )} />
                            )}
                        </div>
                        <div className="pb-6">
                            <h4 className={clsx(
                                "font-medium text-sm",
                                step.status === 'completed' ? "text-gray-900" : "text-gray-500"
                            )}>
                                {step.label}
                            </h4>
                            {step.details && (
                                <p className="text-xs text-gray-500 mt-1">{step.details}</p>
                            )}
                            {step.status === 'completed' && (
                                <span className="text-xs text-green-600 flex items-center gap-1 mt-1">
                                    <CheckCircle size={10} /> Completed
                                </span>
                            )}
                            {step.status === 'error' && (
                                <span className="text-xs text-red-600 flex items-center gap-1 mt-1">
                                    <AlertCircle size={10} /> Rejected
                                </span>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Sanction Letter Download */}
            {state.sanction_letter?.sanction_reference && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
                    <p className="text-green-800 font-medium mb-2">🎉 Loan Sanctioned!</p>
                    <p className="text-sm text-gray-600 mb-3">
                        Reference: {state.sanction_letter.sanction_reference}
                    </p>
                    <button 
                        onClick={handleDownloadSanctionLetter}
                        className="bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2 w-full"
                    >
                        <Download size={16} />
                        Download Sanction Letter
                    </button>
                </div>
            )}
        </div>
    );
}
