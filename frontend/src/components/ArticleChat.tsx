import React, { useEffect, useState } from 'react';
import { useSharedChat } from '../hooks/useSharedChat';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from './ui/Button';

interface ArticleChatProps {
    articleId: string;
    articleTitle: string;
    sharedChat: ReturnType<typeof useSharedChat>;
}

export const ArticleChat: React.FC<ArticleChatProps> = ({ sharedChat }) => {
    const [inputMessage, setInputMessage] = useState('');
    const [isExpanded, setIsExpanded] = useState(false); // Fermé par défaut
    
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

    // Load chat history when component is expanded and messages are empty
    useEffect(() => {
        if (isExpanded && messages.length === 0) {
            loadChatHistory();
        }
    }, [isExpanded, messages.length, loadChatHistory]);

    // Scroll to bottom when messages change
    useEffect(() => {
        if (isExpanded && messages.length > 0) {
            setTimeout(() => scrollToBottom(), 100);
        }
    }, [messages, isExpanded, scrollToBottom]);

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

    return (
        <div className="border rounded-lg bg-white shadow-sm">
            {/* Chat Header */}
            <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-blue-50 transition-colors border-b"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                        <span className="text-lg">🤖</span>
                    </div>
                    <div>
                        <h3 className="font-medium text-gray-900">
                            Chat avec l'Assistant IA
                        </h3>
                        <p className="text-sm text-gray-600">
                            Cliquez pour {isExpanded ? 'réduire' : 'agrandir'} le chat
                        </p>
                    </div>
                </div>
                <div className="flex items-center space-x-2">
                    {messages.length > 0 && (
                        <span className="text-sm text-blue-600 bg-blue-100 px-3 py-1 rounded-full font-medium">
                            {messages.length} message{messages.length > 1 ? 's' : ''}
                        </span>
                    )}
                    <span className={`transform transition-transform text-gray-400 ${isExpanded ? 'rotate-180' : ''}`}>
                        ⌄
                    </span>
                </div>
            </div>

            {/* Chat Content */}
            {isExpanded && (
                <div className="bg-white">
                    {/* Loading history indicator */}
                    {isLoadingHistory && (
                        <div className="p-6 text-center">
                            <div className="flex items-center justify-center space-x-2">
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                                <span className="text-sm text-gray-600">Chargement de l'historique...</span>
                            </div>
                        </div>
                    )}

                    {/* Empty state */}
                    {messages.length === 0 && !isLoadingHistory && (
                        <div className="p-6 text-center">
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-2xl">💬</span>
                            </div>
                            <p className="text-gray-600 mb-2">Commencez une conversation</p>
                            <p className="text-sm text-gray-500">
                                Posez votre première question sur cet article !
                            </p>
                        </div>
                    )}

                    {/* Messages */}
                    {messages.length > 0 && (
                        <div className="max-h-96 overflow-y-auto p-4 space-y-4">
                            {messages.map((message) => (
                                <div
                                    key={message.id}
                                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div
                                        className={`max-w-[80%] p-3 rounded-lg ${message.type === 'user'
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
                                        <div className={`text-xs mt-1 ${message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
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
                            {/* Invisible element to scroll to */}
                            <div ref={messagesEndRef} />
                        </div>
                    )}

                    {/* Input Area */}
                    <div className="p-4 border-t bg-blue-50">
                        <div className="flex space-x-3">
                            <textarea
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Posez votre question sur cet article..."
                                className="flex-1 p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                rows={2}
                                disabled={isLoading || isLoadingHistory}
                            />
                            <div className="flex flex-col space-y-2">
                                <Button
                                    onClick={handleSendMessage}
                                    disabled={!inputMessage.trim() || isLoading || isLoadingHistory}
                                    className="px-6 py-2 text-sm bg-blue-500 hover:bg-blue-600"
                                >
                                    {isLoading ? '...' : 'Envoyer'}
                                </Button>
                                {messages.length > 0 && (
                                    <Button
                                        onClick={clearChat}
                                        variant="outline"
                                        className="px-4 py-1 text-xs text-red-600 hover:text-red-700 hover:bg-red-50"
                                    >
                                        Effacer
                                    </Button>
                                )}
                            </div>
                        </div>

                        <div className="mt-2 text-xs text-gray-500">
                            Entrée pour envoyer • Shift+Entrée pour une nouvelle ligne
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};