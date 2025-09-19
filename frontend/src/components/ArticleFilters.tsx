import { Filter, Star, Tag, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { newsApi } from '../utils/api';
import { StarRating } from './StarRating';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

interface ArticleFiltersProps {
    onFiltersChange?: (filters: { tags?: string[]; min_rating?: number }) => void;
    className?: string;
}

export function ArticleFilters({ onFiltersChange, className = '' }: ArticleFiltersProps) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [minRating, setMinRating] = useState<number>(0);
    const [availableTags, setAvailableTags] = useState<string[]>([]);
    const [popularTags, setPopularTags] = useState<string[]>([]);

    // Charger les tags disponibles
    useEffect(() => {
        const loadTags = async () => {
            try {
                const tags = await newsApi.getAllTags();
                setAvailableTags(tags);
                // Prendre les 8 premiers tags comme "populaires"
                setPopularTags(tags.slice(0, 8));
            } catch (error) {
                console.error('Error loading tags:', error);
            }
        };
        loadTags();
    }, []);

    // Notifier les changements de filtres
    useEffect(() => {
        const filters: { tags?: string[]; min_rating?: number } = {};
        if (selectedTags.length > 0) {
            filters.tags = selectedTags;
        }
        if (minRating > 0) {
            filters.min_rating = minRating;
        }
        onFiltersChange?.(filters);
    }, [selectedTags, minRating, onFiltersChange]);

    const handleTagToggle = (tag: string) => {
        setSelectedTags(prev =>
            prev.includes(tag)
                ? prev.filter(t => t !== tag)
                : [...prev, tag]
        );
    };

    const handleRatingChange = (rating: number) => {
        setMinRating(rating === minRating ? 0 : rating);
    };

    const clearFilters = () => {
        setSelectedTags([]);
        setMinRating(0);
    };

    const hasActiveFilters = selectedTags.length > 0 || minRating > 0;

    return (
        <Card className={className}>
            <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <Filter className="h-5 w-5" />
                        Filtres
                        {hasActiveFilters && (
                            <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                {selectedTags.length + (minRating > 0 ? 1 : 0)}
                            </span>
                        )}
                    </CardTitle>
                    <div className="flex items-center gap-2">
                        {hasActiveFilters && (
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={clearFilters}
                                className="gap-2"
                            >
                                <X className="h-4 w-4" />
                                Effacer
                            </Button>
                        )}
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setIsExpanded(!isExpanded)}
                        >
                            {isExpanded ? 'Réduire' : 'Étendre'}
                        </Button>
                    </div>
                </div>
            </CardHeader>

            {isExpanded && (
                <CardContent className="space-y-6">
                    {/* Rating Filter */}
                    <div>
                        <h4 className="text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
                            <Star className="h-4 w-4" />
                            Note minimale
                        </h4>
                        <div className="flex items-center gap-3">
                            <StarRating
                                rating={minRating}
                                onRatingChange={handleRatingChange}
                                size="md"
                            />
                            <span className="text-sm text-slate-600">
                                {minRating > 0 ? `${minRating}+ étoiles` : 'Toutes les notes'}
                            </span>
                        </div>
                    </div>

                    {/* Tags Filter */}
                    <div>
                        <h4 className="text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
                            <Tag className="h-4 w-4" />
                            Tags ({selectedTags.length} sélectionné{selectedTags.length !== 1 ? 's' : ''})
                        </h4>

                        {/* Popular Tags */}
                        {popularTags.length > 0 && (
                            <div className="mb-3">
                                <p className="text-xs text-slate-500 mb-2">Tags populaires :</p>
                                <div className="flex flex-wrap gap-2">
                                    {popularTags.map((tag) => (
                                        <button
                                            key={tag}
                                            onClick={() => handleTagToggle(tag)}
                                            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${selectedTags.includes(tag)
                                                    ? 'bg-blue-100 text-blue-800 ring-2 ring-blue-200'
                                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                }`}
                                        >
                                            {tag}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* All Tags */}
                        {availableTags.length > popularTags.length && (
                            <div>
                                <p className="text-xs text-slate-500 mb-2">Tous les tags :</p>
                                <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                                    {availableTags
                                        .filter(tag => !popularTags.includes(tag))
                                        .map((tag) => (
                                            <button
                                                key={tag}
                                                onClick={() => handleTagToggle(tag)}
                                                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${selectedTags.includes(tag)
                                                        ? 'bg-blue-100 text-blue-800 ring-2 ring-blue-200'
                                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                    }`}
                                            >
                                                {tag}
                                            </button>
                                        ))}
                                </div>
                            </div>
                        )}

                        {/* Selected Tags Summary */}
                        {selectedTags.length > 0 && (
                            <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                                <p className="text-sm font-medium text-blue-800 mb-2">
                                    Tags sélectionnés :
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {selectedTags.map((tag) => (
                                        <span
                                            key={tag}
                                            className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                                        >
                                            {tag}
                                            <button
                                                onClick={() => handleTagToggle(tag)}
                                                className="hover:bg-blue-200 rounded-full p-0.5"
                                            >
                                                <X className="h-3 w-3" />
                                            </button>
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </CardContent>
            )}
        </Card>
    );
}