import React, { useState, useEffect } from 'react';
import '../styles/styles.css';

export const ResultsScreen = ({ 
  guess, 
  wasCorrect, 
  questionsAsked, 
  statistics,
  onPlayAgain 
}) => {
  const [showTree, setShowTree] = useState(false);
  const [treeDisplay, setTreeDisplay] = useState('');
  const [saveStatus, setSaveStatus] = useState(null);

  useEffect(() => {
    const fetchTreePath = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/tree/path');
        const data = await response.json();
        if (data.path) {
          let treeStructure = 'Decision Tree Path:\n\n';
          
          data.path.forEach((step, index) => {
            if (step.answer === 'Guess') {
              // Final guess node
              treeStructure += `    └─[GUESS] ${step.question}\n`;
            } else {
              // Question nodes with branches
              const indent = '    '.repeat(index);
              const connector = index === 0 ? '○' : '├─';
              const branch = step.answer === 'Yes' ? 'YES─┐' : 'NO──┘';
              
              treeStructure += `${indent}${connector} [Q${index + 1}] ${step.question}\n`;
              treeStructure += `${indent}    └─> ${branch}\n`;
              
              if (index < data.path.length - 2) {
                treeStructure += `${indent}        |\n`;
              }
            }
          });
          
          setTreeDisplay(treeStructure);
        }
      } catch (error) {
        console.error('Error fetching tree path:', error);
      }
    };
    
    if (showTree) {
      fetchTreePath();
    }
  }, [showTree]);

  const handleSaveAsJSON = async () => {
    try {
      // Get current tree data
      const response = await fetch('http://localhost:5000/api/tree/data');
      const data = await response.json();
      
      // Create a blob with the tree and statistics
      const gameData = {
        guess,
        wasCorrect,
        questionsAsked,
        statistics,
        timestamp: new Date().toISOString(),
        tree: data.tree
      };
      
      const jsonString = JSON.stringify(gameData, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `pseudoqui-game-${Date.now()}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      setSaveStatus('Saved!');
      setTimeout(() => setSaveStatus(null), 2000);
    } catch (error) {
      setSaveStatus('Error saving file');
    }
  };

  const score = Math.max(0, 100 - (questionsAsked * 10));

  return (
    <div className="results-container">
      <div className="results-card">
        <div className="results-header">
          <h1 className="results-title">Game Over!</h1>
          <div className="results-status">
            {wasCorrect ? (
              <div className="status-win">
                <p className="status-text">I Won!</p>
                <p className="guess-text">You were thinking of:</p>
                <p className="guess-animal">{guess}</p>
              </div>
            ) : (
              <div className="status-loss">
                <p className="status-text">I Lost!</p>
                <p className="guess-text">I guessed: {guess}</p>
              </div>
            )}
          </div>
        </div>

        <div className="results-stats">
          <div className="stat-box">
            <p className="stat-label">Questions Asked</p>
            <p className="stat-value">{questionsAsked}</p>
          </div>
          <div className="stat-box">
            <p className="stat-label">Score</p>
            <p className="stat-value">{score}</p>
          </div>
          {statistics && statistics.tree && (
            <div className="stat-box">
              <p className="stat-label">Animals Known</p>
              <p className="stat-value">{statistics.tree.leaf_count}</p>
            </div>
          )}
        </div>

        {statistics && statistics.games && (
          <div className="game-statistics">
            <h3 className="stats-title">Game Statistics</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <p className="stat-label">Total Games</p>
                <p className="stat-value">{statistics.games.total}</p>
              </div>
              <div className="stat-item">
                <p className="stat-label">Win Rate</p>
                <p className="stat-value">{statistics.games.success_rate.toFixed(1)}%</p>
              </div>
              <div className="stat-item">
                <p className="stat-label">Correct Guesses</p>
                <p className="stat-value">{statistics.games.correct_guesses}</p>
              </div>
              <div className="stat-item">
                <p className="stat-label">Wrong Guesses</p>
                <p className="stat-value">{statistics.games.incorrect_guesses}</p>
              </div>
              <div className="stat-item">
                <p className="stat-label">Avg Questions</p>
                <p className="stat-value">{statistics.games.average_questions_per_game}</p>
              </div>
              <div className="stat-item">
                <p className="stat-label">Tree Height</p>
                <p className="stat-value">{statistics.tree.height}</p>
              </div>
            </div>
          </div>
        )}

        {statistics && (
          <>
            <button 
              className="retro-btn toggle-tree-btn"
              onClick={() => setShowTree(!showTree)}
            >
              {showTree ? 'Hide Decision Path' : 'Show Decision Path'}
            </button>

            {showTree && (
              <div className="tree-display-results">
                <h3>Current Tree Structure</h3>
                <pre className="tree-text">
                  {treeDisplay || 'Loading tree...'}
                </pre>
              </div>
            )}
          </>
        )}

        <div className="results-actions">
          <button 
            className="retro-btn btn-primary"
            onClick={handleSaveAsJSON}
          >
            Save as JSON
          </button>
          <button 
            className="retro-btn btn-secondary"
            onClick={onPlayAgain}
          >
            Play Again
          </button>
        </div>

        {saveStatus && (
          <div className="save-status">{saveStatus}</div>
        )}
      </div>
    </div>
  );
};
