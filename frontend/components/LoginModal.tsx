'use client';

import React, { useState } from 'react';
import { X, Lock, User } from 'lucide-react';

interface LoginModalProps {
    isOpen: boolean;
    onClose: () => void;
    onLogin: (username: string, password: string) => void;
}

export default function LoginModal({ isOpen, onClose, onLogin }: LoginModalProps) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        // Dummy credentials
        if (username === 'admin' && password === 'admin123') {
            onLogin(username, password);
            onClose();
        } else {
            setError('Invalid credentials. Use admin/admin123');
        }
        
        setIsLoading(false);
    };

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full overflow-hidden animate-in fade-in zoom-in duration-200">
                {/* Header */}
                <div className="bg-gradient-to-r from-tata-blue to-blue-600 text-white p-8 relative">
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-white hover:bg-white/20 p-2 rounded-full transition-colors"
                        aria-label="Close"
                    >
                        <X size={24} />
                    </button>
                    <div className="text-center">
                        <h2 className="text-3xl font-bold">Admin Login</h2>
                        <p className="text-blue-100 text-sm mt-2">Loan Management System</p>
                    </div>
                </div>

                {/* Body */}
                <form onSubmit={handleSubmit} className="p-8 space-y-5">
                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <div>
                        <label className="block text-gray-700 font-medium mb-2">
                            Username
                        </label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-tata-blue focus:border-tata-blue text-gray-900 placeholder:text-gray-400"
                                placeholder="Enter username"
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-gray-700 font-medium mb-2">
                            Password
                        </label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-tata-blue focus:border-tata-blue text-gray-900 placeholder:text-gray-400"
                                placeholder="Enter password"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-gradient-to-r from-tata-blue to-blue-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? 'Logging in...' : 'Login'}
                    </button>

                    <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg text-sm text-center">
                        <p className="font-semibold mb-2">Demo Credentials:</p>
                        <div className="flex justify-center gap-4 text-xs">
                            <span>Username: <span className="font-mono font-bold text-tata-blue">admin</span></span>
                            <span>Password: <span className="font-mono font-bold text-tata-blue">admin123</span></span>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
