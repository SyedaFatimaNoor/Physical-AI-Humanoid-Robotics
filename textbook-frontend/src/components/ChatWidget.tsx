// src/components/ChatWidget.tsx
import React, { useState } from 'react';
// Using native fetch instead of axios
import './ChatWidget.css'; // We'll add minimal styling later

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const ChatWidget: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const userMsg: Message = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: input })
            });
            const data = await response.json();
            const assistantMsg: Message = { role: 'assistant', content: data.answer };
            setMessages((prev) => [...prev, assistantMsg]);
        } catch (err) {
            const errMsg: Message = { role: 'assistant', content: 'Error: unable to get response.' };
            setMessages((prev) => [...prev, errMsg]);
        } finally {
            setLoading(false);
            setInput('');
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="chat-widget">
            <div className="messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        {msg.content}
                    </div>
                ))}
                {loading && <div className="message assistant">Typing...</div>}
            </div>
            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the chapter..."
                disabled={loading}
                rows={2}
            />
            <button onClick={sendMessage} disabled={loading || !input.trim()}>
                Send
            </button>
        </div>
    );
};

export default ChatWidget;
