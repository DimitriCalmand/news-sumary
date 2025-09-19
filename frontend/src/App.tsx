import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Route, BrowserRouter as Router, Routes, useParams } from 'react-router-dom';
import { ArticleDetail } from './components/ArticleDetail';
import { ArticleList } from './components/ArticleList';

// Wrapper pour ArticleDetail avec key basé sur l'ID
function ArticleDetailWrapper() {
  const { id } = useParams<{ id: string }>();
  return <ArticleDetail key={id} />;
}

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: true,
      refetchOnMount: true,
      refetchOnReconnect: true,
      staleTime: 0, // Toujours considérer comme obsolète
      gcTime: 0, // Pas de cache
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<ArticleList />} />
          <Route path="/article/:id" element={<ArticleDetailWrapper />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
