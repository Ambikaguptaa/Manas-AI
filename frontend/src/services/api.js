import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Fetch backend system health and verification metadata
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('API health check error:', error);
    throw error;
  }
};

/**
 * Fetch the 16 self-reflection questionnaire questions with scale guide
 */
export const getQuestions = async () => {
  try {
    const response = await apiClient.get('/assessment/questions');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch questions:', error);
    throw error;
  }
};

/**
 * Submit completed questionnaire responses to calculate feature scores,
 * run ML classification, derive IKS insights, and generate recommendations.
 * @param {Object|Array} responses - Key-value pair or array of responses (scale 1-5)
 */
export const submitAssessment = async (responses) => {
  try {
    const response = await apiClient.post('/assessment', {
      responses,
    });
    return response.data;
  } catch (error) {
    console.error('Failed to submit assessment:', error);
    throw error;
  }
};

export default apiClient;
