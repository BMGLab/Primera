import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const pipelineService = {
  
  runPipeline: async (params) => {
    try {
      
      const response = await axios.post(`${API_URL}/run`, params);
      return response.data;
    } catch (error) {
      console.error("Pipeline run error:", error);
      throw error;
    }
  },

  
  getDownloadLink: (runId, filename) => {
    return `${API_URL}/results/${runId}/${filename}`;
  }
};