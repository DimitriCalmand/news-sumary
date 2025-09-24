import { useQuery } from '@tanstack/react-query';
import { ExternalLink, RefreshCw, Settings } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { newsApi } from '../lib/api';
import { getRelativeTime } from '../utils/api';
import type { Article, ArticleTitle } from '../types';
import { ArticleFilters } from './ArticleFilters';
import { LoadingSpinner } from './LoadingSpinner';
import { PaginationControls } from './PaginationControls';
import SettingsModal from './SettingsModal';
import { StarRating } from './StarRating';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

const ARTICLES_PER_PAGE = 20;

// Fonction de similarité pour la recherche approximative
function calculateSimilarity(str1: string, str2: string): number {
  const longer = str1.length > str2.length ? str1 : str2;
  const shorter = str1.length > str2.length ? str2 : str1;
  
  if (longer.length === 0) return 1.0;
  
  const distance = levenshteinDistance(longer, shorter);
  return (longer.length - distance) / longer.length;
}

// Distance de Levenshtein simplifiée
function levenshteinDistance(str1: string, str2: string): number {
  const matrix = [];
  
  for (let i = 0; i <= str2.length; i++) {
    matrix[i] = [i];
  }
  
  for (let j = 0; j <= str1.length; j++) {
    matrix[0][j] = j;
  }
  
  for (let i = 1; i <= str2.length; i++) {
    for (let j = 1; j <= str1.length; j++) {
      if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1, // substitution
          matrix[i][j - 1] + 1,     // insertion
          matrix[i - 1][j] + 1      // deletion
        );
      }
    }
  }
  
  return matrix[str2.length][str1.length];
}

// Fonction de recherche floue
function fuzzySearch(title: string, searchTerm: string): boolean {
  const titleWords = title.toLowerCase().split(/\s+/);
  const searchWords = searchTerm.toLowerCase().split(/\s+/);
  
  // Si la recherche contient plusieurs mots, tous doivent matcher
  return searchWords.every(searchWord => {
    return titleWords.some(titleWord => {
      // Recherche exacte d'abord (plus rapide)
      if (titleWord.includes(searchWord)) return true;
      
      // Recherche approximative si la longueur est similaire
      if (Math.abs(titleWord.length - searchWord.length) <= 2) {
        const similarity = calculateSimilarity(titleWord, searchWord);
        return similarity >= 0.8; // 80% de similarité minimum
      }
      
      return false;
    });
  });
}

export function ArticleList() {
  const [currentPage, setCurrentPage] = useState(1);
  const [activeFilters, setActiveFilters] = useState<{ tags?: string[]; min_rating?: number }>({});
  const [showFiltered, setShowFiltered] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [sortBy, setSortBy] = useState<'date' | 'order'>('date');
  const [searchTerm, setSearchTerm] = useState('');

  // Query for total count
  const { data: totalCount, refetch: refetchCount } = useQuery({
    queryKey: ['articleCount'],
    queryFn: newsApi.getLength,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnMount: false,
    refetchOnWindowFocus: false,
  });

  // Query for paginated titles (utilisé quand pas de filtres)
  const {
    data: titlesData,
    isLoading: isLoadingTitles,
    error: titlesError,
    refetch: refetchTitles
  } = useQuery({
    queryKey: ['articleTitles', currentPage, sortBy, searchTerm],
    queryFn: () => {
      console.log('Fetching titles for page:', currentPage, 'sort:', sortBy, 'search:', searchTerm);
      return newsApi.getTitles(currentPage, ARTICLES_PER_PAGE, sortBy, searchTerm.trim() || undefined);
    },
    enabled: !showFiltered,
    staleTime: 0, // Pas de cache pour éviter les problèmes de pagination
    refetchOnMount: true,
    refetchOnWindowFocus: false,
  });

  // Query pour les articles filtrés
  const {
    data: filteredData,
    isLoading: isLoadingFiltered,
    error: filteredError,
    refetch: refetchFiltered
  } = useQuery({
    queryKey: ['filteredArticles', activeFilters],
    queryFn: () => newsApi.filterArticles(activeFilters),
    enabled: showFiltered && (Object.keys(activeFilters).length > 0),
    staleTime: 1 * 60 * 1000, // 1 minute
    refetchOnMount: false,
    refetchOnWindowFocus: false,
  });

  const handleFiltersChange = useCallback((filters: { tags?: string[]; min_rating?: number }) => {
    setActiveFilters(filters);
    const hasFilters = (filters.tags && filters.tags.length > 0) ||
      (filters.min_rating && filters.min_rating > 0);
    setShowFiltered(!!hasFilters);
    setCurrentPage(1); // Reset to first page when filters change
  }, []); // Pas de dépendances car on ne lit que les paramètres

  const handlePageChange = (page: number) => {
    console.log('Page change:', currentPage, '->', page);
    setCurrentPage(page);

    // Scroll après un petit délai pour laisser React faire le re-render
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  };

  const handleSortChange = (newSortBy: 'date' | 'order') => {
    console.log('Sort change:', sortBy, '->', newSortBy);
    setSortBy(newSortBy);
    setCurrentPage(1); // Reset to first page when sort changes
  };

  const handleRefresh = async () => {
    if (showFiltered) {
      await refetchFiltered();
    } else {
      await Promise.all([refetchCount(), refetchTitles()]);
    }
  };

  // Déterminer quelles données afficher
  const isLoading = showFiltered ? isLoadingFiltered : isLoadingTitles;
  const error = showFiltered ? filteredError : titlesError;

  // Mémoriser les calculs pour éviter les re-renders constants
  const allArticles = useMemo(() => {
    return showFiltered ? (filteredData || []) : (titlesData?.titles || []);
  }, [showFiltered, filteredData, titlesData?.titles]);

  const displayedArticles = useMemo(() => {
    if (showFiltered) {
      // Mode filtré : pagination côté client sur tous les articles filtrés
      let articles = allArticles;
      
      // Appliquer le filtre de recherche par titre
      if (searchTerm.trim()) {
        const term = searchTerm.toLowerCase().trim();
        articles = articles.filter((article: ArticleTitle) => 
          fuzzySearch(article.title, term)
        );
      }
      
      // Appliquer la pagination côté client
      const startIndex = (currentPage - 1) * ARTICLES_PER_PAGE;
      const endIndex = startIndex + ARTICLES_PER_PAGE;
      return articles.slice(startIndex, endIndex);
    } else {
      // Mode normal : les articles sont déjà paginés et filtrés par le backend
      return titlesData?.titles || [];
    }
  }, [showFiltered, allArticles, titlesData?.titles, searchTerm, currentPage]);

  // Effet pour remettre à la première page quand la recherche change
  useEffect(() => {
    if (searchTerm !== '') {
      setCurrentPage(1);
    }
  }, [searchTerm]);

  const totalItemsCount = useMemo(() => {
    if (showFiltered) {
      // Mode filtré : compter tous les articles filtrés
      let articles = allArticles;
      
      // Appliquer le filtre de recherche par titre pour le compte
      if (searchTerm.trim()) {
        const term = searchTerm.toLowerCase().trim();
        articles = articles.filter((article: ArticleTitle) => 
          fuzzySearch(article.title, term)
        );
      }
      
      return articles.length;
    } else {
      // Mode normal : utiliser le total retourné par le backend (qui tient compte de la recherche)
      return titlesData?.pagination?.total || totalCount || 0;
    }
  }, [showFiltered, allArticles, searchTerm, titlesData?.pagination?.total, totalCount]);

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-red-600 mb-4">Erreur de chargement</h2>
            <p className="text-slate-600 mb-6">
              Impossible de charger les articles. Vérifiez que le serveur backend est en cours d'exécution.
            </p>
            <Button onClick={handleRefresh} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Réessayer
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                Résumé de Nouvelles
              </h1>
              <p className="text-slate-600 mt-1">
                {showFiltered ? (
                  filteredData ? `${filteredData.length} article${filteredData.length !== 1 ? 's' : ''} trouvé${filteredData.length !== 1 ? 's' : ''}` : 'Recherche...'
                ) : (
                  totalCount ? `${totalCount} articles disponibles` : 'Chargement...'
                )}
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={() => setIsSettingsOpen(true)}
                variant="outline"
                className="gap-2"
                title="Paramètres"
              >
                <Settings className="h-4 w-4" />
                Paramètres
              </Button>
              <Button onClick={handleRefresh} variant="outline" className="gap-2 self-start sm:self-auto">
                <RefreshCw className="h-4 w-4" />
                Actualiser
              </Button>
            </div>
          </div>
        </div>

        {/* Recherche par titre */}
        <div className="mb-6">
          <div className="flex items-center gap-4">
            <div className="flex-1 max-w-md">
              <input
                type="text"
                placeholder="Rechercher dans les titres..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            {searchTerm && (
              <Button
                onClick={() => setSearchTerm('')}
                variant="outline"
                size="sm"
              >
                ✕ Effacer
              </Button>
            )}
          </div>
        </div>

        {/* Filtres */}
        <div className="mb-6">
          <ArticleFilters onFiltersChange={handleFiltersChange} />
        </div>

        {/* Contrôles de tri (uniquement quand pas de filtres actifs) */}
        {!showFiltered && (
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-slate-700">Trier par :</span>
              <div className="flex gap-2">
                <Button
                  onClick={() => handleSortChange('date')}
                  variant={sortBy === 'date' ? 'default' : 'outline'}
                  size="sm"
                  className="text-xs"
                >
                  📅 Plus récents
                </Button>
                <Button
                  onClick={() => handleSortChange('order')}
                  variant={sortBy === 'order' ? 'default' : 'outline'}
                  size="sm"
                  className="text-xs"
                >
                  🔢 Ordre d'arrivée
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="flex justify-center py-12">
            <LoadingSpinner />
          </div>
        )}

        {/* Articles list */}
        {!isLoading && (
          <>
            <div className="grid gap-4 mb-8">
              {displayedArticles.map((article: ArticleTitle | Article) => (
                <Card key={article.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex flex-col gap-3">
                      <CardTitle className="text-lg line-clamp-2 leading-tight">
                        {article.title}
                      </CardTitle>

                      {/* Afficher rating et commentaires pour tous les articles qui en ont */}
                      {'rating' in article && article.rating && article.rating > 0 && (
                        <div className="flex items-center gap-2">
                          <StarRating rating={article.rating} readonly size="sm" />
                          <span className="text-sm text-slate-600">
                            ({article.rating}/5)
                          </span>
                        </div>
                      )}

                      {/* Afficher les commentaires s'il y en a */}
                      {'comments' in article && article.comments && article.comments.trim() && (
                        <div className="p-2 bg-amber-50 border-l-4 border-amber-200 rounded-r">
                          <div className="flex items-start gap-2">
                            <span className="text-amber-600 text-sm font-medium">💭 Note :</span>
                            <p className="text-sm text-amber-800 line-clamp-2">
                              {article.comments}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
                      <div className="flex items-center gap-2 text-sm text-slate-500">
                        {article.has_been_pretreat && (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                            Traité
                          </span>
                        )}
                        <a
                          href={article.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          Source <ExternalLink className="h-3 w-3" />
                        </a>
                        {/* Tags à droite du lien Source */}
                        {article.tags && article.tags.length > 0 && (
                          <div className="flex flex-wrap gap-1 ml-2">
                            {article.tags.slice(0, 3).map((tag, index) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                              >
                                {tag}
                              </span>
                            ))}
                            {article.tags.length > 3 && (
                              <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                                +{article.tags.length - 3}
                              </span>
                            )}
                          </div>
                        )}
                        {/* Temps écoulé depuis l'ajout */}
                        {('date' in article || 'scraped_date' in article) && (
                          <span className="text-xs text-slate-500 ml-2">
                            📅 {getRelativeTime(article.scraped_date || article.date || '')}
                          </span>
                        )}
                      </div>
                      <Button
                        size="sm"
                        onClick={() => {
                          console.log('=== DEBUG CLICK ===');
                          console.log('Full article object:', article);
                          console.log('Article ID:', article.id);
                          console.log('Article ID type:', typeof article.id);
                          console.log('Target URL:', `/article/${article.id}`);

                          // Permettre l'ID 0 en vérifiant explicitement null/undefined
                          if (article.id === null || article.id === undefined || typeof article.id !== 'number') {
                            console.error('ERROR: Article ID is invalid!', article.id);
                            alert('Erreur: ID d\'article invalide');
                            return;
                          }

                          window.location.href = `/article/${article.id}`;
                        }}
                      >
                        Lire l'article
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            {((showFiltered && totalItemsCount > ARTICLES_PER_PAGE) || 
              (!showFiltered && totalCount && totalCount > ARTICLES_PER_PAGE)) && (
              <PaginationControls
                currentPage={currentPage}
                totalItems={showFiltered ? totalItemsCount : (totalCount || 0)}
                itemsPerPage={ARTICLES_PER_PAGE}
                onPageChange={handlePageChange}
                className="mb-8"
              />
            )}
          </>
        )}

        {/* Empty state */}
        {!isLoading && displayedArticles.length === 0 && (
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold text-slate-600 mb-2">
              {showFiltered ? 'Aucun article ne correspond aux critères' : 'Aucun article disponible'}
            </h2>
            <p className="text-slate-500 mb-6">
              {showFiltered
                ? 'Essayez de modifier vos filtres pour voir plus de résultats.'
                : 'Il n\'y a actuellement aucun article à afficher.'
              }
            </p>
            <Button onClick={handleRefresh} className="gap-2">
              <RefreshCw className="h-4 w-4" />
              Actualiser
            </Button>
          </div>
        )}
      </div>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={() => {
          // Optionally refetch data when settings are saved
          handleRefresh();
        }}
      />
    </div>
  );
}