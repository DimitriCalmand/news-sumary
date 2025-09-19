import { Clock, Pause, Play } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

interface ReadingTimerProps {
    initialTime?: number; // Initial time in seconds
    onTimeUpdate?: (totalSeconds: number) => void;
    articleId?: number;
    className?: string;
}

export function ReadingTimer({
    initialTime = 0,
    onTimeUpdate,
    articleId,
    className = ''
}: ReadingTimerProps) {
    const [isActive, setIsActive] = useState(false);
    const [currentSessionTime, setCurrentSessionTime] = useState(0);
    const [totalTime, setTotalTime] = useState(initialTime);
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    // Format seconds to readable string
    const formatTime = (seconds: number): string => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const remainingSeconds = seconds % 60;

        if (hours > 0) {
            return `${hours}h ${minutes}m ${remainingSeconds}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${remainingSeconds}s`;
        } else {
            return `${remainingSeconds}s`;
        }
    };

    // Start/stop timer
    const toggleTimer = () => {
        setIsActive(!isActive);
    };

    // Save current session when component unmounts or timer stops
    const saveCurrentSession = () => {
        if (currentSessionTime > 0 && onTimeUpdate) {
            onTimeUpdate(currentSessionTime);
            setTotalTime(prev => prev + currentSessionTime);
            setCurrentSessionTime(0);
        }
    };

    // Handle timer tick
    useEffect(() => {
        if (isActive) {
            intervalRef.current = setInterval(() => {
                setCurrentSessionTime(prev => prev + 1);
            }, 1000);
        } else {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
            // Save session when paused
            if (currentSessionTime > 0) {
                saveCurrentSession();
            }
        }

        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, [isActive, currentSessionTime]);

    // Save session when component unmounts
    useEffect(() => {
        return () => {
            if (currentSessionTime > 0 && onTimeUpdate) {
                onTimeUpdate(currentSessionTime);
            }
        };
    }, []);

    // Auto-pause when user is away (optional feature)
    useEffect(() => {
        const handleVisibilityChange = () => {
            if (document.hidden && isActive) {
                setIsActive(false);
            }
        };

        document.addEventListener('visibilitychange', handleVisibilityChange);
        return () => {
            document.removeEventListener('visibilitychange', handleVisibilityChange);
        };
    }, [isActive]);

    const displayTime = totalTime + currentSessionTime;

    return (
        <div className={`flex items-center gap-3 ${className}`}>
            <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-slate-500" />
                <div className="flex flex-col">
                    <span className="text-sm font-medium text-slate-700">
                        {formatTime(displayTime)}
                    </span>
                    {currentSessionTime > 0 && (
                        <span className="text-xs text-slate-500">
                            +{formatTime(currentSessionTime)} cette session
                        </span>
                    )}
                </div>
            </div>

            <button
                onClick={toggleTimer}
                className={`
          flex items-center gap-1 px-3 py-1 rounded-md text-sm font-medium transition-colors
          ${isActive
                        ? 'bg-red-100 text-red-700 hover:bg-red-200'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    }
        `}
                aria-label={isActive ? 'Pause reading timer' : 'Start reading timer'}
            >
                {isActive ? (
                    <>
                        <Pause className="h-3 w-3" />
                        Pause
                    </>
                ) : (
                    <>
                        <Play className="h-3 w-3" />
                        Lire
                    </>
                )}
            </button>

            {totalTime > 0 && (
                <div className="text-xs text-slate-500">
                    Total: {formatTime(totalTime)}
                </div>
            )}
        </div>
    );
}