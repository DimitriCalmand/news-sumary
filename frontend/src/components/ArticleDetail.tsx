import { useQuery, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, ExternalLink, RefreshCw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSharedChat } from '../hooks/useSharedChat';
import { newsApi } from '../utils/api';
import { ArticleChat } from './ArticleChat';
import { AutoReadingTimer } from './AutoReadingTimer';
import { ChatModal } from './ChatModal';
import { CommentsEditor } from './CommentsEditor';
import { FloatingChatButton } from './FloatingChatButton';
import { LoadingSpinner } from './LoadingSpinner';
import { MarkdownRenderer } from './MarkdownRenderer';
import { StarRating } from './StarRating';
import { TagsEditor } from './TagsEditor';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

export function ArticleDetail() {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const articleId = id ? parseInt(id, 10) : 0;
  const [isChatModalOpen, setIsChatModalOpen] = useState(false);
  
  // Shared chat state
  const sharedChat = useSharedChat(articleId.toString());

  console.log('ArticleDetail - URL id:', id, 'parsed articleId:', articleId);

  // Validation de l'ID
  if (!id || isNaN(articleId) || articleId < 0) {
    console.error('Invalid article ID:', id, articleId);
    return (
      <div className="min-h-screen bg-slate-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <Button variant="outline" onClick={() => window.location.href = '/'} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Retour à la liste
            </Button>
          </div>
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-red-600 mb-4">ID d'article invalide</h2>
            <p className="text-slate-600 mb-6">
              L'identifiant de l'article n'est pas valide: {id}
            </p>
            <Button onClick={() => window.location.href = '/'}>
              Retour à la liste
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Force refresh when articleId changes
  useEffect(() => {
    console.log('=== useEffect triggered ===');
    console.log('articleId:', articleId);
    console.log('articleId type:', typeof articleId);
    console.log('articleId >= 0:', articleId >= 0);
    console.log('!isNaN(articleId):', !isNaN(articleId));

    if (articleId >= 0) { // Changé de if (articleId) pour permettre 0
      console.log('Invalidating queries for articleId:', articleId);
      queryClient.invalidateQueries({ queryKey: ['article'] });
    }
  }, [articleId, queryClient]);

  const {
    data: article,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['article', articleId],
    queryFn: () => newsApi.getArticle(articleId),
    enabled: articleId >= 0 && !isNaN(articleId), // Autoriser l'ID 0
    staleTime: 0, // Toujours refetch
    refetchOnMount: true,
  });

  const handleRatingUpdate = async (rating: number) => {
    if (!article) return;
    try {
      await newsApi.updateRating(articleId, rating);
      // Invalider le cache pour recharger les données
      queryClient.invalidateQueries({ queryKey: ['article', articleId] });
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    } catch (error) {
      console.error('Error updating rating:', error);
    }
  };

  const handleReadingTimeUpdate = async (timeSpent: number) => {
    if (!article) return;
    try {
      await newsApi.addReadingTime(articleId, timeSpent);
      // Note: Pas besoin d'invalider le cache ici car on met à jour en continu
    } catch (error) {
      console.error('Error updating reading time:', error);
    }
  };

  const handleCommentsUpdate = async (comments: string) => {
    if (!article) return;
    try {
      await newsApi.updateComments(articleId, comments);
      // Invalider le cache pour recharger les données
      queryClient.invalidateQueries({ queryKey: ['article', articleId] });
    } catch (error) {
      console.error('Error updating comments:', error);
    }
  };

  const handleTagsUpdate = async (tags: string[]) => {
    if (!article) return;
    try {
      await newsApi.updateTags(articleId, tags);
      // Invalider le cache pour recharger les données
      queryClient.invalidateQueries({ queryKey: ['article', articleId] });
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    } catch (error) {
      console.error('Error updating tags:', error);
    }
  };

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
    console.log('=== ARTICLE DETAIL ERROR ===');
    console.log('Error:', error);
    console.log('Article:', article);
    console.log('ArticleId:', articleId);
    console.log('URL id param:', id);
    console.log('IsLoading:', isLoading);

    return (
      <div className="min-h-screen bg-slate-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <Button variant="outline" onClick={() => window.location.href = '/'} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Retour à la liste
            </Button>
          </div>
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-red-600 mb-4">Article introuvable</h2>
            <p className="text-slate-600 mb-6">
              L'article demandé n'existe pas ou n'a pas pu être chargé.
            </p>
            <div className="bg-gray-100 p-4 rounded mb-4 text-left">
              <p><strong>Debug info:</strong></p>
              <p>URL ID: {id}</p>
              <p>Parsed ArticleId: {articleId}</p>
              <p>IsLoading: {isLoading ? 'true' : 'false'}</p>
              <p>Error: {error ? String(error) : 'No error'}</p>
              <p>Article: {article ? 'Found' : 'Not found'}</p>
            </div>
            <div className="flex gap-3 justify-center">
              <Button onClick={() => refetch()} variant="outline" className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Réessayer
              </Button>
              <Button onClick={() => window.location.href = '/'}>
                Retour à la liste
              </Button>
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
          <Button variant="outline" onClick={() => window.location.href = '/'} className="gap-2">
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
            <MarkdownRenderer
              content={article.content}
              className="min-h-0"
            />
          </CardContent>
        </Card>

        {/* Article Management */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Rating */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Évaluation</CardTitle>
            </CardHeader>
            <CardContent>
              <div>
                <h4 className="text-sm font-medium text-slate-700 mb-3">Noter cet article</h4>
                <StarRating
                  rating={article.rating || 0}
                  onRatingChange={handleRatingUpdate}
                  size="lg"
                />
              </div>
            </CardContent>
          </Card>

          {/* Auto Reading Timer */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Temps de lecture</CardTitle>
            </CardHeader>
            <CardContent>
              <AutoReadingTimer
                initialTime={article.time_spent || 0}
                onTimeUpdate={handleReadingTimeUpdate}
              />
            </CardContent>
          </Card>

          {/* Tags */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tags</CardTitle>
            </CardHeader>
            <CardContent>
              <TagsEditor
                initialTags={article.tags || []}
                onTagsChange={handleTagsUpdate}
              />
            </CardContent>
          </Card>
        </div>

        {/* Chat Section - Repositionné avant les commentaires */}
        <Card className="mb-8 border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <CardHeader className="bg-gradient-to-r from-blue-100 to-indigo-100 border-b border-blue-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-500 rounded-lg">
                  <span className="text-white text-lg">🤖</span>
                </div>
                <div>
                  <CardTitle className="text-lg text-blue-900">
                    Assistant IA pour cet article
                  </CardTitle>
                  <p className="text-sm text-blue-700 mt-1">
                    Posez vos questions sur le contenu de l'article
                  </p>
                </div>
              </div>
              <Button
                onClick={() => setIsChatModalOpen(true)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
              >
                💬 Ouvrir le chat
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-4">
            <ArticleChat
              articleId={articleId.toString()}
              articleTitle={article.title}
              sharedChat={sharedChat}
            />
          </CardContent>
        </Card>

        {/* Comments */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-lg">Mes commentaires</CardTitle>
          </CardHeader>
          <CardContent>
            <CommentsEditor
              initialComments={article.comments || ''}
              onSave={handleCommentsUpdate}
            />
          </CardContent>
        </Card>

        {/* Floating Chat Button */}
        <FloatingChatButton
          isOpen={isChatModalOpen}
          onClick={() => setIsChatModalOpen(!isChatModalOpen)}
          messageCount={sharedChat.messages.length}
        />

        {/* Chat Modal */}
        <ChatModal
          isOpen={isChatModalOpen}
          onClose={() => setIsChatModalOpen(false)}
          articleId={articleId.toString()}
          articleTitle={article.title}
          sharedChat={sharedChat}
        />

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 sm:justify-between">
          <Button variant="outline" onClick={() => window.location.href = '/'} className="gap-2">
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