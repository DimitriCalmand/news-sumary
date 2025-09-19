import { cn } from '../lib/utils';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/Button';

interface PaginationControlsProps {
  currentPage: number;
  totalItems: number;
  itemsPerPage: number;
  onPageChange: (page: number) => void;
  className?: string;
}

export function PaginationControls({
  currentPage,
  totalItems,
  itemsPerPage,
  onPageChange,
  className
}: PaginationControlsProps) {
  const totalPages = Math.ceil(totalItems / itemsPerPage);

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const handlePageClick = (page: number) => {
    onPageChange(page);
  };

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;

    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      const start = Math.max(1, currentPage - 2);
      const end = Math.min(totalPages, start + maxVisible - 1);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (start > 1) {
        pages.unshift('...');
        pages.unshift(1);
      }

      if (end < totalPages) {
        pages.push('...');
        pages.push(totalPages);
      }
    }

    return pages;
  };

  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className={cn("flex flex-col sm:flex-row items-center justify-between gap-4", className)}>
      <div className="text-sm text-slate-600">
        Affichage {startItem}-{endItem} sur {totalItems} articles
      </div>

      <div className="flex items-center gap-1">
        <Button
          variant="outline"
          size="sm"
          onClick={handlePrevious}
          disabled={currentPage === 1}
          className="p-2"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        {getPageNumbers().map((page, index) => (
          <div key={index}>
            {page === '...' ? (
              <span className="px-2 py-1 text-sm text-slate-400">...</span>
            ) : (
              <Button
                variant={currentPage === page ? "default" : "outline"}
                size="sm"
                onClick={() => handlePageClick(page as number)}
                className="min-w-[40px]"
              >
                {page}
              </Button>
            )}
          </div>
        ))}

        <Button
          variant="outline"
          size="sm"
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="p-2"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}