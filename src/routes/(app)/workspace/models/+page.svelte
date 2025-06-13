<script>
	import { onMount } from 'svelte';
	import { config, models, settings } from '$lib/stores';
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/workspace/Models.svelte';

	onMount(async () => {
		await Promise.all([
			(async () => {
				models.set(
					await getModels(
						localStorage.token,
						$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
					)
				);
			})()
		]);
	});
</script>

{#if $models !== null}
	<Models />
{/if}

<div class=" text-gray-600 dark:text-gray-400 text-xs mt-1 mb-2 px-4 py-2 bg-gray-50/50 dark:bg-gray-800/20 rounded-lg border border-gray-200 dark:border-gray-700">
	ⓘ Hier kannst du bestehende LLMs mit Wissen und Systemprompts erweitern, um Vorlagen zu erstellen, die dann im Chat zur Verfügung stehen.
</div>
