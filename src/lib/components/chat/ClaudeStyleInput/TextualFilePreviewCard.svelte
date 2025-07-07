<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { FileWithPreview } from './types';
	
	export let file: FileWithPreview;
	
	const dispatch = createEventDispatcher<{
		remove: string;
	}>();
	
	function handleRemove() {
		dispatch('remove', file.id);
	}
	
	function copyToClipboard() {
		if (file.textContent) {
			navigator.clipboard.writeText(file.textContent);
		}
	}
	
	function getFileExtension(filename: string): string {
		const extension = filename.split('.').pop()?.toUpperCase() || 'FILE';
		return extension.length > 8 ? extension.substring(0, 8) + '...' : extension;
	}
	
	$: previewText = file.textContent?.slice(0, 150) || '';
	$: needsTruncation = (file.textContent?.length || 0) > 150;
	$: fileExtension = getFileExtension(file.file.name);
</script>

<div class="bg-zinc-700 border border-zinc-600 relative rounded-lg p-3 size-[125px] shadow-md flex-shrink-0 overflow-hidden">
	<div class="text-[8px] text-zinc-300 whitespace-pre-wrap break-words max-h-24 overflow-y-auto custom-scrollbar">
		{#if file.textContent}
			{previewText}
			{#if needsTruncation}...{/if}
		{:else}
			<div class="flex items-center justify-center h-full text-zinc-400">
				<svg class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
			</div>
		{/if}
	</div>
	
	<!-- OVERLAY -->
	<div class="group absolute flex justify-start items-end p-2 inset-0 bg-gradient-to-b to-[#30302E] from-transparent overflow-hidden">
		<p class="capitalize text-white text-xs bg-zinc-800 border border-zinc-700 px-2 py-1 rounded-md">
			{fileExtension}
		</p>
		
		<!-- Upload status indicator -->
		{#if file.uploadStatus === 'uploading'}
			<div class="absolute top-2 left-2">
				<svg class="h-3.5 w-3.5 animate-spin text-blue-400" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
			</div>
		{/if}
		{#if file.uploadStatus === 'error'}
			<div class="absolute top-2 left-2">
				<svg class="h-3.5 w-3.5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			</div>
		{/if}
		
		<!-- Actions -->
		<div class="group-hover:opacity-100 opacity-0 transition-opacity duration-300 flex items-center gap-0.5 absolute top-2 right-2">
			{#if file.textContent}
				<button
					class="size-6 bg-zinc-600 hover:bg-zinc-500 border border-zinc-500 rounded-md flex items-center justify-center"
					on:click={copyToClipboard}
					title="Copy content"
					type="button"
				>
					<svg class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
					</svg>
				</button>
			{/if}
			<button
				class="size-6 bg-zinc-600 hover:bg-zinc-500 border border-zinc-500 rounded-md flex items-center justify-center"
				on:click={handleRemove}
				title="Remove file"
				type="button"
			>
				<svg class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	</div>
</div>

<style>
	.custom-scrollbar::-webkit-scrollbar {
		width: 2px;
	}
	.custom-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}
	.custom-scrollbar::-webkit-scrollbar-thumb {
		background-color: rgba(156, 163, 175, 0.5);
		border-radius: 1px;
	}
</style>
