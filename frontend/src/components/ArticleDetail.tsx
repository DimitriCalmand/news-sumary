import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { newsApi } from '../utils/api';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { LoadingSpinner } from './LoadingSpinner';
import { ArrowLeft, ExternalLink, RefreshCw } from 'lucide-react';

export function ArticleDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const articleId = id ? parseInt(id, 10) : 0;

  const { 
    data: article, 
    isLoading, 
    error, 
    refetch 
  } = useQuery({
    queryKey: ['article', articleId],
    queryFn: () => newsApi.getArticle(articleId),
    enabled: !!articleId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-slate-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <Button variant="outline" onClick={() => navigate('/')} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Retour à la liste
            </Button>
          </div>
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-red-600 mb-4">Article introuvable</h2>
            <p className="text-slate-600 mb-6">
              L'article demandé n'existe pas ou n'a pas pu être chargé.
            </p>
            <div className="flex gap-3 justify-center">
              <Button onClick={() => refetch()} variant="outline" className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Réessayer
              </Button>
              <Link to="/">
                <Button>Retour à la liste</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Navigation */}
        <div className="mb-6">
          <Button variant="outline" onClick={() => navigate('/')} className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Retour à la liste
          </Button>
        </div>

        {/* Article */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex flex-col gap-4">
              <CardTitle className="text-2xl lg:text-3xl leading-tight">
                {article.title}
              </CardTitle>
              <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
                <div className="flex items-center gap-3">
                  {article.has_been_pretreat && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800 font-medium">
                      Traité
                    </span>
                  )}
                  <a 
                    href={article.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors font-medium"
                  >
                    Voir la source originale <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="prose prose-slate max-w-none">
              {article.content.split('\n').map((paragraph, index) => (
                paragraph.trim() && (
                  <p key={index} className="mb-4 text-slate-700 leading-relaxed">
                    {paragraph}
                  </p>
                )
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 sm:justify-between">
          <Button variant="outline" onClick={() => navigate('/')} className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Retour à la liste
          </Button>
          <a 
            href={article.url} 
            target="_blank" 
            rel="noopener noreferrer"
          >
            <Button className="gap-2 w-full sm:w-auto">
              Lire l'article complet <ExternalLink className="h-4 w-4" />
            </Button>
          </a>
        </div>
      </div>
    </div>
  );
}