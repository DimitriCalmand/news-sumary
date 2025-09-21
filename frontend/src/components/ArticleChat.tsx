import React, { useEffect, useRef, useState } from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Button } from './ui/Button';

interface ArticleChatProps {
    articleId: string;
    articleTitle: string;
}

interface ChatMessage {
    id: string;
    type: 'user' | 'ai';
    content: string;
    timestamp: Date;
}

export const ArticleChat: React.FC<ArticleChatProps> = ({ articleId }) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [isLoadingHistory, setIsLoadingHistory] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Function to scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    // Load chat history when component mounts or when expanded
    useEffect(() => {
        if (isExpanded && messages.length === 0) {
            loadChatHistory();
        }
    }, [isExpanded, messages.length, articleId]);

    // Scroll to bottom when messages change
    useEffect(() => {
        if (isExpanded && messages.length > 0) {
            scrollToBottom();
        }
    }, [messages, isExpanded]);

    const loadChatHistory = async () => {
        setIsLoadingHistory(true);
        try {
            const response = await fetch(`/api/articles/${articleId}/chat/history`);
            const data = await response.json();

            if (data.success && data.conversation) {
                const loadedMessages: ChatMessage[] = data.conversation.map((msg: any) => ({
                    id: msg.id,
                    type: msg.type,
                    content: msg.content,
                    timestamp: new Date(msg.timestamp)
                }));
                setMessages(loadedMessages);
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        } finally {
            setIsLoadingHistory(false);
        }
    };

    const sendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            type: 'user',
            content: inputMessage,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await fetch(`/api/articles/${articleId}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: inputMessage,
                    model: 'mistral small'
                }),
            });

            const data = await response.json();

            if (data.success) {
                const aiMessage: ChatMessage = {
                    id: (Date.now() + 1).toString(),
                    type: 'ai',
                    content: data.answer,
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, aiMessage]);
            } else {
                const errorMessage: ChatMessage = {
                    id: (Date.now() + 1).toString(),
                    type: 'ai',
                    content: `Erreur: ${data.error}`,
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, errorMessage]);
            }
        } catch (error) {
            const errorMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                type: 'ai',
                content: 'Erreur de connexion avec le service IA',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const clearChat = async () => {
        try {
            const response = await fetch(`/api/articles/${articleId}/chat/clear`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (data.success) {
                setMessages([]);
            } else {
                console.error('Failed to clear chat history:', data.error);
            }
        } catch (error) {
            console.error('Error clearing chat history:', error);
            // Clear locally anyway
            setMessages([]);
        }
    };

    return (
        <div className="mt-6 border rounded-lg bg-gray-50">
            {/* Chat Header */}
            <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-center space-x-2">
                    <span className="text-lg">🤖</span>
                    <h3 className="font-medium text-gray-800">
                        Poser une question sur cet article
                    </h3>
                </div>
                <div className="flex items-center space-x-2">
                    {messages.length > 0 && (
                        <span className="text-sm text-gray-500 bg-gray-200 px-2 py-1 rounded-full">
                            {messages.length} message{messages.length > 1 ? 's' : ''}
                        </span>
                    )}
                    <span className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                        ⌄
                    </span>
                </div>
            </div>

            {/* Chat Content */}
            {isExpanded && (
                <div className="border-t bg-white">
                    {/* Loading history indicator */}
                    {isLoadingHistory && (
                        <div className="p-4 text-center">
                            <div className="flex items-center justify-center space-x-2">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                                <span className="text-sm text-gray-600">Chargement de l'historique...</span>
                            </div>
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
                    <div className="p-4 border-t bg-gray-50">
                        <div className="flex space-x-2">
                            <textarea
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Posez votre question sur cet article..."
                                className="flex-1 p-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                                rows={2}
                                disabled={isLoading || isLoadingHistory}
                            />
                            <div className="flex flex-col space-y-1">
                                <Button
                                    onClick={sendMessage}
                                    disabled={!inputMessage.trim() || isLoading || isLoadingHistory}
                                    className="px-4 py-2 text-sm"
                                >
                                    {isLoading ? '...' : 'Envoyer'}
                                </Button>
                                {messages.length > 0 && (
                                    <Button
                                        onClick={clearChat}
                                        variant="outline"
                                        className="px-4 py-1 text-xs"
                                    >
                                        Effacer
                                    </Button>
                                )}
                            </div>
                        </div>

                        <div className="mt-2 text-xs text-gray-500">
                            Appuyez sur Entrée pour envoyer • Shift+Entrée pour une nouvelle ligne
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};