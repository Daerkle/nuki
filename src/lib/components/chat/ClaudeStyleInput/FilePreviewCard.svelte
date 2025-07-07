<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { FileWithPreview } from './types';
	import TextualFilePreviewCard from './TextualFilePreviewCard.svelte';
	
	export let file: FileWithPreview;
	
	const dispatch = createEventDispatcher<{
		remove: string;
	}>();
	
	function handleRemove() {
		dispatch('remove', file.id);
	}
	
	function formatFileSize(bytes: number): string {
		if (bytes === 0) return '0 Bytes';
		const k = 1024;
		const sizes = ['Bytes', 'KB', 'MB', 'GB'];
		const i = Math.floor(Math.log(bytes) / Math.log(k));
		return (
			Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
		);
	}
	
	function getFileTypeLabel(type: string): string {
		const parts = type.split('/');
		let label = parts[parts.length - 1].toUpperCase();
		if (label.length > 7 && label.includes('-')) {
			label = label.substring(0, label.indexOf('-'));
		}
		if (label.length > 10) {
			label = label.substring(0, 10) + '...';
		}
		return label;
	}
	
	function isTextualFile(file: File): boolean {
		const textualTypes = [
			'text/',
			'application/json',
			'application/xml',
			'application/javascript',
			'application/typescript',
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
		const isTextualExtension =
			textualExtensions.includes(extension) ||
			file.name.toLowerCase().includes('readme') ||
			file.name.toLowerCase().includes('dockerfile') ||
			file.name.toLowerCase().includes('makefile');

		return isTextualMimeType || isTextualExtension;
	}
	
	$: isImage = file.type.startsWith('image/');
	$: isTextual = isTextualFile(file.file);
</script>

{#if isTextual}
	<TextualFilePreviewCard {file} on:remove={handleRemove} />
{:else}
	<div class="relative group bg-zinc-700 border w-fit border-zinc-600 rounded-lg {isImage ? 'p-0' : 'p-3'} size-[125px] shadow-md flex-shrink-0 overflow-hidden">
		<div class="flex items-start gap-3 size-[125px] overflow-hidden">
			{#if isImage && file.preview}
				<div class="relative size-full rounded-md overflow-hidden bg-zinc-600">
					<img
						src={file.preview}
						alt={file.file.name}
						class="w-full h-full object-cover"
					/>
				</div>
			{:else}
				<div class="flex-1 min-w-0 overflow-hidden">
					<div class="flex items-center gap-1.5 mb-1">
						<div class="group absolute flex justify-start items-end p-2 inset-0 bg-gradient-to-b to-[#30302E] from-transparent overflow-hidden">
							<p class="absolute bottom-2 left-2 capitalize text-white text-xs bg-zinc-800 border border-zinc-700 px-2 py-1 rounded-md">
								{getFileTypeLabel(file.type)}
							</p>
						</div>
						{#if file.uploadStatus === 'uploading'}
							<svg class="h-3.5 w-3.5 animate-spin text-blue-400" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
						{/if}
						{#if file.uploadStatus === 'error'}
							<svg class="h-3.5 w-3.5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						{/if}
					</div>

					<p class="max-w-[90%] text-xs font-medium text-zinc-100 truncate" title={file.file.name}>
						{file.file.name}
					</p>
					<p class="text-[10px] text-zinc-500 mt-1">
						{formatFileSize(file.file.size)}
					</p>
				</div>
			{/if}
		</div>
		
		<button
			class="absolute top-1 right-1 h-6 w-6 p-0 opacity-0 group-hover:opacity-100 bg-zinc-600 hover:bg-zinc-500 border border-zinc-500 rounded-md transition-opacity flex items-center justify-center"
			on:click={handleRemove}
			type="button"
		>
			<svg class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
			</svg>
		</button>
	</div>
{/if}
