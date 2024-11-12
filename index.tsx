import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './index.module.css';

const SECTIONS = [
  "Overview of Code",
  "Getting Started",
  "Code Structure Overview",
  "Key Code Components",
  "Functions and API Documentation",
  "Error Handling and Logging",
  "Dependencies",
  "Configuration",
  "Performance Considerations",
  "Testing and Quality Assurance",
  "Security Considerations",
  "Version Control and Changelog",
  "FAQ",
  "Appendix",
  "Conclusion",
];

const Home: React.FC = () => {
  const [githubLink, setGithubLink] = useState('');
  const [selectedSections, setSelectedSections] = useState<string[]>([]);
  const [message, setMessage] = useState('');

  const handleCheckboxChange = (section: string) => {
    setSelectedSections(prev => 
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:4000/generate-docs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ githubLink, selectedSections }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('Documentation generated successfully!');
      } else {
        setMessage(data.error || 'Error generating documentation.');
      }
    } catch (error) {
      setMessage('Error connecting to the server.');
    }
  };

  return (
    <Layout title="Home" description="Generate Documentation for Your Project">
      <div className={styles.container}>
        <h1 className={styles.title}>Generate Documentation for Your GitHub Project</h1>
        <p className={styles.subtitle}>
          Enter your GitHub link and choose the sections to include in the documentation.
        </p>
        <form onSubmit={handleSubmit} className={styles.form}>
          <label htmlFor="githubLink" className={styles.label}>GitHub Repository Link:</label>
          <input
            type="text"
            id="githubLink"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
            placeholder="https://github.com/user/repo"
            required
            className={styles.input}
          />

          <div className={styles.sectionSelection}>
            <h3 className={styles.sectionTitle}>Select Documentation Sections</h3>
            <div className={styles.sectionCheckboxes}>
              {SECTIONS.map(section => (
                <label key={section} className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={selectedSections.includes(section)}
                    onChange={() => handleCheckboxChange(section)}
                    className={styles.checkbox}
                  />
                  {section}
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className={styles.button}>Generate Documentation</button>
        </form>
        {message && <p className={styles.message}>{message}</p>}
      </div>
    </Layout>
  );
};

export default Home;
