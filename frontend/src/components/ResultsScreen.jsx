import React, { useState, useEffect } from 'react';
import '../styles/styles.css';

export const ResultsScreen = ({ 
  guess, 
  wasCorrect, 
  questionsAsked, 
  statistics,
  onPlayAgain,
  onReturnToMenu
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
          let treeStructure = 'Decision Tree Path (Your Journey):\n\n';
          
          data.path.forEach((step, index) => {
            if (step.answer === 'Guess') {
              // Final guess node
              treeStructure += `    └─[GUESS] ${step.question}\n`;
            } else {
              // Question nodes with BOTH branches
              const indent = '    '.repeat(index);
              const connector = index === 0 ? '○' : '├─';
              const chosenBranch = step.answer === 'Yes' ? 'YES' : 'NO';
              const otherBranch = step.answer === 'Yes' ? 'NO' : 'YES';
              
              treeStructure += `${indent}${connector} [Q${index + 1}] ${step.question}\n`;
              treeStructure += `${indent}    ├─> ${chosenBranch} ✓ (You chose this)\n`;
              treeStructure += `${indent}    └─> ${otherBranch} (Not taken)\n`;
              
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
        </div>

        <button 
          className="retro-btn btn-info"
          onClick={() => setShowTree(!showTree)}
          style={{ marginBottom: '20px', width: '100%' }}
        >
          {showTree ? 'Hide Decision Path' : 'Show Decision Path'}
        </button>

        {showTree && (
          <div className="tree-display-results">
            <h3>Your Decision Path</h3>
            <pre className="tree-text">
              {treeDisplay || 'Loading tree...'}
            </pre>
          </div>
        )}

        <div className="results-actions">
          <button 
            className="retro-btn btn-tertiary"
            onClick={handleSaveAsJSON}
          >
            Save as JSON
          </button>
          <button 
            className="retro-btn btn-primary"
            onClick={onPlayAgain}
          >
            Play Again
          </button>
          <button 
            className="retro-btn btn-secondary"
            onClick={onReturnToMenu}
          >
            Return to Menu
          </button>
        </div>

        {saveStatus && (
          <div className="save-status">{saveStatus}</div>
        )}
      </div>
    </div>
  );
};
