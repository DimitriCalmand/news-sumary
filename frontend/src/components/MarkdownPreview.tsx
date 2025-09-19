interface MarkdownPreviewProps {
    content: string;
    maxLength?: number;
    className?: string;
}

export function MarkdownPreview({ content, maxLength = 200, className = '' }: MarkdownPreviewProps) {
    // Fonction pour extraire un aperçu du contenu Markdown
    const getPreview = (markdownContent: string, length: number): string => {
        // Supprimer les headers markdown (# ## ###)
        let preview = markdownContent.replace(/^#{1,6}\s+/gm, '');

        // Supprimer les liens markdown [text](url)
        preview = preview.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');

        // Supprimer le formatage bold/italic (**text** *text*)
        preview = preview.replace(/\*\*([^*]+)\*\*/g, '$1');
        preview = preview.replace(/\*([^*]+)\*/g, '$1');

        // Supprimer les codes inline `code`
        preview = preview.replace(/`([^`]+)`/g, '$1');

        // Supprimer les blocs de code
        preview = preview.replace(/```[\s\S]*?```/g, '');

        // Supprimer les listes - * +
        preview = preview.replace(/^[\s]*[-*+]\s+/gm, '');

        // Supprimer les blockquotes >
        preview = preview.replace(/^>\s+/gm, '');

        // Nettoyer les sauts de ligne multiples
        preview = preview.replace(/\n\s*\n/g, '\n');

        // Supprimer les espaces en début/fin
        preview = preview.trim();

        // Tronquer à la longueur demandée
        if (preview.length > length) {
            preview = preview.substring(0, length);
            // Trouver le dernier espace pour éviter de couper un mot
            const lastSpace = preview.lastIndexOf(' ');
            if (lastSpace > length * 0.8) { // Si l'espace est pas trop loin
                preview = preview.substring(0, lastSpace);
            }
            preview += '...';
        }

        return preview;
    };

    const previewText = getPreview(content, maxLength);

    // Si le contenu est très court ou n'a pas de markdown complexe, 
    // on peut afficher directement le texte
    const hasComplexMarkdown = content.includes('#') ||
        content.includes('**') ||
        content.includes('```') ||
        content.includes('[') ||
        content.includes('*') ||
        content.includes('`');

    if (!hasComplexMarkdown && content.length <= maxLength) {
        return (
            <div className={`text-slate-600 leading-relaxed ${className}`}>
                {content}
            </div>
        );
    }

    // Pour un aperçu, on affiche le texte nettoyé plutôt que le Markdown rendu
    return (
        <div className={`text-slate-600 leading-relaxed ${className}`}>
            {previewText}
        </div>
    );
}