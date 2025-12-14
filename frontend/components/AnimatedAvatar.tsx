import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';

interface AnimatedAvatarProps {
    size?: 'sm' | 'md' | 'lg';
    showGreeting?: boolean;
}

export default function AnimatedAvatar({ size = 'md', showGreeting = false }: AnimatedAvatarProps) {
    const [isThinking, setIsThinking] = useState(false);

    const sizeClasses = {
        sm: 'w-12 h-12',
        md: 'w-24 h-24',
        lg: 'w-32 h-32'
    };

    const containerSize = {
        sm: 'w-16 h-16',
        md: 'w-32 h-32',
        lg: 'w-40 h-40'
    };

    // Simulate thinking animation periodically
    useEffect(() => {
        const interval = setInterval(() => {
            setIsThinking(true);
            setTimeout(() => setIsThinking(false), 2000);
        }, 8000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex flex-col items-center justify-center gap-4">
            {/* Avatar Container with Pulse Animation */}
            <motion.div
                className={`${containerSize[size]} relative flex items-center justify-center`}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.5, type: "spring" }}
            >
                {/* Outer Ring - Pulse Effect */}
                <motion.div
                    className="absolute inset-0 rounded-full bg-gradient-to-br from-tata-blue to-blue-400"
                    animate={{
                        scale: isThinking ? [1, 1.1, 1] : 1,
                        opacity: isThinking ? [0.5, 0.8, 0.5] : 0.3,
                    }}
                    transition={{
                        duration: 2,
                        repeat: isThinking ? Infinity : 0,
                        ease: "easeInOut"
                    }}
                />

                {/* Middle Ring */}
                <motion.div
                    className="absolute inset-2 rounded-full bg-gradient-to-br from-blue-400 to-tata-blue"
                    animate={{
                        scale: isThinking ? [1, 1.05, 1] : 1,
                        opacity: 0.5,
                    }}
                    transition={{
                        duration: 2,
                        delay: 0.2,
                        repeat: isThinking ? Infinity : 0,
                        ease: "easeInOut"
                    }}
                />

                {/* Avatar Image Container */}
                <motion.div
                    className={`${sizeClasses[size]} relative rounded-full bg-white flex items-center justify-center overflow-hidden shadow-xl border-4 border-white`}
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                >
                    {/* TIA Logo */}
                    <Image
                        src="/Tia-icon.svg"
                        alt="TIA"
                        width={128}
                        height={128}
                        className="w-full h-full object-contain p-2"
                    />

                    {/* Thinking Indicator */}
                    {isThinking && (
                        <motion.div
                            className="absolute bottom-0 right-0 bg-green-400 rounded-full p-1"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            exit={{ scale: 0 }}
                        >
                            <motion.div
                                className="flex gap-0.5"
                                animate={{
                                    opacity: [0.5, 1, 0.5],
                                }}
                                transition={{
                                    duration: 1.5,
                                    repeat: Infinity,
                                }}
                            >
                                <div className="w-1 h-1 bg-white rounded-full" />
                                <div className="w-1 h-1 bg-white rounded-full" />
                                <div className="w-1 h-1 bg-white rounded-full" />
                            </motion.div>
                        </motion.div>
                    )}
                </motion.div>
            </motion.div>

            {/* Greeting Text with Fade-in Animation */}
            {showGreeting && (
                <motion.div
                    className="text-center"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, duration: 0.5 }}
                >
                    <motion.h3
                        className="text-xl font-bold text-gray-800 mb-2"
                        animate={{
                            opacity: [1, 0.8, 1],
                        }}
                        transition={{
                            duration: 3,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                    >
                        Hi, I'm TIA
                    </motion.h3>
                    <motion.p
                        className="text-sm text-gray-600 max-w-xs"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.8 }}
                    >
                        Your personal loan assistant at Tata Capital.
                    </motion.p>
                </motion.div>
            )}
        </div>
    );
}
