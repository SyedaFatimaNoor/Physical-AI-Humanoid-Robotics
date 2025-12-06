import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Head from '@docusaurus/Head';

import styles from './index.module.css';

type Track = {
  title: string;
  copy: string;
  tags: string[];
};

type OpsUpdate = {
  label: string;
  status: 'stable' | 'amber' | 'pulse';
  detail: string;
};

const sprintOutline = [
  {
    id: '01',
    title: 'Embodied Intelligence',
    summary: 'Systems thinking & safety playbooks',
  },
  {
    id: '02',
    title: 'ROS 2 Fundamentals',
    summary: 'Realtime control & middleware patterns',
  },
  {
    id: '03',
    title: 'Simulation to Hardware',
    summary: 'Gazebo, Isaac Sim & calibration',
  },
  {
    id: '04',
    title: 'Conversational Robotics',
    summary: 'Multimodal VLA agents in the loop',
  },
];

const pathways: Track[] = [
  {
    title: 'Systems & Simulation',
    copy: 'Model high-fidelity humanoids, stress-test autonomy stacks, and close the sim2real gap with reproducible tooling.',
    tags: ['ROS 2', 'Gazebo', 'Isaac Sim'],
  },
  {
    title: 'Embodied Intelligence',
    copy: 'Fuse perception, planning, and control pipelines with modern foundation models and safety-first guardrails.',
    tags: ['Physical AI', 'Policy distillation', 'Trust & safety'],
  },
  {
    title: 'Deployment & Ops',
    copy: 'Stand up telemetry, CI for robotics, and RAG copilots that sit beside every lab notebook and test cell.',
    tags: ['Observability', 'Fleet ops', 'RAG assistants'],
  },
];

const trustBadges = ['DeepTech Fellows', 'Autonomy Guild', 'Frontier Robotics', 'Atlas Lab Network'];

const opsFeed: OpsUpdate[] = [
  {
    label: 'Control stack',
    status: 'stable',
    detail: 'Loop jitter < 18ms after ROS 2 QoS tuning',
  },
  {
    label: 'RAG tutor',
    status: 'pulse',
    detail: '32 curated notebooks online • 0.8s latency',
  },
  {
    label: 'Hardware rig',
    status: 'amber',
    detail: 'Unitree G1 bay booked • Sat 09:00 UTC',
  },
];

const releaseHighlights = [
  {
    title: 'Module 1 · Robotic Nervous System',
    copy: 'Design ROS 2 nodes, parameter maps, and watchdogs that keep humanoids within thermal and torque limits.',
    meta: 'ROS 2 · rclpy · safety pads',
  },
  {
    title: 'Module 3 · Digital Twin',
    copy: 'Build photoreal Gazebo + Isaac scenes, stream sensor twins, and run sim-to-real transfer rituals.',
    meta: 'Gazebo · Unity · Isaac Sim',
  },
  {
    title: 'Module 6 · Conversational Robotics',
    copy: 'Wire Whisper + GPT planners to gesture stacks so humanoids can negotiate tasks in natural language.',
    meta: 'VLA · Whisper · GPT actions',
  },
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.heroBackdrop} aria-hidden="true" />
      <div className={styles.heroAurora} aria-hidden="true" />
      <div className={clsx('container', styles.heroContainer)}>
        <div className={styles.heroMetaRow}>
          <span>Next intake · February 2025</span>
          <div>
            <span>Guided hardware bring-up</span>
            <span>Live RAG copilots</span>
            <span>Safety reviews</span>
          </div>
        </div>
        <div className={styles.heroGrid}>
          <div className={styles.heroCopy}>
            <div className={styles.heroSignalRow}>
              <span>Studio-grade release</span>
              <span>24-week build track</span>
            </div>
            <span className={styles.pill}>Studio-grade curriculum</span>
            <h1 className={styles.heroTitle}>
              Physical AI & <span>Humanoid Robotics</span>
            </h1>
            <p className={styles.heroSubtitle}>
              {siteConfig.tagline}. Navigate ROS 2, Gazebo, NVIDIA Isaac, and conversational
              robotics with a single, cohesive playbook.
            </p>
            <div className={styles.heroMetrics}>
              <article>
                <strong>Hardware lab</strong>
                <small>Remote kits + onsite calibrations</small>
              </article>
              <article>
                <strong>Ops critiques</strong>
                <small>Weekly faculty reviews & sandboxes</small>
              </article>
              <article>
                <strong>Safety pads</strong>
                <small>Guardrails, incident drills, audits</small>
              </article>
            </div>
            <div className={styles.ctas}>
              <Link
                className={clsx('button button--primary button--lg', styles.primaryCta)}
                to="/docs/module-1--introduction-to-physical-ai">
                Explore modules
              </Link>
              <Link
                className={clsx('button button--secondary button--lg', styles.secondaryCta)}
                to="/docs/capstone-project--the-autonomous-humanoid">
                View capstone brief
              </Link>
            </div>
            <dl className={styles.stats}>
              <div>
                <dt>6 Tracks</dt>
                <dd>From fundamentals to deployment</dd>
              </div>
              <div>
                <dt>120+ Labs</dt>
                <dd>Simulation, hardware & AI copilots</dd>
              </div>
              <div>
                <dt>Capstone</dt>
                <dd>Autonomous humanoid build guide</dd>
              </div>
            </dl>
            <div className={styles.heroFootnote}>
              <span>Trusted launchpads</span>
              <ul className={styles.trustBadges}>
                {trustBadges.map((badge) => (
                  <li key={badge}>{badge}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className={styles.heroPanel}>
            <div className={styles.panelCard}>
              <p className={styles.panelLabel}>Learning sprint</p>
              <ul className={styles.moduleList}>
                {sprintOutline.map((sprint) => (
                  <li key={sprint.id}>
                    <span className={styles.moduleNumber}>{sprint.id}</span>
                    <div>
                      <strong>{sprint.title}</strong>
                      <small>{sprint.summary}</small>
                    </div>
                  </li>
                ))}
              </ul>
              <div className={styles.signal}>
                <span aria-hidden="true" />
                <div>
                  <strong>Live RAG tutor</strong>
                  <small>Highlight any paragraph to summon the assistant.</small>
                </div>
              </div>
            </div>
            <div className={styles.opsCard}>
              <header>
                <span>Ops console</span>
                <span>Realtime</span>
              </header>
              <ul>
                {opsFeed.map((update) => (
                  <li key={update.label}>
                    <div>
                      <strong>{update.label}</strong>
                      <small>{update.detail}</small>
                    </div>
                    <span data-tone={update.status}>
                      {update.status === 'stable' && 'Stable'}
                      {update.status === 'amber' && 'Booked'}
                      {update.status === 'pulse' && 'Online'}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  const metaDescription =
    'Design embodied intelligence systems with a polished, end-to-end robotics curriculum.';

  return (
    <Layout>
      <Head>
        <title>{`${siteConfig.title} | Physical AI Stack`}</title>
        <meta name="description" content={metaDescription} />
      </Head>
      <HomepageHeader />
      <main className={styles.pageSections}>
        <section className={styles.tracksSection}>
          <div className="container">
            <div className={styles.sectionHeading}>
              <p>What you&apos;ll master</p>
              <h2>Full-stack humanoid robotics workflow</h2>
              <span>
                Chain perception, simulation, foundation models, and hardware bring-up into a repeatable operating
                rhythm.
              </span>
            </div>
            <div className={styles.trackGrid}>
              {pathways.map((track) => (
                <article key={track.title} className={styles.trackCard}>
                  <div>
                    <h3>{track.title}</h3>
                    <p>{track.copy}</p>
                  </div>
                  <div className={styles.tagGroup}>
                    {track.tags.map((tag) => (
                      <span key={tag}>{tag}</span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
        <HomepageFeatures />
        <section className={styles.quoteSection}>
          <div className="container">
            <div className={styles.quoteCard}>
              <p>
                &ldquo;The playbook links simulation, control, and conversational robotics so teams can move from lab
                insights to hardware releases without breaking flow.&rdquo;
              </p>
              <div>
                <span>Capstone</span>
                Autonomous humanoid service robot
              </div>
            </div>
          </div>
        </section>
        <section className={styles.chapterShowcase}>
          <div className="container">
            <div className={styles.sectionHeading}>
              <p>Inside the book</p>
              <h2>Chapter launchpads</h2>
              <span>Each module is an ops-ready kit with rituals, labs, and autop-runbooks.</span>
            </div>
            <div className={styles.chapterGrid}>
              {releaseHighlights.map((chapter) => (
                <article key={chapter.title}>
                  <header>
                    <small>Module</small>
                    <strong>{chapter.title}</strong>
                  </header>
                  <p>{chapter.copy}</p>
                  <footer>{chapter.meta}</footer>
                </article>
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
