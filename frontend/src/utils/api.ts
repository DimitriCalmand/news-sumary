import axios from 'axios';
import type { Article, TitlesResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const newsApi = {
  // Get total count of articles
  getLength: async (): Promise<number> => {
    const response = await api.get('length');
    return response.data;
  },

  // Get paginated titles
  getTitles: async (page: number, perPage: number): Promise<TitlesResponse> => {
    const response = await api.post('titles', {
      page,
      per_page: perPage,
    });
    return response.data;
  },

  // Get full article by ID
  getArticle: async (id: number): Promise<Article> => {
    const response = await api.get(`article/${id}`);
    return response.data;
  },

  // Get untreated articles
  getUntreatArticles: async (): Promise<Article[]> => {
    const response = await api.get('unpretreat');
    return response.data;
  },
};