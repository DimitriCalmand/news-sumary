import axios from 'axios';
import type { Article, TitlesResponse, TagCategoriesResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api/';

// Console log only once at startup
const globalAny = globalThis as any;
if (!globalAny.__API_DEBUG_LOGGED) {
  console.log('API_BASE_URL configured as:', API_BASE_URL);
  console.log('VITE_API_URL from env:', import.meta.env.VITE_API_URL);
  globalAny.__API_DEBUG_LOGGED = true;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add minimal error logging only
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message
    });
    return Promise.reject(error);
  }
);

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

  // Update article rating
  updateRating: async (id: number, rating: number): Promise<void> => {
    await api.put(`articles/${id}/rating`, { rating });
  },

  // Add reading time to article
  addReadingTime: async (id: number, seconds: number): Promise<void> => {
    await api.post(`articles/${id}/reading-time`, { seconds });
  },

  // Update article comments
  updateComments: async (id: number, comments: string): Promise<void> => {
    await api.put(`articles/${id}/comments`, { comments });
  },

  // Update article tags
  updateTags: async (id: number, tags: string[]): Promise<void> => {
    await api.put(`articles/${id}/tags`, { tags });
  },

  // Get all available tags
  getAllTags: async (): Promise<string[]> => {
    const response = await api.get('tags');
    return response.data.tags;
  },

  // Get organized tag categories
  getTagCategories: async (): Promise<TagCategoriesResponse> => {
    const response = await api.get('tags/categories');
    return response.data;
  },

  // Filter articles by tags and/or rating
  filterArticles: async (filters: { tags?: string[]; min_rating?: number }): Promise<Article[]> => {
    const params = new URLSearchParams();
    if (filters.tags) {
      filters.tags.forEach(tag => params.append('tags', tag));
    }
    if (filters.min_rating) {
      params.append('min_rating', filters.min_rating.toString());
    }

    const response = await api.get(`articles/filter?${params}`);
    return response.data;
  },
};