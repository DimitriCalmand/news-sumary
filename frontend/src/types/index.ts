export interface Article {
  id: number;
  title: string;
  url: string;
  content: string;
  has_been_pretreat: boolean;
}

export interface ArticleTitle {
  id: number;
  title: string;
  url: string;
  has_been_pretreat: boolean;
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