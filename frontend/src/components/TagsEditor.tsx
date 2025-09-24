import { Plus, Tag, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Button } from './ui/Button';

interface TagsEditorProps {
    initialTags?: string[];
    availableTags?: string[];
    onTagsChange?: (tags: string[]) => void;
    className?: string;
}

export function TagsEditor({
    initialTags = [],
    availableTags = [],
    onTagsChange,
    className = ''
}: TagsEditorProps) {
    const [tags, setTags] = useState<string[]>(initialTags);
    const [newTag, setNewTag] = useState('');
    const [showInput, setShowInput] = useState(false);
    const [suggestions, setSuggestions] = useState<string[]>([]);

    // Update suggestions based on input
    useEffect(() => {
        if (newTag.length > 0) {
            const filtered = availableTags.filter(tag =>
                tag.toLowerCase().includes(newTag.toLowerCase()) &&
                !tags.includes(tag)
            );
            setSuggestions(filtered.slice(0, 5)); // Limit to 5 suggestions
        } else {
            setSuggestions([]);
        }
    }, [newTag, availableTags, tags]);

    const addTag = (tagToAdd: string) => {
        const cleanTag = tagToAdd.trim().toLowerCase();
        if (cleanTag && !tags.includes(cleanTag) && cleanTag.length <= 30) {
            const newTags = [...tags, cleanTag];
            setTags(newTags);
            if (onTagsChange) {
                onTagsChange(newTags);
            }
        }
        setNewTag('');
        setShowInput(false);
        setSuggestions([]);
    };

    const removeTag = (tagToRemove: string) => {
        const newTags = tags.filter(tag => tag !== tagToRemove);
        setTags(newTags);
        if (onTagsChange) {
            onTagsChange(newTags);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && newTag.trim()) {
            e.preventDefault();
            addTag(newTag);
        } else if (e.key === 'Escape') {
            setNewTag('');
            setShowInput(false);
            setSuggestions([]);
        }
    };

    const handleInputBlur = () => {
        // Small delay to allow clicking on suggestions
        setTimeout(() => {
            if (newTag.trim()) {
                addTag(newTag);
            } else {
                setShowInput(false);
                setSuggestions([]);
            }
        }, 150);
    };

    return (
        <div className={`space-y-3 ${className}`}>
            <div className="flex items-center gap-2">
                <Tag className="h-4 w-4 text-slate-500" />
                <h3 className="text-sm font-medium text-slate-700">Tags</h3>
            </div>

            {/* Current tags */}
            <div className="flex flex-wrap gap-2">
                {tags.map((tag) => (
                    <div
                        key={tag}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-md text-sm"
                    >
                        <span>{tag}</span>
                        <button
                            onClick={() => removeTag(tag)}
                            className="hover:bg-blue-200 rounded-full p-0.5 transition-colors"
                            aria-label={`Remove tag ${tag}`}
                        >
                            <X className="h-3 w-3" />
                        </button>
                    </div>
                ))}

                {/* Add tag button/input */}
                {!showInput ? (
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setShowInput(true)}
                        className="gap-1 border-dashed"
                    >
                        <Plus className="h-3 w-3" />
                        Ajouter tag
                    </Button>
                ) : (
                    <div className="relative">
                        <input
                            type="text"
                            value={newTag}
                            onChange={(e) => {
                                const value = e.target.value;
                                if (value.length <= 30) {
                                    setNewTag(value);
                                }
                            }}
                            onKeyDown={handleKeyPress}
                            onBlur={handleInputBlur}
                            placeholder="Nouveau tag..."
                            className={`px-2 py-1 border rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none w-32 ${
                                newTag.length > 25 ? 'border-orange-300' : 'border-slate-300'
                            }`}
                            autoFocus
                        />
                        {newTag.length > 20 && (
                            <div className="absolute -top-6 right-0 text-xs text-slate-500">
                                {newTag.length}/30
                            </div>
                        )}

                        {/* Suggestions dropdown */}
                        {suggestions.length > 0 && (
                            <div className="absolute z-10 top-full mt-1 w-48 bg-white border border-slate-200 rounded-md shadow-lg">
                                {suggestions.map((suggestion) => (
                                    <button
                                        key={suggestion}
                                        onClick={() => addTag(suggestion)}
                                        className="w-full px-3 py-2 text-left text-sm hover:bg-slate-100 first:rounded-t-md last:rounded-b-md"
                                    >
                                        {suggestion}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Popular tags suggestions */}
            {availableTags.length > 0 && tags.length === 0 && (
                <div className="space-y-2">
                    <p className="text-xs text-slate-500">Tags populaires :</p>
                    <div className="flex flex-wrap gap-1">
                        {availableTags.slice(0, 8).map((tag) => (
                            <button
                                key={tag}
                                onClick={() => addTag(tag)}
                                className="px-2 py-1 bg-slate-100 text-slate-600 rounded-md text-xs hover:bg-slate-200 transition-colors"
                            >
                                {tag}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}