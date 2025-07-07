<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { PastedContent } from './types';
	
	export let content: PastedContent;
	
	const dispatch = createEventDispatcher<{
		remove: string;
	}>();
	
	function handleRemove() {
		dispatch('remove', content.id);
	}
	
	function copyToClipboard() {
		navigator.clipboard.writeText(content.content);
	}
	
	$: previewText = content.content.slice(0, 150);
	$: needsTruncation = content.content.length > 150;
</script>

<div class="bg-zinc-700 border border-zinc-600 relative rounded-lg p-3 size-[125px] shadow-md flex-shrink-0 overflow-hidden">
	<div class="text-[8px] text-zinc-300 whitespace-pre-wrap break-words max-h-24 overflow-y-auto custom-scrollbar">
		{previewText}
		{#if needsTruncation}...{/if}
	</div>
	
	<!-- OVERLAY -->
	<div class="group absolute flex justify-start items-end p-2 inset-0 bg-gradient-to-b to-[#30302E] from-transparent overflow-hidden">
		<p class="capitalize text-white text-xs bg-zinc-800 border border-zinc-700 px-2 py-1 rounded-md">
			PASTED
		</p>
		
		<!-- Actions -->
		<div class="group-hover:opacity-100 opacity-0 transition-opacity duration-300 flex items-center gap-0.5 absolute top-2 right-2">
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
			<button
				class="size-6 bg-zinc-600 hover:bg-zinc-500 border border-zinc-500 rounded-md flex items-center justify-center"
				on:click={handleRemove}
				title="Remove content"
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
