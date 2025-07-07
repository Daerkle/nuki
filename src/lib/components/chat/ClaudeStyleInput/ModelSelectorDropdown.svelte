<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { clickOutside } from './clickOutside';
	import type { ModelOption } from './types';
	
	export let models: ModelOption[] = [];
	export let selectedModel: string = '';
	
	const dispatch = createEventDispatcher<{
		change: string;
	}>();
	
	let isOpen = false;
	let selectedModelData: ModelOption | undefined;
	
	$: selectedModelData = models.find(m => m.id === selectedModel) || models[0];
	
	function handleModelChange(modelId: string) {
		dispatch('change', modelId);
		isOpen = false;
	}
	
	function handleClickOutside() {
		isOpen = false;
	}
</script>

<div class="relative" use:clickOutside={handleClickOutside}>
	<button
		class="h-9 px-2.5 text-sm font-medium text-zinc-300 hover:text-zinc-100 hover:bg-zinc-700 rounded-md transition-colors flex items-center gap-1"
		on:click={() => isOpen = !isOpen}
		type="button"
	>
		<span class="truncate max-w-[150px] sm:max-w-[200px]">
			{selectedModelData?.name || 'Select Model'}
		</span>
		<svg 
			class="ml-1 h-4 w-4 transition-transform {isOpen ? 'rotate-180' : ''}"
			fill="none" 
			viewBox="0 0 24 24" 
			stroke="currentColor"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
		</svg>
	</button>

	{#if isOpen}
		<div class="absolute bottom-full right-0 mb-2 w-72 bg-zinc-800 border border-zinc-700 rounded-lg shadow-xl z-20 p-2">
			{#each models as model (model.id)}
				<button
					class="w-full text-left p-2.5 rounded-md hover:bg-zinc-700 transition-colors flex items-center justify-between {model.id === selectedModel ? 'bg-zinc-700' : ''}"
					on:click={() => handleModelChange(model.id)}
					type="button"
				>
					<div>
						<div class="flex items-center gap-2">
							<span class="font-medium text-zinc-100">
								{model.name}
							</span>
							{#if model.badge}
								<span class="px-1.5 py-0.5 text-xs bg-blue-500/20 text-blue-300 rounded">
									{model.badge}
								</span>
							{/if}
						</div>
						{#if model.description}
							<p class="text-xs text-zinc-400 mt-0.5">
								{model.description}
							</p>
						{/if}
					</div>
					{#if model.id === selectedModel}
						<svg class="h-4 w-4 text-blue-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					{/if}
				</button>
			{/each}
		</div>
	{/if}
</div>
