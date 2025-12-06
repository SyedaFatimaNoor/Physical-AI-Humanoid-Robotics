import type {ReactNode} from 'react';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: ReactNode;
  icon: string;
  meta: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Adaptive Control Studio',
    description: (
      <>
        Build reusable control blocks with latency budgets, watchdogs, and ROS 2 QoS templates that survive
        lab-to-field shifts.
      </>
    ),
    icon: '01',
    meta: 'Control & middleware',
  },
  {
    title: 'Simulation to Reality Bridge',
    description: (
      <>
        Validate full-stack behaviors in Gazebo & Isaac, then auto-generate calibration and telemetry rituals for the
        real robot.
      </>
    ),
    icon: '02',
    meta: 'Sim pipelines',
  },
  {
    title: 'RAG Copilot Inbox',
    description: (
      <>
        Spin up a notebook-aware assistant that surfaces troubleshooting recipes, BOM context, and test results in
        under a second.
      </>
    ),
    icon: '03',
    meta: 'AI assistance',
  },
];

function Feature({title, description, icon, meta}: FeatureItem) {
  return (
    <article className={styles.featureCard}>
      <div className={styles.featureIcon}>{icon}</div>
      <div className={styles.featureBody}>
        <div className={styles.featureMeta}>{meta}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </article>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.featureGrid}>
          {FeatureList.map((props) => (
            <Feature key={props.title} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
