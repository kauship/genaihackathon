import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Documentation, OverviewSection } from './types';

const App: React.FC = () => {
  const [documentation, setDocumentation] = useState<Documentation | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchDocumentation = async () => {
      try {
        const response = await axios.get<Documentation>('/api/documentation');
        setDocumentation(response.data);
      } catch (error) {
        console.error("Error fetching documentation", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDocumentation();
  }, []);

  if (loading) return <div>Loading...</div>;

  if (!documentation) return <div>No documentation available</div>;

  return (
    <div className="App">
      <h1>Project Documentation</h1>

      {/* Overview */}
      <section>
        <h2>1. Overview</h2>
        <p>{documentation.Overview.description}</p>
      </section>

      {/* Getting Started */}
      <section>
        <h2>2. Getting Started</h2>
        <h3>Prerequisites</h3>
        <ul>
          {documentation.GettingStarted.Prequsites.map((prerequisite, index) => (
            <li key={index}>{prerequisite}</li>
          ))}
        </ul>
        <h3>Setup Instructions</h3>
        <ul>
          {documentation.GettingStarted.SetupInstructions.map((instruction, index) => (
            <li key={index}>{instruction}</li>
          ))}
        </ul>
        <h3>Run Instructions</h3>
        <ul>
          {documentation.GettingStarted.RunInstructions.map((instruction, index) => (
            <li key={index}>{instruction}</li>
          ))}
        </ul>
      </section>

      {/* Additional sections... */}
    </div>
  );
};

export default App;
