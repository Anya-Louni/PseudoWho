import React, { useState } from 'react';
import '../styles/styles.css';

export const LearnAnimalForm = ({ onLearned, wrongGuess }) => {
  const [animalName, setAnimalName] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('yes');
  const [step, setStep] = useState(1); // 1 = animal name, 2 = question
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleNextStep = () => {
    if (!animalName.trim()) {
      alert('Please enter an animal name!');
      return;
    }
    setStep(2);
  };

  const handleSubmit = async () => {
    if (!question.trim()) {
      alert('Please enter a discriminating question!');
      return;
    }

    setIsSubmitting(true);
    try {
      // Send the new animal with discriminating question to backend
      const response = await fetch('http://localhost:5000/api/game/learn', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          new_animal: animalName.trim(),
          question: question.trim(),
          answer_for_new: answer,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        alert(`Great! I've learned about ${animalName}!\n\nNow I know to ask: "${question}"\nAnswer YES for ${animalName}, NO for ${wrongGuess}`);
        onLearned();
      } else {
        alert(data.message || 'Failed to learn animal. Please try again.');
      }
    } catch (error) {
      console.error('Error learning animal:', error);
      alert('Error learning animal');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="learn-animal-form">
      <div className="learn-section">
        {step === 1 && (
          <>
            <h2>I got it wrong!</h2>
            <p className="wrong-guess">I guessed: <strong>{wrongGuess}</strong></p>
            <p className="prompt">What animal were you thinking of?</p>
            
            <input
              type="text"
              placeholder="Enter animal name (e.g., Kangaroo)"
              value={animalName}
              onChange={(e) => setAnimalName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleNextStep()}
              className="animal-input"
              disabled={isSubmitting}
              autoFocus
            />
            
            <div className="learn-buttons">
              <button
                onClick={handleNextStep}
                className="retro-btn btn-primary"
                disabled={!animalName.trim()}
              >
                Next
              </button>
              <button
                onClick={onLearned}
                className="retro-btn btn-secondary"
              >
                Skip
              </button>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <h2>Help me learn!</h2>
            <div className="comparison-box">
              <p><strong>Your animal:</strong> {animalName}</p>
              <p><strong>I guessed:</strong> {wrongGuess}</p>
            </div>
            
            <p className="prompt">What question would distinguish them?</p>
            <input
              type="text"
              placeholder="e.g., Does it jump on two legs?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              className="animal-input"
              disabled={isSubmitting}
              autoFocus
            />
            
            <p className="prompt small">For <strong>{animalName}</strong>, the answer is:</p>
            <div className="answer-selection">
              <label className={`answer-option ${answer === 'yes' ? 'selected' : ''}`}>
                <input
                  type="radio"
                  name="answer"
                  value="yes"
                  checked={answer === 'yes'}
                  onChange={(e) => setAnswer(e.target.value)}
                />
                <span>YES</span>
              </label>
              <label className={`answer-option ${answer === 'no' ? 'selected' : ''}`}>
                <input
                  type="radio"
                  name="answer"
                  value="no"
                  checked={answer === 'no'}
                  onChange={(e) => setAnswer(e.target.value)}
                />
                <span>NO</span>
              </label>
            </div>
            
            <div className="learn-buttons">
              <button
                onClick={() => setStep(1)}
                className="retro-btn btn-secondary"
                disabled={isSubmitting}
              >
                Back
              </button>
              <button
                onClick={handleSubmit}
                className="retro-btn btn-primary"
                disabled={isSubmitting || !question.trim()}
              >
                {isSubmitting ? 'Learning...' : 'Teach Me!'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
