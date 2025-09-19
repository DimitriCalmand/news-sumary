import { MessageSquare, Save, X } from 'lucide-react';
import { useState } from 'react';
import { Button } from './ui/Button';

interface CommentsEditorProps {
    initialComments?: string;
    onSave?: (comments: string) => void;
    className?: string;
}

export function CommentsEditor({
    initialComments = '',
    onSave,
    className = ''
}: CommentsEditorProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [comments, setComments] = useState(initialComments);
    const [tempComments, setTempComments] = useState(initialComments);

    const handleStartEdit = () => {
        setTempComments(comments);
        setIsEditing(true);
    };

    const handleSave = () => {
        setComments(tempComments);
        setIsEditing(false);
        if (onSave) {
            onSave(tempComments);
        }
    };

    const handleCancel = () => {
        setTempComments(comments);
        setIsEditing(false);
    };

    const hasComments = comments.trim().length > 0;

    return (
        <div className={`space-y-3 ${className}`}>
            <div className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-slate-500" />
                <h3 className="text-sm font-medium text-slate-700">Mes commentaires</h3>
            </div>

            {!isEditing ? (
                <div className="space-y-2">
                    {hasComments ? (
                        <div
                            className="p-3 bg-slate-50 rounded-md border cursor-pointer hover:bg-slate-100 transition-colors"
                            onClick={handleStartEdit}
                        >
                            <p className="text-sm text-slate-700 whitespace-pre-wrap">
                                {comments}
                            </p>
                        </div>
                    ) : (
                        <div
                            className="p-3 bg-slate-50 rounded-md border border-dashed cursor-pointer hover:bg-slate-100 transition-colors"
                            onClick={handleStartEdit}
                        >
                            <p className="text-sm text-slate-500 italic">
                                Cliquez pour ajouter vos commentaires...
                            </p>
                        </div>
                    )}

                    {hasComments && (
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleStartEdit}
                        >
                            Modifier
                        </Button>
                    )}
                </div>
            ) : (
                <div className="space-y-3">
                    <textarea
                        value={tempComments}
                        onChange={(e) => setTempComments(e.target.value)}
                        placeholder="Ajoutez vos commentaires personnels sur cet article..."
                        className="w-full p-3 border border-slate-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-vertical min-h-[100px]"
                        autoFocus
                    />

                    <div className="flex gap-2">
                        <Button
                            size="sm"
                            onClick={handleSave}
                            className="gap-1"
                        >
                            <Save className="h-3 w-3" />
                            Sauvegarder
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleCancel}
                            className="gap-1"
                        >
                            <X className="h-3 w-3" />
                            Annuler
                        </Button>
                    </div>
                </div>
            )}
        </div>
    );
}