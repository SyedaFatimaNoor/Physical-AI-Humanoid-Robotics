import React, { useState, useEffect, ChangeEvent, KeyboardEvent } from 'react';
import './chat.css';

interface Message {
    role: string;
    content: string;
}

const ChatWidget: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [selectedText, setSelectedText] = useState<string>('');

    useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection();
            const text = selection ? selection.toString() : '';
            if (text && text.length > 10) {
                setSelectedText(text);
                if (!isOpen) setIsOpen(true); // Auto-open on selection
            }
        };

        document.addEventListener('mouseup', handleSelection);
        return () => document.removeEventListener('mouseup', handleSelection);
    }, [isOpen]);

    const toggleChat = () => setIsOpen(!isOpen);

    const sendMessage = async () => {
        if (!input.trim() && !selectedText) return;

        const userMsg: Message = { role: 'user', content: input };
        setMessages((prev: Message[]) => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            let endpoint = 'http://localhost:8000/rag/ask';
            let body: any = { query: input, history: messages };

            if (selectedText) {
                endpoint = 'http://localhost:8000/rag/ask-selection';
                body = { query: input || "Explain this selection", selected_text: selectedText };
                // Clear selection after sending
                setSelectedText('');
            }

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await response.json();
            setMessages((prev: Message[]) => [...prev, { role: 'assistant', content: data.answer }]);
        } catch (error) {
            setMessages((prev: Message[]) => [...prev, { role: 'assistant', content: "Error connecting to AI." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-widget-container">
            {!isOpen && (
                <button className="chat-toggle-btn" onClick={toggleChat}>
                    💬 Ask AI
                </button>
            )}
            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <h3>Physical AI Assistant</h3>
                        <button onClick={toggleChat}>X</button>
                    </div>
                    <div className="chat-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role}`}>
                                {msg.content}
                            </div>
                        ))}
                        {loading && <div className="message assistant">Thinking...</div>}
                    </div>

                    {selectedText && (
                        <div className="selection-preview">
                            <small>Selected: {selectedText.substring(0, 30)}...</small>
                            <button onClick={() => setSelectedText('')}>x</button>
                        </div>
                    )}

                    <div className="chat-input">
                        <input
                            value={input}
                            onChange={(e: ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
                            onKeyPress={(e: KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && sendMessage()}
                            placeholder={selectedText ? "Ask about selection..." : "Ask a question..."}
                        />
                        <button onClick={sendMessage}>Send</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatWidget;
