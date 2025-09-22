import React, { useEffect, useRef, useState } from 'react';
import { X, MessageCircle, Trash2 } from 'lucide-react';
import { useSharedChat } from '../hooks/useSharedChat';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from './ui/Button';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  articleId: string;
  articleTitle: string;
  sharedChat: ReturnType<typeof useSharedChat>;
}

export const ChatModal: React.FC<ChatModalProps> = ({
  isOpen,
  onClose,
  articleTitle,
  sharedChat
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Destructure shared chat state and methods
  const {
    messages,
    isLoading,
    isLoadingHistory,
    messagesEndRef,
    scrollToBottom,
    loadChatHistory,
    sendMessage,
    clearChat
  } = sharedChat;

  // Load chat history when modal opens
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      loadChatHistory();
    }
  }, [isOpen, messages.length, loadChatHistory]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (isOpen && messages.length > 0) {
      setTimeout(() => scrollToBottom(), 100);
    }
  }, [messages, isOpen, scrollToBottom]);

  // Focus textarea when modal opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        textareaRef.current?.focus();
      }, 200);
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    
    await sendMessage(inputMessage);
    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-end justify-center p-4 md:items-center">
        <div className="bg-white rounded-t-lg md:rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col animate-in slide-in-from-bottom-4 md:slide-in-from-bottom-0 md:fade-in duration-200">
          
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b bg-blue-50 rounded-t-lg">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MessageCircle className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900">
                  Chat sur l'article
                </h3>
                <p className="text-sm text-gray-600 truncate max-w-xs">
                  {articleTitle}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {messages.length > 0 && (
                <Button
                  onClick={clearChat}
                  variant="outline"
                  size="sm"
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
              <button
                onClick={onClose}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
            {isLoadingHistory && (
              <div className="text-center py-8">
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                  <span className="text-sm text-gray-600">Chargement de l'historique...</span>
                </div>
              </div>
            )}

            {messages.length === 0 && !isLoadingHistory && (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="h-8 w-8 text-blue-600" />
                </div>
                <p className="text-gray-600 mb-2">Aucune conversation pour le moment</p>
                <p className="text-sm text-gray-500">
                  Posez votre première question sur cet article !
                </p>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] p-3 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {message.type === 'ai' ? (
                    <MarkdownRenderer
                      content={message.content}
                      className="text-sm"
                    />
                  ) : (
                    <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                  )}
                  <div className={`text-xs mt-2 ${
                    message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 p-3 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                    <span className="text-sm">L'IA réfléchit...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t bg-gray-50">
            <div className="flex space-x-3">
              <textarea
                ref={textareaRef}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Posez votre question sur cet article..."
                className="flex-1 p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={2}
                disabled={isLoading || isLoadingHistory}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading || isLoadingHistory}
                className="px-6 self-end"
              >
                {isLoading ? '...' : 'Envoyer'}
              </Button>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Entrée pour envoyer • Shift+Entrée pour une nouvelle ligne
            </div>
          </div>
        </div>
      </div>
    </>
  );
};