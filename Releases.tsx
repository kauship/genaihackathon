import React from 'react';
import styles from './Releases.module.css';

type Release = {
  title: string;
  date: string;
};

type PullRequest = {
  title: string;
  date: string;
  description: string;
};

const Releases: React.FC = () => {
  const releases: Release[] = [
    { title: 'Release 1.0.0', date: 'January 1, 2024' },
    { title: 'Release 1.1.0', date: 'February 15, 2024' },
    // Add more releases as needed
  ];

  const pullRequests: PullRequest[] = [
    { title: 'Fix login issue', date: 'March 5, 2024', description: 'Resolved login bug affecting API authentication.' },
    { title: 'Optimize database queries', date: 'March 7, 2024', description: 'Improved performance of main database queries.' },
    // Add more PRs as needed
  ];

  return (
    <div className={styles.pageContainer}>
      {/* Container for side-by-side layout */}
      <div className={styles.sectionsContainer}>
        {/* Releases Section */}
        <div className={`${styles.section} ${styles.releasesSection}`}>
          <h2 className={styles.releasesTitle}>Completed Releases</h2>
          {releases.map((release, index) => (
            <div key={index} className={styles.card}>
              <div className={styles.releaseTitle}>{release.title}</div>
              <div className={styles.releaseDate}>{release.date}</div>
            </div>
          ))}
        </div>

        {/* PR Section */}
        <div className={`${styles.section} ${styles.prSection}`}>
          <h2 className={styles.prTitle}>Current Pull Requests</h2>
          {pullRequests.map((pr, index) => (
            <div key={index} className={styles.card}>
              <div className={styles.prTitleText}>{pr.title}</div>
              <div className={styles.prDate}>{pr.date}</div>
              <div className={styles.prDescription}>{pr.description}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Releases;
