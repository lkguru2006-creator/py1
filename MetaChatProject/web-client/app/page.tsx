"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, Image as ImageIcon, Paperclip, Sparkles } from "lucide-react";
import ThreeDLetterG from "@/components/ThreeDLetterG";

export default function Home() {
    const [messages, setMessages] = useState<{ role: string; content: string }[]>([
        { role: "assistant", content: "Hello! I am MetaChat AI. How can I help you today?" },
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setInput("");
        setIsLoading(true);

        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.body) return;

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let assistantResponse = "";

            setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                assistantResponse += chunk;

                setMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1].content = assistantResponse;
                    return newMessages;
                });
            }
        } catch (error) {
            console.error("Error calling chatter API", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="flex min-h-screen flex-row bg-gray-50 dark:bg-gray-900 overflow-hidden">
            {/* Sidebar / Hero Section (Desktop) */}
            <section className="hidden lg:flex w-1/3 relative flex-col items-center justify-center bg-meta-gradient text-white overflow-hidden">
                {/* Abstract Background Shapes */}
                <div className="absolute top-0 left-0 w-full h-full opacity-20 pointer-events-none">
                    <div className="absolute top-[-20%] left-[-20%] w-[800px] h-[800px] rounded-full bg-white blur-[100px] mix-blend-overlay animate-float"></div>
                    <div className="absolute bottom-[-20%] right-[-20%] w-[600px] h-[600px] rounded-full bg-blue-300 blur-[80px] mix-blend-overlay"></div>
                </div>

                <div className="relative z-10 flex flex-col items-center gap-8 p-10 text-center">
                    <ThreeDLetterG />
                    <div className="space-y-4 max-w-md">
                        <h2 className="text-4xl font-bold tracking-tight">Experience<br />The Future</h2>
                        <p className="text-blue-100 text-lg font-light leading-relaxed">
                            Engage with the next generation of AI in a beautifully designed, immersive environment.
                        </p>
                    </div>
                </div>

                <div className="absolute bottom-8 text-sm text-blue-200/60 font-medium tracking-widest uppercase">
                    MetaChat AI v1.0
                </div>
            </section>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative h-screen bg-[#f0f2f5] dark:bg-[#18191a]">

                {/* Header */}
                <header className="w-full p-4 glass-panel sticky top-0 z-20 shadow-sm backdrop-blur-md">
                    <div className="max-w-4xl mx-auto flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-gradient-to-br from-meta-base to-meta-light rounded-2xl shadow-lg shadow-blue-500/30">
                                <Bot className="text-white w-6 h-6" />
                            </div>
                            <div>
                                <h1 className="text-xl font-bold text-gray-800 dark:text-white">MetaChat</h1>
                                <div className="flex items-center gap-1.5">
                                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                    <span className="text-xs text-gray-500 font-medium">Online</span>
                                </div>
                            </div>
                        </div>
                        <button className="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
                            <Sparkles className="w-5 h-5 text-meta-base" />
                        </button>
                    </div>
                </header>

                {/* Messages */}
                <div className="flex-1 w-full max-w-4xl mx-auto p-4 md:p-6 overflow-y-auto space-y-6 scroll-smooth">
                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex w-full group ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                        >
                            {msg.role === "assistant" && (
                                <div className="w-8 h-8 mr-3 rounded-full bg-gradient-to-br from-meta-base to-meta-light flex items-center justify-center shadow-md flex-shrink-0 mt-2">
                                    <Bot className="w-5 h-5 text-white" />
                                </div>
                            )}

                            <div
                                className={`flex max-w-[85%] md:max-w-[70%] rounded-2xl p-4 shadow-sm transition-all duration-200 ${msg.role === "user"
                                        ? "bg-gradient-to-br from-meta-base to-meta-dark text-white rounded-br-none shadow-blue-500/20"
                                        : "bg-white dark:bg-[#242526] text-gray-800 dark:text-gray-100 rounded-bl-none border border-gray-100 dark:border-gray-700"
                                    }`}
                            >
                                <p className="whitespace-pre-wrap leading-relaxed text-[15px]">{msg.content}</p>
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-meta-base to-meta-light flex items-center justify-center shadow-md">
                                <Bot className="w-5 h-5 text-white" />
                            </div>
                            <div className="bg-white dark:bg-[#242526] px-4 py-3 rounded-2xl rounded-bl-none border border-gray-100 dark:border-gray-700 flex items-center gap-2">
                                <span className="w-2 h-2 bg-meta-base/60 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                                <span className="w-2 h-2 bg-meta-base/60 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                <span className="w-2 h-2 bg-meta-base/60 rounded-full animate-bounce"></span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-white/80 dark:bg-[#242526]/80 backdrop-blur-md border-t border-gray-100 dark:border-gray-800">
                    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative flex items-center gap-3">
                        <button type="button" className="p-3 text-gray-400 hover:text-meta-base hover:bg-blue-50 rounded-full transition-all duration-200">
                            <ImageIcon size={22} />
                        </button>
                        <button type="button" className="p-3 text-gray-400 hover:text-meta-base hover:bg-blue-50 rounded-full transition-all duration-200">
                            <Paperclip size={22} />
                        </button>

                        <div className="flex-1 relative group">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Message MetaChat..."
                                className="w-full p-4 pl-6 pr-12 rounded-3xl bg-gray-100 dark:bg-[#3a3b3c] border-transparent focus:bg-white dark:focus:bg-[#3a3b3c] focus:border-meta-base/30 dark:text-white focus:outline-none focus:ring-4 focus:ring-meta-base/10 transition-all duration-200 shadow-inner"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="p-4 bg-meta-base text-white rounded-full hover:bg-meta-dark hover:shadow-lg hover:shadow-blue-500/30 disabled:opacity-50 disabled:shadow-none disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95"
                        >
                            <Send size={20} className={input.trim() ? "fill-current" : ""} />
                        </button>
                    </form>
                    <div className="text-center mt-2">
                        <p className="text-xs text-gray-400">MetaChat can make mistakes. Verify important info.</p>
                    </div>
                </div>
            </div>
        </main>
    );
}
