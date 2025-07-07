export interface FileWithPreview {
	id: string;
	file: File;
	preview?: string;
	type: string;
	uploadStatus: 'pending' | 'uploading' | 'complete' | 'error';
	uploadProgress?: number;
	abortController?: AbortController;
	textContent?: string;
	// OpenWebUI specific fields
	collection_name?: string;
	url?: string;
	name?: string;
	size?: number;
	status?: string;
	itemId?: string;
	error?: string;
}

export interface PastedContent {
	id: string;
	content: string;
	timestamp: Date;
	wordCount: number;
}

export interface ModelOption {
	id: string;
	name: string;
	description?: string;
	badge?: string;
	info?: Record<string, unknown>;
}
