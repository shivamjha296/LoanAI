
import React from 'react';
import { Facebook, Twitter, Linkedin, Instagram, Youtube } from 'lucide-react';

export default function Footer() {
    return (
        <footer className="bg-gray-900 text-white pt-12 pb-6">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Products</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li className="hover:text-white cursor-pointer transition-colors">Personal Loan</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Home Loan</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Business Loan</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Loan Against Property</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Used Car Loan</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Calculators</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li className="hover:text-white cursor-pointer transition-colors">Personal Loan EMI Calculator</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Home Loan EMI Calculator</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Business Loan EMI Calculator</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Eligibility Calculator</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">About Us</h3>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li className="hover:text-white cursor-pointer transition-colors">Overview</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Leadership</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Careers</li>
                            <li className="hover:text-white cursor-pointer transition-colors">Contact Us</li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-bold mb-4 text-tata-blue">Connect</h3>
                        <p className="text-gray-400 text-sm mb-4">
                            Stay updated with our latest offers and news.
                        </p>
                        <div className="flex gap-4">
                            <a href="#" className="text-gray-400 hover:text-white transition-colors"><Facebook size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-white transition-colors"><Twitter size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-white transition-colors"><Linkedin size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-white transition-colors"><Instagram size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-white transition-colors"><Youtube size={20} /></a>
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
