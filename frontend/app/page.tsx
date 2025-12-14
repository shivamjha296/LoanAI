
'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import LoginModal from '@/components/LoginModal';
import { User, CreditCard, MapPin, ArrowRight, Loader2, AlertCircle, Video } from 'lucide-react';
import clsx from 'clsx';
import Link from 'next/link';
import { Customer } from '@/types';
import { API_ENDPOINTS } from '@/lib/config';

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [initializing, setInitializing] = useState<string | null>(null);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const router = useRouter();

  const handleLogin = (username: string, password: string) => {
    // Store admin session
    localStorage.setItem('adminLoggedIn', 'true');
    router.push('/admin');
  };

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axios.get(API_ENDPOINTS.customers);
        setCustomers(response.data);
        setError(null);
      } catch (error) {
        console.error('Error fetching customers:', error);
        setError('Failed to load customers. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const handleSelectCustomer = async (customerId: string) => {
    setInitializing(customerId);
    try {
      const response = await axios.post(API_ENDPOINTS.session, {
        customer_id: customerId,
      });
      const { session_id, customer_id } = response.data;
      // Use the customer_id returned from backend to ensure case consistency
      router.push(`/chat?session_id=${session_id}&user_id=${customer_id || customerId}`);
    } catch (error) {
      console.error('Error initializing session:', error);
      setError('Failed to start session. Please try again.');
      setInitializing(null);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header onLoginClick={() => setIsLoginModalOpen(true)} />
      <LoginModal 
        isOpen={isLoginModalOpen} 
        onClose={() => setIsLoginModalOpen(false)}
        onLogin={handleLogin}
      />

      <main className="flex-1 container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to <span className="text-tata-blue">Tata Capital</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Experience our AI-powered personal loan assistant. Select a profile below to start your journey.
          </p>
          
          {/* AI Persona CTA */}
          <div className="mt-6">
            <Link 
              href="/persona"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-tata-blue to-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              <Video size={20} />
              Try Our AI Video Advisor
              <ArrowRight size={20} />
            </Link>
            <p className="text-sm text-gray-500 mt-2">
              Experience real-time video conversations with our AI loan advisor
            </p>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 size={48} className="animate-spin text-tata-blue" />
          </div>
        ) : error ? (
          <div className="max-w-md mx-auto bg-red-50 border border-red-200 text-red-600 p-6 rounded-lg flex items-center gap-3">
            <AlertCircle size={24} />
            <div>
              <p className="font-medium">{error}</p>
              <button 
                onClick={() => window.location.reload()} 
                className="text-sm underline mt-2"
              >
                Reload Page
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 px-8 md:px-12 lg:px-16">
            {customers.map((customer) => (
              <div
                key={customer.id}
                className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-gray-200 group hover:scale-105 hover:-translate-y-2 hover:border-tata-blue"
              >
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="bg-blue-50 p-3 rounded-full text-tata-blue group-hover:bg-tata-blue group-hover:text-white transition-colors">
                      <User size={24} />
                    </div>
                    <span className={clsx(
                      "px-3 py-1 rounded-full text-xs font-bold",
                      customer.credit_score >= 750 ? "bg-green-100 text-green-700" :
                        customer.credit_score >= 700 ? "bg-yellow-100 text-yellow-700" :
                          "bg-red-100 text-red-700"
                    )}>
                      Score: {customer.credit_score}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-gray-800 mb-2">{customer.name}</h3>

                  <div className="space-y-2 text-sm text-gray-600 mb-6">
                    <div className="flex items-center gap-2">
                      <MapPin size={16} className="text-gray-400" />
                      <span>{customer.city}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CreditCard size={16} className="text-gray-400" />
                      <span>Salary: ₹{customer.monthly_salary.toLocaleString()}</span>
                    </div>
                    <div className="mt-2 pt-2 border-t border-gray-100">
                      <p className="text-xs text-gray-500 uppercase font-semibold">Pre-approved Limit</p>
                      <p className="text-lg font-bold text-tata-blue">₹{customer.pre_approved_limit.toLocaleString()}</p>
                    </div>
                  </div>

                  <button
                    onClick={() => handleSelectCustomer(customer.id)}
                    disabled={initializing === customer.id}
                    className="w-full bg-white border-2 border-tata-blue text-tata-blue hover:bg-tata-blue hover:text-white py-2 rounded-lg font-semibold transition-all flex items-center justify-center gap-2"
                  >
                    {initializing === customer.id ? (
                      <>
                        <Loader2 size={18} className="animate-spin" />
                        Starting...
                      </>
                    ) : (
                      <>
                        Start Application <ArrowRight size={18} />
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
