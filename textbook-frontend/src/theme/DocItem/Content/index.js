import React, {useEffect, useState} from 'react';
import clsx from 'clsx';
import Content from '@theme-original/DocItem/Content';
import ReactMarkdown from 'react-markdown';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import API from '../../../config/api';

import styles from './styles.module.css';

const statusCopy = {
    default: 'Rendering the original textbook narrative',
    personalized: 'Personalized for your learning profile',
    urdu: 'Translated to Urdu with right-to-left formatting',
};

export default function ContentWrapper(props) {
    const {metadata, frontMatter} = useDoc();
    const heroTitle = metadata?.title ?? props.contentTitle ?? 'Physical AI Module';
    const heroDescription =
        frontMatter?.abstract ??
        metadata?.description ??
        'Operational briefings, labs, and autopilot rituals for embodied intelligence.';
    const heroPill = frontMatter?.pill ?? 'Embodied Intelligence';
    const moduleCode = frontMatter?.module ?? metadata?.permalink?.split('/').slice(-1)[0] ?? 'Module';
    const heroChips =
        (Array.isArray(frontMatter?.tags) && frontMatter.tags.length > 0 ? frontMatter.tags : null) ??
        ['ROS 2', 'Gazebo', 'Isaac Sim'];

    const [contentMode, setContentMode] = useState('default'); // default, personalized, urdu
    const [customContent, setCustomContent] = useState('');
    const [loading, setLoading] = useState(false);
    const [baseText, setBaseText] = useState('');

    useEffect(() => {
        if (contentMode !== 'default') {
            return;
        }
        const article = document.querySelector('.theme-doc-markdown');
        const text = article ? article.innerText : '';
        if (text) {
            setBaseText(text);
        }
    }, [contentMode]);

    const handlePersonalize = async (mode) => {
        setLoading(true);
        const text = baseText || document.querySelector('.theme-doc-markdown')?.innerText || '';

        if (!text) {
            alert('Could not find content to process');
            setLoading(false);
            return;
        }

        try {
            const endpoint = mode === 'urdu' ? API.translate : API.personalize;
            const body = mode === 'urdu' ? { chapter: text, language: 'ur' } : { text, level: 'beginner' };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            setCustomContent(data.personalized_markdown || data.translated || '');
            setContentMode(mode);
        } catch (error) {
            console.error('API Error:', error);
            alert('Failed to process content. Please make sure the backend is running at the configured URL.');
        } finally {
            setLoading(false);
        }
    };

    const resetToOriginal = () => {
        setContentMode('default');
        setCustomContent('');
    };

    const renderBody =
        contentMode === 'default' ? (
            <div className={styles.docBodyCard}>
                <Content {...props} />
            </div>
        ) : (
            <div
                className={clsx(styles.docBodyCard, styles.generatedPanel)}
                dir={contentMode === 'urdu' ? 'rtl' : 'ltr'}>
                <ReactMarkdown>{customContent}</ReactMarkdown>
            </div>
        );

    return (
        <div className={styles.docShell}>
            <section className={styles.docHero}>
                <div className={styles.heroPillRow}>
                    <span>{moduleCode}</span>
                    <small>{heroPill}</small>
                </div>
                <h1>{heroTitle}</h1>
                <p>{heroDescription}</p>
                <div className={styles.heroChips}>
                    {heroChips.map((chip) => (
                        <span key={chip}>{chip}</span>
                    ))}
                </div>
            </section>

            <div className={styles.docActions}>
                <div className={styles.actionCopy}>
                    <span>Adaptive mode</span>
                    <p>{statusCopy[contentMode]}</p>
                </div>
                <div className={styles.actionButtons}>
                    <button
                        className={clsx('button button--sm', contentMode === 'default' ? 'button--secondary' : '')}
                        onClick={resetToOriginal}
                        disabled={contentMode === 'default'}>
                        Original
                    </button>
                    <button
                        className={clsx('button button--sm button--primary', styles.primaryAction)}
                        onClick={() => handlePersonalize('personalized')}
                        disabled={loading}>
                        {loading && contentMode === 'personalized' ? 'Personalizing…' : '✨ Personalize'}
                    </button>
                    <button
                        className="button button--sm button--outline button--info"
                        onClick={() => handlePersonalize('urdu')}
                        disabled={loading}>
                        {loading && contentMode === 'urdu' ? 'Translating…' : '🌐 Urdu'}
                    </button>
                </div>
            </div>

            {renderBody}
        </div>
    );
}
