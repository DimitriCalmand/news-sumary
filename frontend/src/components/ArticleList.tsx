import type { ArticleTitle } from '../types';
import { newsApi } from '../utils/api';
import { useQuery } from '@tanstack/react-query';
import { ExternalLink, RefreshCw } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { LoadingSpinner } from './LoadingSpinner';
import { PaginationControls } from './PaginationControls';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

const ARTICLES_PER_PAGE = 20;

export function ArticleList() {
  const [currentPage, setCurrentPage] = useState(1);

  // Query for total count
  const { data: totalCount, refetch: refetchCount } = useQuery({
    queryKey: ['articleCount'],
    queryFn: newsApi.getLength,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Query for paginated titles
  const {
    data: titlesData,
    isLoading,
    error,
    refetch: refetchTitles
  } = useQuery({
    queryKey: ['articleTitles', currentPage],
    queryFn: () => newsApi.getTitles(currentPage, ARTICLES_PER_PAGE),
    enabled: !!totalCount,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleRefresh = async () => {
    await Promise.all([refetchCount(), refetchTitles()]);
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
                {totalCount ? `${totalCount} articles disponibles` : 'Chargement...'}
              </p>
            </div>
            <Button onClick={handleRefresh} variant="outline" className="gap-2 self-start sm:self-auto">
              <RefreshCw className="h-4 w-4" />
              Actualiser
            </Button>
          </div>
        </div>

        {/* Loading state */}
        {isLoading && (
          <div className="flex justify-center py-12">
            <LoadingSpinner />
          </div>
        )}

        {/* Articles list */}
        {titlesData?.titles && (
          <>
            <div className="grid gap-4 mb-8">
              {titlesData.titles.map((article: ArticleTitle) => (
                <Card key={article.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg line-clamp-2 leading-tight">
                      {article.title}
                    </CardTitle>
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
                      <Link to={`/article/${article.id}`}>
                        <Button size="sm">
                          Lire l'article
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            {totalCount && totalCount > ARTICLES_PER_PAGE && (
              <PaginationControls
                currentPage={currentPage}
                totalItems={totalCount}
                itemsPerPage={ARTICLES_PER_PAGE}
                onPageChange={handlePageChange}
                className="mb-8"
              />
            )}
          </>
        )}

        {/* Empty state */}
        {titlesData?.titles && titlesData.titles.length === 0 && (
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold text-slate-600 mb-2">
              Aucun article disponible
            </h2>
            <p className="text-slate-500 mb-6">
              Il n'y a actuellement aucun article à afficher.
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