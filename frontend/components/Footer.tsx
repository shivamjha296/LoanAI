
import React from 'react';

export default function Footer() {
    return (
        <footer className="bg-gray-900 text-white pt-12 pb-6">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Products</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li>Personal Loan</li>
                            <li>Home Loan</li>
                            <li>Business Loan</li>
                            <li>Loan Against Property</li>
                            <li>Used Car Loan</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Calculators</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li>Personal Loan EMI Calculator</li>
                            <li>Home Loan EMI Calculator</li>
                            <li>Business Loan EMI Calculator</li>
                            <li>Eligibility Calculator</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">About Us</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li>Overview</li>
                            <li>Leadership</li>
                            <li>Careers</li>
                            <li>Contact Us</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Connect</h3>
                        <p className="text-gray-400 text-sm mb-4">
                            Stay updated with our latest offers and news.
                        </p>
                        <div className="flex gap-2">
                            {/* Social icons placeholders */}
                            <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                            <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                            <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                            <div className="w-8 h-8 bg-gray-700 rounded-full"></div>
                        </div>
                    </div>
                </div>

                <div className="border-t border-gray-800 pt-6 text-center text-gray-500 text-sm">
                    <p>&copy; 2024 Tata Capital Limited. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}
