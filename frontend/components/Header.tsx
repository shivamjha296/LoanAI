
import React from 'react';
import Link from 'next/link';
import { Menu, Search, User } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2">
            {/* Placeholder for Logo - using text for now or a simple SVG */}
            <div className="bg-tata-blue text-white p-1 rounded font-bold text-xl tracking-tighter">
              TATA
            </div>
            <div className="text-tata-blue font-bold text-xl tracking-tight">
              CAPITAL
            </div>
          </Link>
        </div>

        {/* Navigation - Desktop */}
        <nav className="hidden md:flex items-center gap-8 text-gray-700 font-medium">
          <Link href="#" className="hover:text-tata-blue transition-colors">Personal Loan</Link>
          <Link href="#" className="hover:text-tata-blue transition-colors">Home Loan</Link>
          <Link href="#" className="hover:text-tata-blue transition-colors">Business Loan</Link>
          <Link href="#" className="hover:text-tata-blue transition-colors">Calculators</Link>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-gray-100 rounded-full text-gray-600">
            <Search size={20} />
          </button>
          <button className="hidden md:flex items-center gap-2 bg-tata-red text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors font-medium">
            <User size={18} />
            <span>Login</span>
          </button>
          <button className="md:hidden p-2 hover:bg-gray-100 rounded-full text-gray-600">
            <Menu size={24} />
          </button>
        </div>
      </div>
      
      {/* Sub-header for Personal Loan context */}
      <div className="bg-tata-blue text-white py-2 px-4 text-sm hidden md:block">
        <div className="container mx-auto flex justify-between items-center">
          <span>Personal Loan Assistant</span>
          <div className="flex gap-4">
            <span>Call us: 1800-209-6060</span>
            <span>Email: customercare@tatacapital.com</span>
          </div>
        </div>
      </div>
    </header>
  );
}
