// src/components/ChatWidget.tsx
import React, { useState, useEffect } from 'react';
// Using native fetch instead of axios
import './chat.css'; // We'll add minimal styling later

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const ChatWidget: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [selectedText, setSelectedText] = useState<string>('');
    // Removed duplicate selectedText state

    // Removed duplicate selection effect

    // Capture user text selection for contextual QA
    React.useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection();
            const text = selection ? selection.toString() : '';
            if (text && text.length > 10) {
                setSelectedText(text);
            }
        };
        document.addEventListener('mouseup', handleSelection);
        return () => document.removeEventListener('mouseup', handleSelection);
    }, []);

    const sendMessage = async () => {
        if (!input.trim()) return;
        const userMsg: Message = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);
        try {
            const body = selectedText
                ? { query: input || 'Explain this selection', selected_text: selectedText }
                : { query: input };
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
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
            setSelectedText('');
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
                placeholder={selectedText ? 'Ask about selected text...' : 'Ask a question about the chapter...'}
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
