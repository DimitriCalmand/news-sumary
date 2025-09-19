import 'highlight.js/styles/github.css'; // Style pour syntax highlighting
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
    content: string;
    className?: string;
}

export function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
    return (
        <div className={`prose prose-slate max-w-none ${className}`}>
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight, rehypeRaw]}
                components={{
                    // Personnalisation des composants Markdown
                    h1: ({ children }) => (
                        <h1 className="text-3xl font-bold text-slate-900 mb-6 border-b border-slate-200 pb-3">
                            {children}
                        </h1>
                    ),
                    h2: ({ children }) => (
                        <h2 className="text-2xl font-semibold text-slate-800 mb-4 mt-8">
                            {children}
                        </h2>
                    ),
                    h3: ({ children }) => (
                        <h3 className="text-xl font-medium text-slate-700 mb-3 mt-6">
                            {children}
                        </h3>
                    ),
                    p: ({ children }) => (
                        <p className="text-slate-600 leading-relaxed mb-4">
                            {children}
                        </p>
                    ),
                    strong: ({ children }) => (
                        <strong className="font-semibold text-slate-900">
                            {children}
                        </strong>
                    ),
                    em: ({ children }) => (
                        <em className="italic text-slate-700">
                            {children}
                        </em>
                    ),
                    ul: ({ children }) => (
                        <ul className="list-disc list-inside mb-4 space-y-2 text-slate-600">
                            {children}
                        </ul>
                    ),
                    ol: ({ children }) => (
                        <ol className="list-decimal list-inside mb-4 space-y-2 text-slate-600">
                            {children}
                        </ol>
                    ),
                    li: ({ children }) => (
                        <li className="leading-relaxed">
                            {children}
                        </li>
                    ),
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-blue-500 pl-4 py-2 mb-4 bg-blue-50 text-slate-700 italic">
                            {children}
                        </blockquote>
                    ),
                    code: ({ className, children, ...props }) => {
                        const match = /language-(\w+)/.exec(className || '');
                        const isInline = !match;

                        if (isInline) {
                            return (
                                <code className="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded text-sm font-mono">
                                    {children}
                                </code>
                            );
                        }

                        return (
                            <code className={className} {...props}>
                                {children}
                            </code>
                        );
                    },
                    pre: ({ children }) => (
                        <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg mb-4 overflow-x-auto">
                            {children}
                        </pre>
                    ),
                    a: ({ href, children }) => (
                        <a
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 underline"
                        >
                            {children}
                        </a>
                    ),
                    table: ({ children }) => (
                        <div className="overflow-x-auto mb-4">
                            <table className="min-w-full border border-slate-300">
                                {children}
                            </table>
                        </div>
                    ),
                    th: ({ children }) => (
                        <th className="border border-slate-300 px-4 py-2 bg-slate-100 font-semibold text-left">
                            {children}
                        </th>
                    ),
                    td: ({ children }) => (
                        <td className="border border-slate-300 px-4 py-2">
                            {children}
                        </td>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}