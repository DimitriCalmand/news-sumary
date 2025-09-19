import { Star } from 'lucide-react';
import { useEffect, useState } from 'react';

interface StarRatingProps {
    rating?: number; // Current rating (1-5)
    onRatingChange?: (rating: number) => void;
    readonly?: boolean;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

export function StarRating({
    rating = 0,
    onRatingChange,
    readonly = false,
    size = 'md',
    className = ''
}: StarRatingProps) {
    const [hoverRating, setHoverRating] = useState(0);
    const [localRating, setLocalRating] = useState(rating); // État local pour affichage immédiat

    // Reset hover rating when rating prop changes
    useEffect(() => {
        setHoverRating(0);
        setLocalRating(rating); // Sync avec le prop
    }, [rating]);

    const sizeClasses = {
        sm: 'h-4 w-4',
        md: 'h-5 w-5',
        lg: 'h-6 w-6'
    };

    const handleClick = (starRating: number) => {
        if (!readonly && onRatingChange) {
            setHoverRating(0); // Reset hover après le clic
            setLocalRating(starRating); // Mettre à jour immédiatement l'affichage local
            onRatingChange(starRating);
        }
    };

    const handleMouseEnter = (starRating: number) => {
        if (!readonly) {
            setHoverRating(starRating);
        }
    };

    const handleMouseLeave = () => {
        if (!readonly) {
            setHoverRating(0);
        }
    };

    const displayRating = readonly ? localRating : (hoverRating || localRating);

    return (
        <div className={`flex items-center gap-1 ${className}`}>
            {[1, 2, 3, 4, 5].map((star) => (
                <button
                    key={star}
                    type="button"
                    disabled={readonly}
                    onClick={() => handleClick(star)}
                    onMouseEnter={() => handleMouseEnter(star)}
                    onMouseLeave={handleMouseLeave}
                    className={`
            ${sizeClasses[size]}
            ${readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110'}
            transition-all duration-150
            ${star <= displayRating ? 'text-yellow-500' : 'text-slate-300'}
            ${!readonly ? 'hover:text-yellow-400' : ''}
          `}
                    aria-label={`Rate ${star} star${star !== 1 ? 's' : ''}`}
                >
                    <Star
                        className={`w-full h-full ${star <= displayRating ? 'fill-current' : ''}`}
                    />
                </button>
            ))}

            {/* Display rating text if there's a rating */}
            {localRating > 0 && (
                <span className="ml-2 text-sm text-slate-600">
                    {localRating}/5
                </span>
            )}
        </div>
    );
}