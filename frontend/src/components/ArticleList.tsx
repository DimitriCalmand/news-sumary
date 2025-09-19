import { useQuery } from '@tanstack/react-query';
import { ExternalLink, RefreshCw } from 'lucide-react';
import { useState } from 'react';
import type { Article, ArticleTitle } from '../types';
import { newsApi } from '../utils/api';
import { ArticleFilters } from './ArticleFilters';
import { LoadingSpinner } from './LoadingSpinner';
import { PaginationControls } from './PaginationControls';
import { StarRating } from './StarRating';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

const ARTICLES_PER_PAGE = 20;

export function ArticleList() {
  const [currentPage, setCurrentPage] = useState(1);
  const [activeFilters, setActiveFilters] = useState<{ tags?: string[]; min_rating?: number }>({});
  const [filteredArticles, setFilteredArticles] = useState<Article[]>([]);
  const [showFiltered, setShowFiltered] = useState(false);

  // Query for total count
  const { data: totalCount, refetch: refetchCount } = useQuery({
    queryKey: ['articleCount'],
    queryFn: newsApi.getLength,
    staleTime: 0, // Force refresh
    refetchOnMount: true,
  });

  // Query for paginated titles (utilisé quand pas de filtres)
  const {
    data: titlesData,
    isLoading: isLoadingTitles,
    error: titlesError,
    refetch: refetchTitles
  } = useQuery({
    queryKey: ['articleTitles', currentPage],
    queryFn: () => newsApi.getTitles(currentPage, ARTICLES_PER_PAGE),
    enabled: !!totalCount && !showFiltered,
    staleTime: 0, // Force refresh
    refetchOnMount: true,
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
    staleTime: 0, // Force refresh
    refetchOnMount: true,
  });

  const handleFiltersChange = (filters: { tags?: string[]; min_rating?: number }) => {
    setActiveFilters(filters);
    const hasFilters = (filters.tags && filters.tags.length > 0) ||
      (filters.min_rating && filters.min_rating > 0);
    setShowFiltered(!!hasFilters);
    setCurrentPage(1); // Reset to first page when filters change

    if (hasFilters) {
      setFilteredArticles([]);
    }
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
  const currentData = showFiltered ? filteredData : titlesData?.titles;

  // Pour les articles filtrés, on gère la pagination côté client
  const getPaginatedFilteredArticles = () => {
    if (!filteredData) return [];
    const startIndex = (currentPage - 1) * ARTICLES_PER_PAGE;
    const endIndex = startIndex + ARTICLES_PER_PAGE;
    return filteredData.slice(startIndex, endIndex);
  };

  const getDisplayedArticles = () => {
    if (showFiltered) {
      return getPaginatedFilteredArticles();
    }
    return currentData || [];
  };

  const getTotalItemsCount = () => {
    if (showFiltered && filteredData) {
      return filteredData.length;
    }
    return totalCount || 0;
  };

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
            <Button onClick={handleRefresh} variant="outline" className="gap-2 self-start sm:self-auto">
              <RefreshCw className="h-4 w-4" />
              Actualiser
            </Button>
          </div>
        </div>

        {/* Filtres */}
        <div className="mb-6">
          <ArticleFilters onFiltersChange={handleFiltersChange} />
        </div>

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
              {getDisplayedArticles().map((article: ArticleTitle | Article) => (
                <Card key={article.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex flex-col gap-3">
                      <CardTitle className="text-lg line-clamp-2 leading-tight">
                        {article.title}
                      </CardTitle>
                      {/* Afficher rating et tags pour les articles filtrés */}
                      {showFiltered && 'rating' in article && (
                        <div className="flex items-center gap-4">
                          {article.rating && article.rating > 0 && (
                            <div className="flex items-center gap-2">
                              <StarRating rating={article.rating} readonly size="sm" />
                              <span className="text-sm text-slate-600">
                                ({article.rating}/5)
                              </span>
                            </div>
                          )}
                          {article.tags && article.tags.length > 0 && (
                            <div className="flex flex-wrap gap-1">
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
                      </div>
                      <Button
                        size="sm"
                        onClick={() => {
                          console.log('Clicking article with ID:', article.id);
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
            {getTotalItemsCount() > ARTICLES_PER_PAGE && (
              <PaginationControls
                currentPage={currentPage}
                totalItems={getTotalItemsCount()}
                itemsPerPage={ARTICLES_PER_PAGE}
                onPageChange={handlePageChange}
                className="mb-8"
              />
            )}
          </>
        )}

        {/* Empty state */}
        {!isLoading && getDisplayedArticles().length === 0 && (
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
    </div>
  );
}