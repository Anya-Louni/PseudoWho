import React, { useState, useEffect } from 'react';
import { MenuScreen } from './components/MenuScreen';
import { GameScreen } from './components/GameScreen';
import { StatisticsScreen } from './components/StatisticsScreen';
import { useGameStore } from './hooks/useGameStore';
import './styles/styles.css';

function App() {
  const [currentScreen, setCurrentScreen] = useState('menu');
  const { startGame, reset } = useGameStore();

  const handlePlayClick = async () => {
    await startGame();
    setCurrentScreen('game');
  };

  const handleStatsClick = () => {
    setCurrentScreen('stats');
  };

  const handleQuitClick = () => {
    window.close();
  };

  const handleBackToMenu = () => {
    reset();
    setCurrentScreen('menu');
  };

  return (
    <div className="app">
      {currentScreen === 'menu' && (
        <MenuScreen
          onPlayClick={handlePlayClick}
          onStatsClick={handleStatsClick}
          onQuitClick={handleQuitClick}
        />
      )}
      {currentScreen === 'game' && <GameScreen />}
      {currentScreen === 'stats' && (
        <div style={{ width: '100%' }}>
          <StatisticsScreen />
          <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <button
              onClick={handleBackToMenu}
              style={{
                padding: '10px 30px',
                background: 'white',
                color: 'var(--primary-color)',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '1em',
                boxShadow: '0 5px 15px rgba(0, 0, 0, 0.1)'
              }}
            >
              ← Back to Menu
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
