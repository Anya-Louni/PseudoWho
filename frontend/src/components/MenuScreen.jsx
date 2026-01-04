import React from 'react';
import { FiPlay, FiBarChart2, FiLogOut } from 'react-icons/fi';
import '../styles/styles.css';

export const MenuScreen = ({ onPlayClick, onStatsClick, onQuitClick }) => {
  return (
    <div className="menu-container">
      <div className="menu-card">
        <div className="title-section">
          <h1 className="main-title">PseudoQui</h1>
          <p className="subtitle">Guess the Animal Game</p>
          <p className="description">
            Can you think of an animal and let me guess what it is?
          </p>
        </div>

        <div className="menu-buttons">
          <button onClick={onPlayClick} className="retro-btn btn-primary">
            <FiPlay /> Play Game
          </button>
          <button onClick={onStatsClick} className="retro-btn btn-secondary">
            <FiBarChart2 /> View Statistics
          </button>
          <button onClick={onQuitClick} className="retro-btn btn-no">
            <FiLogOut /> Quit
          </button>
        </div>

        <div className="info-section">
          <h3>How to Play</h3>
          <ol>
            <li>Think of an animal (don't tell me!)</li>
            <li>I'll ask yes/no questions to narrow it down</li>
            <li>I'll make a guess when I think I know</li>
            <li>If I'm wrong, teach me the correct answer!</li>
          </ol>
        </div>
      </div>
    </div>
  );
};
