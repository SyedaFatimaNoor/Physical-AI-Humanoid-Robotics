import React, { useState } from 'react';
import Content from '@theme-original/DocItem/Content';
import { useDoc } from '@docusaurus/theme-common/internal';

export default function ContentWrapper(props) {
    const { metadata } = useDoc();
    const [contentMode, setContentMode] = useState('default'); // default, personalized, urdu
    const [customContent, setCustomContent] = useState(null);
    const [loading, setLoading] = useState(false);

    const handlePersonalize = async (mode) => {
        setLoading(true);
        try {
            const endpoint = mode === 'urdu' ? 'http://localhost:8000/rag/translate' : 'http://localhost:8000/rag/personalize';
            const body = {
                text: "Chapter content placeholder", // In real app, send slug or content
                level: "beginner", // Mock user level
                target_language: "Urdu"
            };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await response.json();
            setCustomContent(data.personalized_markdown || data.translated_markdown);
            setContentMode(mode);
        } catch (error) {
            alert("Failed to personalize content");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <button onClick={() => setContentMode('default')} disabled={contentMode === 'default'}>
                    Original
                </button>
                <button onClick={() => handlePersonalize('personalized')} disabled={loading}>
                    {loading && contentMode === 'personalized' ? 'Generating...' : 'Personalize for Me'}
                </button>
                <button onClick={() => handlePersonalize('urdu')} disabled={loading}>
                    {loading && contentMode === 'urdu' ? 'Translating...' : 'Translate to Urdu'}
                </button>
            </div>

            {contentMode === 'default' ? (
                <Content {...props} />
            ) : (
                <div className="markdown">
                    {/* In a real app, use a Markdown renderer like react-markdown here */}
                    <pre style={{ whiteSpace: 'pre-wrap' }}>{customContent}</pre>
                </div>
            )}
        </>
    );
}
