import React, { useState, useEffect } from 'react';
import { useGameStore } from '../hooks/useGameStore';
import { FiBarChart2, FiAward, FiTrendingDown } from 'react-icons/fi';
import '../styles/styles.css';

export const StatisticsScreen = () => {
  const { statistics, fetchStatistics, allAnimals } = useGameStore();
  const [treeDisplay, setTreeDisplay] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      await fetchStatistics();
      await fetchTreeDisplay();
      setLoading(false);
    };
    fetchData();
  }, []);

  const fetchTreeDisplay = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/tree/display');
      const data = await response.json();
      if (data.success) {
        setTreeDisplay(data.tree);
      }
    } catch (error) {
      console.error('Error fetching tree display:', error);
    }
  };

  if (loading || !statistics) {
    return (
      <div className="loading-container">
        <p>Loading statistics...</p>
      </div>
    );
  }

  const { tree, games } = statistics;

  return (
    <div className="stats-container">
      <h1>Statistics & Analysis</h1>

      <div className="stats-grid">
        <div className="stat-card tree-stat">
          <h3>Tree Structure</h3>
          <div className="stat-items">
            <div className="stat-item">
              <span className="stat-label">Total Nodes:</span>
              <span className="stat-value">{tree.total_nodes}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Height:</span>
              <span className="stat-value">{tree.height}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Animals Known:</span>
              <span className="stat-value">{tree.leaf_count}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Avg Questions/Game:</span>
              <span className="stat-value">{tree.average_depth}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Balance Factor:</span>
              <span className="stat-value">{(tree.balance_factor * 100).toFixed(0)}%</span>
            </div>
          </div>
        </div>

        <div className="stat-card game-stat">
          <h3>Game Statistics</h3>
          <div className="stat-items">
            <div className="stat-item">
              <span className="stat-label">Total Games:</span>
              <span className="stat-value">{games.total}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Correct Guesses:</span>
              <span className="stat-value success">{games.correct_guesses}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Incorrect Guesses:</span>
              <span className="stat-value error">{games.incorrect_guesses}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Success Rate:</span>
              <span className="stat-value">{games.success_rate.toFixed(1)}%</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Avg Questions/Game:</span>
              <span className="stat-value">{games.average_questions_per_game}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="animals-card">
        <h3>All Known Animals ({allAnimals.length})</h3>
        <div className="animals-list">
          {allAnimals.map((animal, index) => (
            <span key={index} className="animal-badge">
              {animal}
            </span>
          ))}
        </div>
      </div>

      <div className="tree-display">
        <h3>Tree Structure</h3>
        <pre className="tree-text">
          {treeDisplay}
        </pre>
      </div>

      <div className="insights">
        <h3>Insights</h3>
        <ul>
          <li>
            Current tree height of {tree.height} means up to {tree.height} questions to guess an animal
          </li>
          <li>
            System knows {tree.leaf_count} animals and can distinguish between them
          </li>
          <li>
            Balance factor of {(tree.balance_factor * 100).toFixed(0)}% suggests tree is {tree.balance_factor < 0.3 ? 'well-balanced' : 'could be optimized'}
          </li>
          <li>
            Success rate of {games.success_rate.toFixed(1)}% shows system learning effectiveness
          </li>
        </ul>
      </div>
    </div>
  );
};
