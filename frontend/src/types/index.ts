export interface Article {
  id: number;
  title: string;
  url: string;
  content: string;
  has_been_pretreat: boolean;
  rating?: number; // 1-5 stars
  time_spent: number; // seconds
  comments: string;
  tags: string[];
  source?: string; // Source de l'article (TechCrunch, France Info, etc.)
  scraped_date?: string; // Date et heure de scraping
  date?: string; // Date de publication ou de scraping (legacy)
}

export interface ArticleTitle {
  id: number;
  title: string;
  url: string;
  has_been_pretreat: boolean;
  rating?: number;
  time_spent: number;
  comments: string;
  tags: string[];
  source?: string; // Source de l'article (TechCrunch, France Info, etc.)
  scraped_date?: string; // Date et heure de scraping
  date?: string; // Date de publication ou de scraping (legacy)
}

export interface PaginationInfo {
  start: number;
  end: number;
  total: number;
  returned: number;
}

export interface TitlesResponse {
  titles: ArticleTitle[];
  pagination: PaginationInfo;
}

export interface ArticlesResponse {
  articles: Article[];
  pagination: PaginationInfo;
}

// Types pour les nouvelles API
export interface RatingUpdate {
  rating: number; // 1-5
}

// Types pour les catégories de tags
export interface TagCategory {
  main_tag: string;
  sub_tags: string[];
  has_main: boolean;
}

export interface TagCategoriesResponse {
  categories: {
    [categoryKey: string]: TagCategory;
  };
  basic_tags: string[];
  other_tags: string[];
}

export interface ReadingTimeUpdate {
  seconds: number;
}

export interface CommentsUpdate {
  comments: string;
}

export interface TagsUpdate {
  tags: string[];
}

export interface TagsResponse {
  tags: string[];
}

export interface FilterParams {
  tags?: string[];
  min_rating?: number;
}