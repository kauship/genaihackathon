import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import styles from './Releases.module.css';
import releaseData from '../data/releaseData.json';
import clsx from 'clsx';

interface Release {
  name: string;
  version: string;
  date: string;
  description: string;
}

interface PR {
  title: string;
  number: number;
  author: string;
  date: string;
  description: string;
}

const Releases: React.FC = () => {
  const [releases, setReleases] = useState<Release[]>([]);
  const [mergedPRs, setMergedPRs] = useState<PR[]>([]);

  useEffect(() => {
    setReleases(releaseData.releases);
    setMergedPRs(releaseData.mergedPRs);
  }, []);

  return (
    <Layout title="Releases and Merged PRs">
      <div className={clsx(styles.pageContainer)}>
        <h1 className={styles.header}>Releases and Merged Pull Requests</h1>

        <div className={clsx(styles.section, styles.releasesSection)}>
          <h2 className={styles.sectionHeader}>Completed Releases</h2>
          <div className={styles.gridContainer}>
            {releases.map((release, index) => (
              <div key={index} className={styles.card}>
                <h3 className={styles.cardTitle}>{release.name}</h3>
                <p className={styles.cardVersion}>Version: {release.version}</p>
                <p className={styles.cardDate}>Date: {release.date}</p>
                <p className={styles.cardDescription}>{release.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className={clsx(styles.section, styles.prSection)}>
          <h2 className={styles.sectionHeader}>Recently Merged PRs</h2>
          <div className={styles.gridContainer}>
            {mergedPRs.map((pr, index) => (
              <div key={index} className={styles.card}>
                <h3 className={styles.cardTitle}>#{pr.number} - {pr.title}</h3>
                <p className={styles.cardAuthor}>Author: {pr.author}</p>
                <p className={styles.cardDate}>Merged on: {pr.date}</p>
                <p className={styles.cardDescription}>{pr.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Releases;
