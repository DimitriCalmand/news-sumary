import { useCallback, useRef, useState } from 'react';

export interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export function useSharedChat(articleId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Function to scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // Load chat history
  const loadChatHistory = useCallback(async () => {
    if (messages.length > 0) return; // Don't reload if already loaded
    
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
  }, [articleId, messages.length]);

  // Send message
  const sendMessage = useCallback(async (inputMessage: string) => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
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
  }, [articleId, isLoading]);

  // Clear chat
  const clearChat = useCallback(async () => {
    try {
      const response = await fetch(`/api/articles/${articleId}/chat/clear`, {
        method: 'DELETE'
      });
      const data = await response.json();

      if (data.success) {
        setMessages([]);
      } else {
        console.error('Failed to clear chat history:', data.error);
        // Clear locally anyway
        setMessages([]);
      }
    } catch (error) {
      console.error('Error clearing chat history:', error);
      // Clear locally anyway
      setMessages([]);
    }
  }, [articleId]);

  return {
    messages,
    isLoading,
    isLoadingHistory,
    messagesEndRef,
    scrollToBottom,
    loadChatHistory,
    sendMessage,
    clearChat
  };
}