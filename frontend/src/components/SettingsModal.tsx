import React, { useEffect, useState } from 'react';
import { settingsApi, type Model, type Settings } from '../lib/api';

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave?: () => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, onSave }) => {
    const [settings, setSettings] = useState<Settings | null>(null);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Load settings when modal opens
    useEffect(() => {
        if (isOpen) {
            loadSettings();
        }
    }, [isOpen]);

    const loadSettings = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await settingsApi.getSettings();
            setSettings(data);
        } catch (err) {
            setError('Erreur lors du chargement des paramètres');
            console.error('Error loading settings:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!settings) return;

        setSaving(true);
        setError(null);
        try {
            await settingsApi.updateSettings(settings);
            onSave?.();
            onClose();
        } catch (err) {
            setError('Erreur lors de la sauvegarde des paramètres');
            console.error('Error saving settings:', err);
        } finally {
            setSaving(false);
        }
    };

    const handlePromptChange = (type: 'article_processing' | 'chat', value: string) => {
        if (!settings) return;
        setSettings({
            ...settings,
            prompts: {
                ...settings.prompts,
                [type]: value,
            },
        });
    };

    const handleDefaultModelChange = (modelName: string) => {
        if (!settings) return;
        setSettings({
            ...settings,
            default_model: modelName,
        });
    };

    const handleModelChange = (index: number, field: keyof Model, value: string) => {
        if (!settings) return;
        const updatedModels = [...settings.models];
        updatedModels[index] = {
            ...updatedModels[index],
            [field]: value,
        };
        setSettings({
            ...settings,
            models: updatedModels,
        });
    };

    const addModel = () => {
        if (!settings) return;
        const newModel: Model = {
            name: 'Nouveau modèle',
            id: '',
            url: '',
            apikey: '',
            llm: 'mistral',
        };
        setSettings({
            ...settings,
            models: [...settings.models, newModel],
        });
    };

    const removeModel = (index: number) => {
        if (!settings || settings.models.length <= 1) return;
        const updatedModels = settings.models.filter((_, i) => i !== index);
        setSettings({
            ...settings,
            models: updatedModels,
        });
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                        <svg
                            className="w-6 h-6 mr-2 text-gray-600"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                            />
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                            />
                        </svg>
                        Paramètres
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
                    {loading && (
                        <div className="flex items-center justify-center py-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                            <span className="ml-2 text-gray-600">Chargement des paramètres...</span>
                        </div>
                    )}

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                            {error}
                        </div>
                    )}

                    {settings && (
                        <div className="space-y-8">
                            {/* Models Section */}
                            <div>
                                <h3 className="text-lg font-medium text-gray-900 mb-4">Modèles IA</h3>

                                {/* Default Model Selection */}
                                <div className="mb-6">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Modèle par défaut
                                    </label>
                                    <select
                                        value={settings.default_model}
                                        onChange={(e) => handleDefaultModelChange(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    >
                                        {settings.models.map((model) => (
                                            <option key={model.name} value={model.name}>
                                                {model.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                {/* Models List */}
                                <div className="space-y-4">
                                    {settings.models.map((model, index) => (
                                        <div key={index} className="border border-gray-200 rounded-lg p-4">
                                            <div className="flex items-center justify-between mb-3">
                                                <h4 className="text-md font-medium text-gray-800">Modèle {index + 1}</h4>
                                                {settings.models.length > 1 && (
                                                    <button
                                                        onClick={() => removeModel(index)}
                                                        className="text-red-600 hover:text-red-800 text-sm"
                                                    >
                                                        Supprimer
                                                    </button>
                                                )}
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div>
                                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                                        Nom du modèle
                                                    </label>
                                                    <input
                                                        type="text"
                                                        value={model.name}
                                                        onChange={(e) => handleModelChange(index, 'name', e.target.value)}
                                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                                    />
                                                </div>
                                                <div>
                                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                                        ID du modèle
                                                    </label>
                                                    <input
                                                        type="text"
                                                        value={model.id}
                                                        onChange={(e) => handleModelChange(index, 'id', e.target.value)}
                                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                                    />
                                                </div>
                                                <div>
                                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                                        URL de l'API
                                                    </label>
                                                    <input
                                                        type="url"
                                                        value={model.url}
                                                        onChange={(e) => handleModelChange(index, 'url', e.target.value)}
                                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                                    />
                                                </div>
                                                <div>
                                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                                        Clé API
                                                    </label>
                                                    <input
                                                        type="password"
                                                        value={model.apikey}
                                                        onChange={(e) => handleModelChange(index, 'apikey', e.target.value)}
                                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))}

                                    <button
                                        onClick={addModel}
                                        className="w-full py-2 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors"
                                    >
                                        + Ajouter un modèle
                                    </button>
                                </div>
                            </div>

                            {/* Prompts Section */}
                            <div>
                                <h3 className="text-lg font-medium text-gray-900 mb-4">Prompts</h3>

                                <div className="space-y-6">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Prompt de traitement d'articles
                                        </label>
                                        <textarea
                                            value={settings.prompts.article_processing}
                                            onChange={(e) => handlePromptChange('article_processing', e.target.value)}
                                            rows={8}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                            placeholder="Prompt utilisé pour traiter et reformater les articles..."
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Prompt de chat
                                        </label>
                                        <textarea
                                            value={settings.prompts.chat}
                                            onChange={(e) => handlePromptChange('chat', e.target.value)}
                                            rows={8}
                                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                                            placeholder="Prompt utilisé pour le chat avec l'IA..."
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="flex justify-end space-x-3 p-6 border-t bg-gray-50">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                    >
                        Annuler
                    </button>
                    <button
                        onClick={handleSave}
                        disabled={saving || !settings}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
                    >
                        {saving && (
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        )}
                        Sauvegarder
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;