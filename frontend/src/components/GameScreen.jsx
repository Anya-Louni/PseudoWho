import '../styles/styles.css';
import React, { useState, useEffect } from 'react';
import { useGameStore } from '../hooks/useGameStore';
import { FiCheck, FiX, FiLoader } from 'react-icons/fi';
import { ResultsScreen } from './ResultsScreen';
import { LearnAnimalForm } from './LearnAnimalForm';

export const GameScreen = ({ onReturnToMenu }) => {
  const {
    currentQuestion,
    questionsAsked,
    reachedGuess,
    currentGuess,
    loading,
    error,
    answerQuestion,
    submitGuessResult,
    reset,
    startGame,
  } = useGameStore();

  const [showGuessResult, setShowGuessResult] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showLearning, setShowLearning] = useState(false);
  const [wasCorrect, setWasCorrect] = useState(null);
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    if (wasCorrect !== null && !showLearning) {
      // Fetch statistics for results screen
      const fetchStats = async () => {
        try {
          const response = await fetch('http://localhost:5000/api/stats');
          const data = await response.json();
          setStatistics(data.statistics);
          setShowResults(true); // Show results AFTER stats are loaded
        } catch (err) {
          console.error('Error fetching statistics:', err);
          setShowResults(true); // Show results even if stats fail
        }
      };
      fetchStats();
    }
  }, [wasCorrect, showLearning]);

  const handleAnswer = async (answer) => {
    console.log(`>>> FRONTEND SENDING ANSWER: '${answer}' <<<`);
    await answerQuestion(answer);
  };

  const handleGuessCorrect = () => {
    submitGuessResult(true);
    setWasCorrect(true); // This triggers the useEffect
  };

  const handleGuessWrong = () => {
    submitGuessResult(false);
    setShowLearning(true); // Show learning form
  };

  const handleLearningComplete = async () => {
    // Reset all state and start a new game
    setShowLearning(false);
    setShowGuessResult(false);
    setShowResults(false);
    setWasCorrect(null);
    setStatistics(null);
    reset();
    await startGame();
  };

  const handlePlayAgain = async () => {
    // Reset all state and start a new game
    setShowResults(false);
    setShowGuessResult(false);
    setShowLearning(false);
    setWasCorrect(null);
    setStatistics(null);
    reset();
    await startGame();
  };

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={handlePlayAgain}>Try Again</button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="loading-container">
        <FiLoader className="spinner" />
        <p>Thinking...</p>
      </div>
    );
  }

  if (showResults && statistics) {
    return (
      <ResultsScreen
        guess={currentGuess}
        wasCorrect={wasCorrect}
        questionsAsked={questionsAsked}
        statistics={statistics}
        onPlayAgain={handlePlayAgain}
        onReturnToMenu={onReturnToMenu}
      />
    );
  }

  if (showLearning) {
    return (
      <div className="result-container failure">
        <LearnAnimalForm onLearned={handleLearningComplete} wrongGuess={currentGuess} />
      </div>
    );
  }

  if (showGuessResult) {
    if (wasCorrect) {
      return (
        <div className="result-container success">
          <h1>Excellent!</h1>
          <p>I guessed correctly!</p>
          <p className="guess-text">You were thinking of a {currentGuess}</p>
        </div>
      );
    }
  }

  if (reachedGuess) {
    return (
      <div className="game-screen">
        <div className="question-card guess-card">
          <h2>Is it a {currentGuess}?</h2>
          <div className="answer-buttons">
            <button
              onClick={handleGuessCorrect}
              className="retro-btn btn-yes"
              disabled={loading}
            >
              <FiCheck /> Yes!
            </button>
            <button
              onClick={handleGuessWrong}
              className="retro-btn btn-no"
              disabled={loading}
            >
              <FiX /> No
            </button>
          </div>
        </div>
        <div className="question-counter">
          Asked {questionsAsked} question{questionsAsked !== 1 ? 's' : ''}
        </div>
      </div>
    );
  }

  return (
    <div className="game-screen">
      <div className="question-card">
        <h2>{currentQuestion}</h2>
        <div className="answer-buttons">
          <button
            onClick={() => handleAnswer('yes')}
            className="retro-btn btn-yes"
            disabled={loading}
          >
            Yes
          </button>
          <button
            onClick={() => handleAnswer('no')}
            className="retro-btn btn-no"
            disabled={loading}
          >
            No
          </button>
        </div>
      </div>
      <div className="question-counter">
        Questions asked: {questionsAsked}
      </div>
    </div>
  );
};
