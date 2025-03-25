import React, { useState } from 'react';
import './styles.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setAnalysisResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/analyze-code', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const result = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderScoreBar = (score) => {
    return (
      <div className="score-bar-container">
        <div 
          className="score-bar" 
          style={{ width: `${score}%`, backgroundColor: getScoreColor(score) }}
        ></div>
        <span className="score-text">{score}/100</span>
      </div>
    );
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FFC107';
    if (score >= 40) return '#FF9800';
    return '#F44336';
  };

  return (
    <div className="file-upload-container">
      <h1>Clean Code Analyzer</h1>
      <p>Upload a JavaScript (.js, .jsx) or Python (.py) file to analyze its code quality.</p>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-input-container">
          <input 
            type="file" 
            id="code-file" 
            accept=".js,.jsx,.py" 
            onChange={handleFileChange}
          />
          <label htmlFor="code-file" className="file-label">
            {file ? file.name : 'Choose a file...'}
          </label>
        </div>
        <button type="submit" disabled={isLoading} className="analyze-button">
          {isLoading ? 'Analyzing...' : 'Analyze Code'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {analysisResult && (
        <div className="results-container">
          <h2>Analysis Results</h2>
          
          <div className="overall-score">
            <h3>Overall Score</h3>
            {renderScoreBar(analysisResult.overall_score)}
          </div>

          <div className="breakdown-section">
            <h3>Category Breakdown</h3>
            <div className="breakdown-grid">
              <div className="breakdown-item">
                <span>Naming Conventions</span>
                {renderScoreBar(analysisResult.breakdown.naming * 10)}
              </div>
              <div className="breakdown-item">
                <span>Function Modularity</span>
                {renderScoreBar(analysisResult.breakdown.modularity * 5)}
              </div>
              <div className="breakdown-item">
                <span>Comments & Docs</span>
                {renderScoreBar(analysisResult.breakdown.comments * 5)}
              </div>
              <div className="breakdown-item">
                <span>Formatting</span>
                {renderScoreBar(analysisResult.breakdown.formatting * (100/15))}
              </div>
              <div className="breakdown-item">
                <span>Reusability</span>
                {renderScoreBar(analysisResult.breakdown.reusability * (100/15))}
              </div>
              <div className="breakdown-item">
                <span>Best Practices</span>
                {renderScoreBar(analysisResult.breakdown.best_practices * 5)}
              </div>
            </div>
          </div>

          <div className="recommendations-section">
            <h3>Recommendations</h3>
            <ul>
              {analysisResult.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;