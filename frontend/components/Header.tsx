
import React, { useState } from 'react';
import Link from 'next/link';
import { Menu, Search, User, X } from 'lucide-react';

interface HeaderProps {
  onLoginClick?: () => void;
}

export default function Header({ onLoginClick }: HeaderProps = {}) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 h-12 flex items-center justify-between">
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
          <Link href="#" className="hover:text-tata-blue transition-colors relative group">
            Personal Loan
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-tata-blue transition-all group-hover:w-full"></span>
          </Link>
          <Link href="#" className="hover:text-tata-blue transition-colors relative group">
            Home Loan
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-tata-blue transition-all group-hover:w-full"></span>
          </Link>
          <Link href="#" className="hover:text-tata-blue transition-colors relative group">
            Business Loan
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-tata-blue transition-all group-hover:w-full"></span>
          </Link>
          <Link href="#" className="hover:text-tata-blue transition-colors relative group">
            Calculators
            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-tata-blue transition-all group-hover:w-full"></span>
          </Link>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <button
            className="p-2 hover:bg-gray-100 rounded-full text-gray-600 transition-colors"
            aria-label="Search"
          >
            <Search size={20} />
          </button>
          <button
            onClick={onLoginClick}
            className="hidden md:flex items-center gap-2 bg-tata-red text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors font-medium shadow-sm hover:shadow-md"
            aria-label="Login to your account"
          >
            <User size={18} />
            <span>Login</span>
          </button>
          <button
            className="md:hidden p-2 hover:bg-gray-100 rounded-full text-gray-600 transition-colors"
            aria-label="Open menu"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 absolute w-full shadow-lg animate-fade-in">
          <nav className="flex flex-col p-4 space-y-4 font-medium text-gray-700">
            <Link href="#" className="hover:text-tata-blue transition-colors p-2 hover:bg-gray-50 rounded">Personal Loan</Link>
            <Link href="#" className="hover:text-tata-blue transition-colors p-2 hover:bg-gray-50 rounded">Home Loan</Link>
            <Link href="#" className="hover:text-tata-blue transition-colors p-2 hover:bg-gray-50 rounded">Business Loan</Link>
            <Link href="#" className="hover:text-tata-blue transition-colors p-2 hover:bg-gray-50 rounded">Calculators</Link>
            <button
              className="flex items-center gap-2 bg-tata-red text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors font-medium w-full justify-center mt-4"
            >
              <User size={18} />
              <span>Login</span>
            </button>
          </nav>
        </div>
      )}

      {/* Sub-header for Personal Loan context */}
      <div className="bg-tata-blue text-white py-2 px-4 text-sm hidden md:block">
        <div className="container mx-auto flex justify-between items-center">
          <span className="font-medium">Personal Loan Assistant</span>
          <div className="flex gap-6 text-blue-100">
            <span className="hover:text-white cursor-pointer transition-colors">Call us: 1800-209-6060</span>
            <span className="hover:text-white cursor-pointer transition-colors">Email: customercare@tatacapital.com</span>
          </div>
        </div>
      </div>
    </header>
  );
}
