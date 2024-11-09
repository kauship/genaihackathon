documentation_dashboard/
├── backend/
│   ├── app.py                 # Flask app with API endpoints
│   ├── generate_docs.py       # Script to generate structured documentation
│   └── data/
│       └── documentation.json # JSON data from generated documentation
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── style.css              # Custom CSS
│   ├── app.js                 # JavaScript for interactive features
│   └── components/
│       ├── Sidebar.js         # Sidebar component
│       ├── Content.js         # Main content area component
│       └── Search.js          # Search bar component
└── README.md


  # backend/app.py
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load documentation JSON
with open('data/documentation.json') as f:
    documentation = json.load(f)

@app.route('/api/sections', methods=['GET'])
def get_sections():
    return jsonify(list(documentation.keys()))

@app.route('/api/section/<section_name>', methods=['GET'])
def get_section(section_name):
    return jsonify(documentation.get(section_name, {}))

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    results = {}
    for section, files in documentation.items():
        results[section] = {file: content for file, content in files.items() if query in content.lower()}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)


// frontend/app.js
import React, { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Content from './components/Content';
import Search from './components/Search';

function App() {
    const [sections, setSections] = useState([]);
    const [content, setContent] = useState({});
    const [currentSection, setCurrentSection] = useState(null);

    useEffect(() => {
        fetch('/api/sections')
            .then(response => response.json())
            .then(data => setSections(data));
    }, []);

    const fetchContent = (section) => {
        fetch(`/api/section/${section}`)
            .then(response => response.json())
            .then(data => {
                setCurrentSection(section);
                setContent(data);
            });
    };

    return (
        <div className="App">
            <Sidebar sections={sections} onSelect={fetchContent} />
            <Content section={currentSection} content={content} />
            <Search onSearch={query => fetch(`/api/search?query=${query}`).then(res => res.json()).then(setContent)} />
        </div>
    );
}

export default App;






