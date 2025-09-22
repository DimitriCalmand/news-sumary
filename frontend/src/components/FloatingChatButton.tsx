import React from 'react';
import { MessageCircle, X } from 'lucide-react';

interface FloatingChatButtonProps {
  isOpen: boolean;
  onClick: () => void;
  messageCount?: number;
}

export const FloatingChatButton: React.FC<FloatingChatButtonProps> = ({
  isOpen,
  onClick,
  messageCount = 0
}) => {
  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={onClick}
        className={`
          relative flex items-center justify-center
          w-14 h-14 rounded-full shadow-lg
          transition-all duration-300 ease-in-out
          hover:scale-110 active:scale-95
          ${isOpen 
            ? 'bg-red-500 hover:bg-red-600' 
            : 'bg-blue-500 hover:bg-blue-600'
          }
          text-white
        `}
        aria-label={isOpen ? "Fermer le chat" : "Ouvrir le chat"}
      >
        {/* Icon */}
        <div className="transition-transform duration-200">
          {isOpen ? (
            <X className="h-6 w-6" />
          ) : (
            <MessageCircle className="h-6 w-6" />
          )}
        </div>

        {/* Message Count Badge */}
        {!isOpen && messageCount > 0 && (
          <div className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center min-w-[1.5rem]">
            {messageCount > 99 ? '99+' : messageCount}
          </div>
        )}

        {/* Pulse Animation for new messages */}
        {!isOpen && messageCount === 0 && (
          <div className="absolute inset-0 rounded-full bg-blue-400 animate-ping opacity-75"></div>
        )}
      </button>

      {/* Tooltip */}
      {!isOpen && (
        <div className="absolute bottom-full right-0 mb-2 opacity-0 hover:opacity-100 transition-opacity duration-200 pointer-events-none">
          <div className="bg-gray-800 text-white text-sm py-2 px-3 rounded-lg whitespace-nowrap">
            💬 Poser une question sur cet article
            <div className="absolute top-full right-4 border-4 border-transparent border-t-gray-800"></div>
          </div>
        </div>
      )}
    </div>
  );
};