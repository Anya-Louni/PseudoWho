import create from 'zustand';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const useGameStore = create((set, get) => ({
  // State
  gameStarted: false,
  currentQuestion: '',
  questionsAsked: 0,
  reachedGuess: false,
  currentGuess: '',
  gameHistory: [],
  statistics: null,
  allAnimals: [],
  loading: false,
  error: null,

  // Actions
  startGame: async () => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/game/start`);
      if (response.data.success) {
        set({
          gameStarted: true,
          currentQuestion: response.data.question,
          questionsAsked: 0,
          reachedGuess: false,
        });
      }
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  answerQuestion: async (answer) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/game/answer`, { answer });
      if (response.data.success) {
        const newState = {
          questionsAsked: response.data.questions_asked,
          reachedGuess: response.data.reached_guess,
        };
        if (response.data.reached_guess) {
          newState.currentGuess = response.data.guess;
        } else {
          newState.currentQuestion = response.data.question;
        }
        set(newState);
      }
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  submitGuessResult: async (wasCorrect, actualAnimal) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/game/guess-result`, {
        was_correct: wasCorrect,
        actual_animal: actualAnimal,
      });
      if (response.data.success) {
        set({ error: null });
      }
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  learnNewAnimal: async (newAnimal, question, answerForNew) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/game/learn`, {
        new_animal: newAnimal,
        question: question,
        answer_for_new: answerForNew,
      });
      if (response.data.success) {
        set({ gameStarted: false });
        await get().fetchStatistics();
        await get().fetchAnimals();
      }
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  endGame: async () => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/game/end`);
      if (response.data.success) {
        set({ gameStarted: false });
      }
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ loading: false });
    }
  },

  fetchStatistics: async () => {
    try {
      const response = await axios.get(`${API_BASE}/stats`);
      if (response.data.success) {
        set({ statistics: response.data.statistics });
      }
    } catch (error) {
      set({ error: error.message });
    }
  },

  fetchAnimals: async () => {
    try {
      const response = await axios.get(`${API_BASE}/animals`);
      if (response.data.success) {
        set({ allAnimals: response.data.animals });
      }
    } catch (error) {
      set({ error: error.message });
    }
  },

  reset: () => set({
    gameStarted: false,
    currentQuestion: '',
    questionsAsked: 0,
    reachedGuess: false,
    currentGuess: '',
    error: null,
  }),
}));
