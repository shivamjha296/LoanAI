'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Users, CreditCard, Database, TrendingUp, LogOut, Menu, X } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '@/lib/config';

type TableType = 'customers' | 'offers' | 'kyc' | 'credit';

export default function AdminPage() {
    const [selectedTable, setSelectedTable] = useState<TableType>('customers');
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const router = useRouter();

    useEffect(() => {
        // Check if admin is logged in
        const isLoggedIn = localStorage.getItem('adminLoggedIn');
        if (!isLoggedIn) {
            router.push('/');
        }
    }, [router]);

    useEffect(() => {
        fetchData(selectedTable);
    }, [selectedTable]);

    const fetchData = async (table: TableType) => {
        setLoading(true);
        try {
            console.log('Fetching from:', `${API_BASE_URL}/api/admin/${table}`);
            const response = await axios.get(`${API_BASE_URL}/api/admin/${table}`);
            console.log('Response data:', response.data);
            setData(response.data);
        } catch (error: any) {
            console.error('Error fetching data:', error);
            console.error('Error details:', error.response?.status, error.response?.data);
            setData([]);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('adminLoggedIn');
        router.push('/');
    };

    const menuItems = [
        { id: 'customers' as TableType, label: 'Customer Database', icon: Users, description: 'Synthetic customer data' },
        { id: 'offers' as TableType, label: 'Offer Mart', icon: CreditCard, description: 'Pre-approved loan offers' },
        { id: 'kyc' as TableType, label: 'CRM Server', icon: Database, description: 'Customer KYC data' },
        { id: 'credit' as TableType, label: 'Credit Bureau', icon: TrendingUp, description: 'Credit scores & history' },
    ];

    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar */}
            <aside className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-gradient-to-b from-gray-900 to-gray-800 text-white transition-all duration-300 overflow-hidden flex flex-col`}>
                {/* Logo Section */}
                <div className="p-6 border-b border-gray-700">
                    <div className="flex items-center gap-3">
                        <div className="bg-tata-blue p-2 rounded-lg">
                            <Database size={24} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold">Loan Admin</h1>
                            <p className="text-xs text-gray-400">Loan Management</p>
                        </div>
                    </div>
                </div>

                {/* Menu Items */}
                <nav className="flex-1 p-4 space-y-2">
                    {menuItems.map((item) => {
                        const Icon = item.icon;
                        return (
                            <button
                                key={item.id}
                                onClick={() => setSelectedTable(item.id)}
                                className={`w-full flex items-start gap-3 p-3 rounded-lg transition-all ${
                                    selectedTable === item.id
                                        ? 'bg-tata-blue text-white shadow-lg'
                                        : 'hover:bg-gray-700 text-gray-300'
                                }`}
                            >
                                <Icon size={20} className="mt-0.5 flex-shrink-0" />
                                <div className="text-left">
                                    <div className="font-medium text-sm">{item.label}</div>
                                    <div className="text-xs opacity-75">{item.description}</div>
                                </div>
                            </button>
                        );
                    })}
                </nav>

                {/* Admin User Section */}
                <div className="p-4 border-t border-gray-700">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 rounded-full bg-tata-blue flex items-center justify-center font-bold">
                            A
                        </div>
                        <div className="flex-1">
                            <p className="font-medium text-sm">Admin User</p>
                            <p className="text-xs text-gray-400">Loan Administrator</p>
                        </div>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium"
                    >
                        <LogOut size={16} />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <header className="bg-white shadow-sm border-b border-gray-200">
                    <div className="px-6 py-4 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() => setSidebarOpen(!sidebarOpen)}
                                className="p-2 hover:bg-gray-100 rounded-lg"
                                aria-label="Toggle sidebar"
                            >
                                {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
                            </button>
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">
                                    {menuItems.find(item => item.id === selectedTable)?.label}
                                </h2>
                                <p className="text-sm text-gray-500">
                                    {menuItems.find(item => item.id === selectedTable)?.description}
                                </p>
                            </div>
                        </div>
                        <div className="text-right">
                            <p className="text-sm font-medium text-tata-blue">Tata Capital Admin</p>
                        </div>
                    </div>
                </header>

                {/* Content Area */}
                <main className="flex-1 p-6 overflow-auto">
                    {loading ? (
                        <div className="flex items-center justify-center h-64">
                            <div className="animate-spin rounded-full h-12 w-12 border-4 border-tata-blue border-t-transparent"></div>
                        </div>
                    ) : (
                        <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                            {selectedTable === 'customers' && <CustomersTable data={data} />}
                            {selectedTable === 'offers' && <OffersTable data={data} />}
                            {selectedTable === 'kyc' && <KYCTable data={data} />}
                            {selectedTable === 'credit' && <CreditTable data={data} />}
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}

// Table Components
function CustomersTable({ data }: { data: any[] }) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-800 to-gray-700 text-white">
                    <tr>
                        <th className="px-6 py-4 text-left text-sm font-semibold">ID</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Customer Name</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Age</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">City</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Credit Score</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Pre-approved Limit</th>
                        <th className="px-6 py-4 text-center text-sm font-semibold">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {data.map((customer, index) => (
                        <tr key={customer.id || index} className="hover:bg-blue-50 transition-colors">
                            <td className="px-6 py-4 text-sm font-medium text-gray-900">{customer.id}</td>
                            <td className="px-6 py-4 text-sm text-gray-700 font-medium">{customer.name}</td>
                            <td className="px-6 py-4 text-sm text-gray-600">{customer.age || 'N/A'}</td>
                            <td className="px-6 py-4 text-sm text-gray-600">{customer.city}</td>
                            <td className="px-6 py-4">
                                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                                    customer.credit_score >= 750 ? 'bg-green-100 text-green-700' :
                                    customer.credit_score >= 700 ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-red-100 text-red-700'
                                }`}>
                                    {customer.credit_score}
                                </span>
                            </td>
                            <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                                ₹{customer.pre_approved_limit?.toLocaleString()}
                            </td>
                            <td className="px-6 py-4 text-center">
                                <div className="flex items-center justify-center gap-2">
                                    <button className="bg-blue-600 text-white px-3 py-1 rounded text-xs font-medium hover:bg-blue-700">
                                        View
                                    </button>
                                    <button className="bg-teal-600 text-white px-3 py-1 rounded text-xs font-medium hover:bg-teal-700">
                                        Edit
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function OffersTable({ data }: { data: any[] }) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-800 to-gray-700 text-white">
                    <tr>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Customer ID</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Offer Amount</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Interest Rate</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Tenure Options</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Processing Fee</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {data.map((offer, index) => (
                        <tr key={index} className="hover:bg-blue-50 transition-colors">
                            <td className="px-6 py-4 text-sm font-medium text-gray-900">{offer.customer_id}</td>
                            <td className="px-6 py-4 text-sm font-semibold text-gray-900">₹{offer.amount?.toLocaleString()}</td>
                            <td className="px-6 py-4 text-sm text-gray-700">{offer.interest_rate}%</td>
                            <td className="px-6 py-4 text-sm text-gray-600">{offer.tenure_options}</td>
                            <td className="px-6 py-4 text-sm text-gray-600">₹{offer.processing_fee?.toLocaleString()}</td>
                            <td className="px-6 py-4">
                                <span className="inline-flex px-3 py-1 rounded-full text-xs font-bold bg-green-100 text-green-700">
                                    Active
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function KYCTable({ data }: { data: any[] }) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-800 to-gray-700 text-white">
                    <tr>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Customer ID</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Name</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">PAN</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Aadhar</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Phone Verified</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">KYC Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {data.map((kyc, index) => (
                        <tr key={index} className="hover:bg-blue-50 transition-colors">
                            <td className="px-6 py-4 text-sm font-medium text-gray-900">{kyc.customer_id}</td>
                            <td className="px-6 py-4 text-sm text-gray-700">{kyc.name}</td>
                            <td className="px-6 py-4 text-sm text-gray-600 font-mono">{kyc.pan_number}</td>
                            <td className="px-6 py-4 text-sm text-gray-600 font-mono">{kyc.aadhar_number}</td>
                            <td className="px-6 py-4">
                                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                                    kyc.phone_verified ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                }`}>
                                    {kyc.phone_verified ? '✓ Verified' : '✗ Not Verified'}
                                </span>
                            </td>
                            <td className="px-6 py-4">
                                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                                    kyc.kyc_status === 'COMPLETED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                                }`}>
                                    {kyc.kyc_status}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function CreditTable({ data }: { data: any[] }) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-800 to-gray-700 text-white">
                    <tr>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Customer ID</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Credit Score</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Score Range</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Total Accounts</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Active Loans</th>
                        <th className="px-6 py-4 text-left text-sm font-semibold">Payment History</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {data.map((credit, index) => (
                        <tr key={index} className="hover:bg-blue-50 transition-colors">
                            <td className="px-6 py-4 text-sm font-medium text-gray-900">{credit.customer_id}</td>
                            <td className="px-6 py-4">
                                <span className={`inline-flex px-3 py-1 rounded-full text-sm font-bold ${
                                    credit.credit_score >= 750 ? 'bg-green-100 text-green-700' :
                                    credit.credit_score >= 700 ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-red-100 text-red-700'
                                }`}>
                                    {credit.credit_score}
                                </span>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-600">{credit.score_range}</td>
                            <td className="px-6 py-4 text-sm text-gray-700">{credit.total_accounts}</td>
                            <td className="px-6 py-4 text-sm text-gray-700">{credit.active_accounts}</td>
                            <td className="px-6 py-4">
                                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                                    credit.payment_history === 'Good' || credit.payment_history === 'Excellent' 
                                        ? 'bg-green-100 text-green-700' 
                                        : 'bg-yellow-100 text-yellow-700'
                                }`}>
                                    {credit.payment_history}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
