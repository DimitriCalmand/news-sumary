import { Clock, Pause, Play } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

interface AutoReadingTimerProps {
    initialTime?: number; // Initial time in seconds
    onTimeUpdate?: (totalSeconds: number) => void;
    className?: string;
}

export function AutoReadingTimer({
    initialTime = 0,
    onTimeUpdate,
    className = ''
}: AutoReadingTimerProps) {
    const [isActive, setIsActive] = useState(false);
    const [currentSessionTime, setCurrentSessionTime] = useState(0);
    const [totalTime, setTotalTime] = useState(initialTime);
    const [isPaused, setIsPaused] = useState(false);
    const [lastSavedSessionTime, setLastSavedSessionTime] = useState(0); // Pour tracker le delta
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    // Auto-start timer when component mounts
    useEffect(() => {
        setIsActive(true);
        setIsPaused(false);
    }, []);

    // Handle visibility change (tab switching, minimizing, etc.)
    useEffect(() => {
        const handleVisibilityChange = () => {
            if (document.hidden) {
                // Page is hidden - pause timer
                setIsPaused(true);
            } else {
                // Page is visible - resume timer
                setIsPaused(false);
            }
        };

        // Handle window focus/blur
        const handleFocus = () => setIsPaused(false);
        const handleBlur = () => setIsPaused(true);

        document.addEventListener('visibilitychange', handleVisibilityChange);
        window.addEventListener('focus', handleFocus);
        window.addEventListener('blur', handleBlur);

        // Initial state check
        if (document.hidden) {
            setIsPaused(true);
        }

        return () => {
            document.removeEventListener('visibilitychange', handleVisibilityChange);
            window.removeEventListener('focus', handleFocus);
            window.removeEventListener('blur', handleBlur);
        };
    }, []);

    // Timer logic
    useEffect(() => {
        if (isActive && !isPaused) {
            intervalRef.current = setInterval(() => {
                setCurrentSessionTime(prev => prev + 1);
                setTotalTime(prev => prev + 1);
            }, 1000);
        } else if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }

        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, [isActive, isPaused]);

    // Save time periodically (every 10 seconds)
    useEffect(() => {
        if (!isActive) return;

        const saveInterval = setInterval(() => {
            const deltaTime = currentSessionTime - lastSavedSessionTime;
            if (deltaTime > 0) {
                onTimeUpdate?.(deltaTime); // Envoyer seulement le delta
                setLastSavedSessionTime(currentSessionTime); // Mettre à jour le dernier temps sauvé
            }
        }, 10000); // Toutes les 10 secondes

        return () => clearInterval(saveInterval);
    }, [currentSessionTime, lastSavedSessionTime, onTimeUpdate, isActive]);

    // Save final time when component unmounts
    useEffect(() => {
        return () => {
            const deltaTime = currentSessionTime - lastSavedSessionTime;
            if (deltaTime > 0) {
                onTimeUpdate?.(deltaTime); // Envoyer le delta final
            }
        };
    }, [currentSessionTime, lastSavedSessionTime, onTimeUpdate]);

    const formatTime = (seconds: number): string => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        if (hours > 0) {
            return `${hours}h ${minutes}m ${secs}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    };

    const handleManualToggle = () => {
        if (isActive) {
            setIsActive(false);
            setIsPaused(false);
        } else {
            setIsActive(true);
            setIsPaused(false);
        }
    };

    const getStatusColor = () => {
        if (!isActive) return 'text-gray-500';
        if (isPaused) return 'text-orange-500';
        return 'text-green-500';
    };

    const getStatusText = () => {
        if (!isActive) return 'Arrêté';
        if (isPaused) return 'En pause (onglet inactif)';
        return 'En cours';
    };

    const getStatusIcon = () => {
        if (!isActive) return <Clock className="h-4 w-4" />;
        if (isPaused) return <Pause className="h-4 w-4" />;
        return <Play className="h-4 w-4" />;
    };

    return (
        <div className={`bg-white border border-gray-200 rounded-lg p-4 ${className}`}>
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <div className={getStatusColor()}>
                        {getStatusIcon()}
                    </div>
                    <span className="text-sm font-medium text-gray-700">Temps de lecture</span>
                </div>
                <button
                    onClick={handleManualToggle}
                    className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                >
                    {isActive ? 'Arrêter' : 'Reprendre'}
                </button>
            </div>

            <div className="space-y-2">
                <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Session actuelle:</span>
                    <span className="text-sm font-mono text-gray-900">
                        {formatTime(currentSessionTime)}
                    </span>
                </div>

                <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Temps total:</span>
                    <span className="text-sm font-mono font-medium text-gray-900">
                        {formatTime(totalTime)}
                    </span>
                </div>

                <div className="pt-2 border-t border-gray-100">
                    <div className={`flex items-center gap-2 text-xs ${getStatusColor()}`}>
                        {getStatusIcon()}
                        <span>{getStatusText()}</span>
                    </div>
                </div>
            </div>

            {isPaused && (
                <div className="mt-3 p-2 bg-orange-50 border border-orange-200 rounded-md">
                    <p className="text-xs text-orange-700">
                        ⏸️ Timer en pause - revenez sur cet onglet pour continuer
                    </p>
                </div>
            )}
        </div>
    );
}