<script lang="ts">
	import { createEventDispatcher, onMount, tick } from 'svelte';
	import { v4 as uuidv4 } from 'uuid';
	import type { FileWithPreview, PastedContent, ModelOption } from './types';
	import ModelSelectorDropdown from './ModelSelectorDropdown.svelte';
	import FilePreviewCard from './FilePreviewCard.svelte';
	import PastedContentCard from './PastedContentCard.svelte';
	
	// Props
	export let disabled = false;
	export let placeholder = 'How can I help you today?';
	export let maxFiles = 10;
	export let maxFileSize = 50 * 1024 * 1024; // 50MB
	export let acceptedFileTypes: string[] | undefined = undefined;
	export let models: ModelOption[] = [];
	export let selectedModel = '';
	export let message = '';
	export let transparentBackground = false;
	
	// OpenWebUI specific props
	export let webSearchEnabled = false;
	export let imageGenerationEnabled = false;
	export let codeInterpreterEnabled = false;
	export let selectedToolIds: string[] = [];
	export let recording = false;
	
	const dispatch = createEventDispatcher<{
		submit: string;
		modelChange: string;
		fileSelect: FileList;
		webSearchToggle: boolean;
		imageGenerationToggle: boolean;
		codeInterpreterToggle: boolean;
		voiceRecord: void;
	}>();
	
	// State
	let files: FileWithPreview[] = [];
	let pastedContent: PastedContent[] = [];
	let isDragging = false;
	let textareaRef: HTMLTextAreaElement;
	let fileInputRef: HTMLInputElement;
	
	const PASTE_THRESHOLD = 200;
	
	// Auto-resize textarea
	$: if (textareaRef && message !== undefined) {
		tick().then(() => {
			textareaRef.style.height = 'auto';
			const maxHeight = 120;
			textareaRef.style.height = `${Math.min(textareaRef.scrollHeight, maxHeight)}px`;
		});
	}
	
	function handleFileSelect(selectedFiles: FileList | null) {
		if (!selectedFiles) return;
		
		const currentFileCount = files.length;
		if (currentFileCount >= maxFiles) {
			alert(`Maximum ${maxFiles} files allowed. Please remove some files to add new ones.`);
			return;
		}
		
		const availableSlots = maxFiles - currentFileCount;
		const filesToAdd = Array.from(selectedFiles).slice(0, availableSlots);
		
		if (selectedFiles.length > availableSlots) {
			alert(`You can only add ${availableSlots} more file(s). ${selectedFiles.length - availableSlots} file(s) were not added.`);
		}
		
		const newFiles = filesToAdd
			.filter((file) => {
				if (file.size > maxFileSize) {
					alert(`File ${file.name} exceeds size limit.`);
					return false;
				}
				if (acceptedFileTypes && !acceptedFileTypes.some(type => 
					file.type.includes(type) || type === file.name.split('.').pop()
				)) {
					alert(`File type for ${file.name} not supported.`);
					return false;
				}
				return true;
			})
			.map((file) => ({
				id: uuidv4(),
				file,
				preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined,
				type: file.type || 'application/octet-stream',
				uploadStatus: 'pending' as const,
				uploadProgress: 0,
			}));
		
		files = [...files, ...newFiles];
		
		// Read text content for textual files
		newFiles.forEach((fileToUpload) => {
			if (isTextualFile(fileToUpload.file)) {
				readFileAsText(fileToUpload.file)
					.then((textContent) => {
						files = files.map((f) =>
							f.id === fileToUpload.id ? { ...f, textContent } : f
						);
					})
					.catch((error) => {
						console.error('Error reading file content:', error);
					});
			}
		});
		
		// Dispatch to parent for actual upload handling
		const dataTransfer = new DataTransfer();
		filesToAdd.forEach(file => dataTransfer.items.add(file));
		dispatch('fileSelect', dataTransfer.files);
	}
	
	function isTextualFile(file: File): boolean {
		const textualTypes = [
			'text/', 'application/json', 'application/xml', 
			'application/javascript', 'application/typescript',
		];
		
		const textualExtensions = [
			'txt', 'md', 'py', 'js', 'ts', 'jsx', 'tsx', 'html', 'htm', 'css', 'scss', 'sass',
			'json', 'xml', 'yaml', 'yml', 'csv', 'sql', 'sh', 'bash', 'php', 'rb', 'go',
			'java', 'c', 'cpp', 'h', 'hpp', 'cs', 'rs', 'swift', 'kt', 'scala', 'r',
			'vue', 'svelte', 'astro', 'config', 'conf', 'ini', 'toml', 'log', 'gitignore',
			'dockerfile', 'makefile', 'readme',
		];
		
		const isTextualMimeType = textualTypes.some((type) =>
			file.type.toLowerCase().startsWith(type)
		);
		
		const extension = file.name.split('.').pop()?.toLowerCase() || '';
		const isTextualExtension = textualExtensions.includes(extension) ||
			file.name.toLowerCase().includes('readme') ||
			file.name.toLowerCase().includes('dockerfile') ||
			file.name.toLowerCase().includes('makefile');
		
		return isTextualMimeType || isTextualExtension;
	}
	
	function readFileAsText(file: File): Promise<string> {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = (e) => resolve((e.target?.result as string) || '');
			reader.onerror = (e) => reject(e);
			reader.readAsText(file);
		});
	}
	
	function removeFile(id: string) {
		const fileToRemove = files.find((f) => f.id === id);
		if (fileToRemove?.preview) {
			URL.revokeObjectURL(fileToRemove.preview);
		}
		files = files.filter((f) => f.id !== id);
	}
	
	function removePastedContent(id: string) {
		pastedContent = pastedContent.filter((c) => c.id !== id);
	}
	
	function handlePaste(e: ClipboardEvent) {
		const clipboardData = e.clipboardData;
		if (!clipboardData) return;
		
		const items = clipboardData.items;
		const fileItems = Array.from(items).filter(item => item.kind === 'file');
		
		if (fileItems.length > 0 && files.length < maxFiles) {
			e.preventDefault();
			const pastedFiles = fileItems
				.map(item => item.getAsFile())
				.filter(Boolean) as File[];
			const dataTransfer = new DataTransfer();
			pastedFiles.forEach(file => dataTransfer.items.add(file));
			handleFileSelect(dataTransfer.files);
			return;
		}
		
		const textData = clipboardData.getData('text');
		if (textData && textData.length > PASTE_THRESHOLD && pastedContent.length < 5) {
			e.preventDefault();
			message = message + textData.slice(0, PASTE_THRESHOLD) + '...';
			
			const pastedItem: PastedContent = {
				id: uuidv4(),
				content: textData,
				timestamp: new Date(),
				wordCount: textData.split(/\s+/).filter(Boolean).length,
			};
			
			pastedContent = [...pastedContent, pastedItem];
		}
	}
	
	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		if (e.dataTransfer?.types?.includes('Files')) {
			isDragging = true;
		}
	}
	
	function handleDragLeave() {
		isDragging = false;
	}
	
	function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
		if (e.dataTransfer?.files) {
			handleFileSelect(e.dataTransfer.files);
		}
	}
	
	function handleSend() {
		if (disabled || (!message.trim() && files.length === 0 && pastedContent.length === 0)) {
			return;
		}
		
		dispatch('submit', message);
		
		// Reset state
		message = '';
		files.forEach(file => {
			if (file.preview) URL.revokeObjectURL(file.preview);
		});
		files = [];
		pastedContent = [];
		
		if (textareaRef) {
			textareaRef.style.height = 'auto';
		}
	}
	
	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
			e.preventDefault();
			handleSend();
		}
	}
	
	function handleModelChange(modelId: string) {
		dispatch('modelChange', modelId);
	}
	
	$: hasContent = message.trim() || files.length > 0 || pastedContent.length > 0;
	$: canSend = hasContent && !disabled;
</script>

<div
	class="relative w-full max-w-2xl mx-auto"
	on:dragover={handleDragOver}
	on:dragleave={handleDragLeave}
	on:drop={handleDrop}
	role="application"
	aria-label="Chat input"
>
	{#if isDragging}
		<div class="absolute inset-0 z-50 bg-blue-900/20 border-2 border-dashed border-blue-500 rounded-xl flex flex-col items-center justify-center pointer-events-none">
			<p class="text-sm text-blue-500 flex items-center gap-2">
				<svg class="size-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
				</svg>
				Drop files here to add to chat
			</p>
		</div>
	{/if}

	<div class="bg-[#30302E] border border-zinc-700 rounded-xl shadow-lg items-end gap-2 min-h-[150px] flex flex-col">
		<textarea
			bind:this={textareaRef}
			bind:value={message}
			on:paste={handlePaste}
			on:keydown={handleKeyDown}
			{placeholder}
			{disabled}
			class="flex-1 min-h-[100px] w-full p-4 focus-within:border-none focus:outline-none focus:border-none border-none outline-none focus-within:ring-0 focus-within:ring-offset-0 focus-within:outline-none max-h-[120px] resize-none border-0 bg-transparent text-zinc-100 shadow-none focus-visible:ring-0 placeholder:text-zinc-500 text-sm sm:text-base custom-scrollbar"
			rows="1"
		/>
		
		<div class="flex items-center gap-2 justify-between w-full px-3 pb-1.5">
			<div class="flex items-center gap-2">
				<!-- File Upload Button -->
				<button
					class="h-9 w-9 p-0 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700 flex-shrink-0 rounded-md transition-colors flex items-center justify-center"
					on:click={() => fileInputRef?.click()}
					{disabled}
					title={files.length >= maxFiles ? `Max ${maxFiles} files reached` : 'Attach files'}
					type="button"
				>
					<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
					</svg>
				</button>
				
				<!-- Voice Recording Button -->
				<button
					class="h-9 w-9 p-0 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700 flex-shrink-0 rounded-md transition-colors flex items-center justify-center"
					on:click={() => dispatch('voiceRecord')}
					{disabled}
					title="Voice input"
					type="button"
				>
					<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
					</svg>
				</button>
				
				<!-- Tool Toggles -->
				{#if webSearchEnabled !== undefined}
					<button
						class="px-2 py-1.5 text-xs rounded-full transition-colors {webSearchEnabled ? 'bg-blue-500/20 text-blue-300' : 'text-zinc-400 hover:text-zinc-200'}"
						on:click={() => dispatch('webSearchToggle', !webSearchEnabled)}
						title="Web Search"
						type="button"
					>
						Web
					</button>
				{/if}
				
				{#if imageGenerationEnabled !== undefined}
					<button
						class="px-2 py-1.5 text-xs rounded-full transition-colors {imageGenerationEnabled ? 'bg-blue-500/20 text-blue-300' : 'text-zinc-400 hover:text-zinc-200'}"
						on:click={() => dispatch('imageGenerationToggle', !imageGenerationEnabled)}
						title="Image Generation"
						type="button"
					>
						Image
					</button>
				{/if}
				
				{#if codeInterpreterEnabled !== undefined}
					<button
						class="px-2 py-1.5 text-xs rounded-full transition-colors {codeInterpreterEnabled ? 'bg-blue-500/20 text-blue-300' : 'text-zinc-400 hover:text-zinc-200'}"
						on:click={() => dispatch('codeInterpreterToggle', !codeInterpreterEnabled)}
						title="Code Interpreter"
						type="button"
					>
						Code
					</button>
				{/if}
			</div>
			
			<div class="flex items-center gap-2">
				{#if models && models.length > 0}
					<ModelSelectorDropdown
						{models}
						{selectedModel}
						on:change={(e) => handleModelChange(e.detail)}
					/>
				{/if}

				<button
					class="h-9 w-9 p-0 flex-shrink-0 rounded-md transition-colors {canSend ? 'bg-amber-600 hover:bg-amber-700 text-white' : 'bg-zinc-700 text-zinc-500 cursor-not-allowed'} flex items-center justify-center"
					on:click={handleSend}
					disabled={!canSend}
					title="Send message"
					type="button"
				>
					<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
					</svg>
				</button>
			</div>
		</div>
		
		{#if files.length > 0 || pastedContent.length > 0}
			<div class="overflow-x-auto border-t border-zinc-700 p-3 w-full bg-[#262624]">
				<div class="flex gap-3">
					{#each pastedContent as content (content.id)}
						<PastedContentCard
							{content}
							on:remove={(e) => removePastedContent(e.detail)}
						/>
					{/each}
					{#each files as file (file.id)}
						<FilePreviewCard
							{file}
							on:remove={(e) => removeFile(e.detail)}
						/>
					{/each}
				</div>
			</div>
		{/if}
	</div>

	<input
		bind:this={fileInputRef}
		type="file"
		multiple
		class="hidden"
		accept={acceptedFileTypes?.join(',')}
		on:change={(e) => {
			handleFileSelect(e.currentTarget.files);
			if (e.currentTarget) e.currentTarget.value = '';
		}}
	/>
</div>

<style>
	.custom-scrollbar::-webkit-scrollbar {
		width: 4px;
	}
	.custom-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}
	.custom-scrollbar::-webkit-scrollbar-thumb {
		background-color: rgba(156, 163, 175, 0.5);
		border-radius: 2px;
	}
</style>
