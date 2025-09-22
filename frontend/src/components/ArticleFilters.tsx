import { Filter, Star, Tag, X, ChevronDown, ChevronRight } from 'lucide-react';
import { useEffect, useState } from 'react';
import { newsApi } from '../utils/api';
import type { TagCategoriesResponse } from '../types';
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
    const [tagCategories, setTagCategories] = useState<TagCategoriesResponse | null>(null);
    const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());

    // Charger les catégories de tags
    useEffect(() => {
        const loadTagCategories = async () => {
            try {
                const categories = await newsApi.getTagCategories();
                console.log('Categories loaded:', categories);
                setTagCategories(categories);
                // Expand categories that have tags by default
                const initialExpanded = new Set<string>();
                Object.entries(categories.categories).forEach(([key, category]) => {
                    console.log(`Category ${key}:`, category);
                    // Expand if main tag exists OR if sub_tags exist
                    if (category.has_main || category.sub_tags.length > 0) {
                        initialExpanded.add(key);
                    }
                });
                console.log('Initial expanded:', initialExpanded);
                setExpandedCategories(initialExpanded);
            } catch (error) {
                console.error('Error loading tag categories:', error);
            }
        };
        loadTagCategories();
    }, []);

    // Notifier les changements de filtres (seulement si il y a vraiment des filtres)
    useEffect(() => {
        const filters: { tags?: string[]; min_rating?: number } = {};

        if (selectedTags.length > 0) {
            filters.tags = selectedTags;
        }
        if (minRating > 0) {
            filters.min_rating = minRating;
        }

        // Seulement notifier si il y a des filtres ou si on reset à vide
        onFiltersChange?.(filters);
    }, [selectedTags, minRating]); // Supprimé onFiltersChange des dépendances

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

    const toggleCategory = (categoryKey: string) => {
        setExpandedCategories(prev => {
            const newSet = new Set(prev);
            if (newSet.has(categoryKey)) {
                newSet.delete(categoryKey);
            } else {
                newSet.add(categoryKey);
            }
            return newSet;
        });
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

                        {tagCategories && (
                            <div className="space-y-4">
                                {/* Tags fréquents (BASIC_TAGS) */}
                                {tagCategories.basic_tags.length > 0 && (
                                    <div>
                                        <p className="text-sm font-medium text-slate-700 mb-2">Tags fréquents :</p>
                                        <div className="flex flex-wrap gap-2">
                                            {tagCategories.basic_tags.map((tag) => (
                                                <button
                                                    key={tag}
                                                    onClick={() => handleTagToggle(tag)}
                                                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                                                        selectedTags.includes(tag)
                                                            ? 'bg-green-100 text-green-800 ring-2 ring-green-200'
                                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                    }`}
                                                >
                                                    {tag}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Categories IA et Politique */}
                                {Object.entries(tagCategories.categories).map(([categoryKey, category]) => (
                                    <div key={categoryKey} className="border border-slate-200 rounded-lg">
                                        <button
                                            onClick={() => toggleCategory(categoryKey)}
                                            className="w-full px-3 py-2 flex items-center justify-between text-left hover:bg-slate-50 rounded-t-lg"
                                        >
                                            <span className="font-medium text-slate-700 capitalize">
                                                {categoryKey === 'ia' ? 'IA' : categoryKey === 'politique' ? 'Politique' : categoryKey}
                                            </span>
                                            {expandedCategories.has(categoryKey) ? 
                                                <ChevronDown className="h-4 w-4" /> : 
                                                <ChevronRight className="h-4 w-4" />
                                            }
                                        </button>
                                        {expandedCategories.has(categoryKey) && (
                                            <div className="p-3 border-t border-slate-200">
                                                <div className="flex flex-wrap gap-2">
                                                    {/* Main tag */}
                                                    {category.has_main && (
                                                        <button
                                                            onClick={() => handleTagToggle(category.main_tag)}
                                                            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                                                                selectedTags.includes(category.main_tag)
                                                                    ? 'bg-blue-100 text-blue-800 ring-2 ring-blue-200'
                                                                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                                                            }`}
                                                        >
                                                            {category.main_tag} (principal)
                                                        </button>
                                                    )}
                                                    {/* Sub tags */}
                                                    {category.sub_tags.map((tag) => (
                                                        <button
                                                            key={tag}
                                                            onClick={() => handleTagToggle(tag)}
                                                            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                                                                selectedTags.includes(tag)
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
                                    </div>
                                ))}

                                {/* Autres tags (non catégorisés) */}
                                {tagCategories.other_tags.length > 0 && (
                                    <div>
                                        <p className="text-sm font-medium text-slate-700 mb-2">Autres tags :</p>
                                        <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto">
                                            {tagCategories.other_tags.map((tag) => (
                                                <button
                                                    key={tag}
                                                    onClick={() => handleTagToggle(tag)}
                                                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                                                        selectedTags.includes(tag)
                                                            ? 'bg-purple-100 text-purple-800 ring-2 ring-purple-200'
                                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                    }`}
                                                >
                                                    {tag}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                )}
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