import React, { useState } from 'react';
import Layout from '@theme/Layout';

const Home: React.FC = () => {
  const [githubLink, setGithubLink] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:4000/generate-docs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ githubLink }),
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
      <div className="container">
        <h1>Generate Documentation for Your GitHub Project</h1>
        <form onSubmit={handleSubmit}>
          <label htmlFor="githubLink">GitHub Repository Link:</label>
          <input
            type="text"
            id="githubLink"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
            placeholder="https://github.com/user/repo"
            required
          />
          <button type="submit">Generate Documentation</button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </Layout>
  );
};

export default Home;
