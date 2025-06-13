<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher, onMount, getContext, tick } from 'svelte';
	import { getModels as _getModels, getToolServersData } from '$lib/apis';

	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	import { models, settings, toolServers, user } from '$lib/stores';

	import Switch from '$lib/components/common/Switch.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Plus from '$lib/components/icons/Plus.svelte';
	import Connection from './Tools/Connection.svelte';

	import AddServerModal from '$lib/components/AddServerModal.svelte';

	export let saveSettings: Function;

	let servers = null;
	let showConnectionModal = false;

	const addConnectionHandler = async (server) => {
		servers = [...servers, server];
		await updateHandler();
	};

	const updateHandler = async () => {
		await saveSettings({
			toolServers: servers
		});

		toolServers.set(await getToolServersData($i18n, $settings?.toolServers ?? []));
	};

	onMount(async () => {
		servers = $settings?.toolServers ?? [];
	});
</script>

<AddServerModal bind:show={showConnectionModal} onSubmit={addConnectionHandler} direct />

<form
	class="flex flex-col h-full justify-between text-sm text-gray-700 dark:text-gray-200"
	on:submit|preventDefault={() => {
		updateHandler();
	}}
>
	<div class="overflow-y-scroll scrollbar-hidden h-full pr-2">
		{#if servers !== null}
			<div class="space-y-4">
				<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
					<div class="flex justify-between items-center mb-4">
						<div class="text-sm font-semibold text-gray-800 dark:text-gray-100">{$i18n.t('Tool-Server verwalten')}</div>

						<Tooltip content={$i18n.t(`Server hinzufügen`)}>
							<button
								class="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
								on:click={() => {
									showConnectionModal = true;
								}}
								type="button"
							>
								<Plus className="w-4 h-4 text-gray-600 dark:text-gray-300" />
							</button>
						</Tooltip>
					</div>

					<div class="flex flex-col gap-2">
							{#each servers as server, idx}
								<Connection
									bind:connection={server}
									direct
									onSubmit={() => {
										updateHandler();
									}}
									onDelete={() => {
										servers = servers.filter((_, i) => i !== idx);
										updateHandler();
									}}
								/>
							{/each}
						</div>

					<div class="mt-4 p-3 bg-gray-100 dark:bg-gray-900/50 rounded-lg">
						<div class="text-xs text-gray-600 dark:text-gray-400">
							{$i18n.t('Verbinden Sie sich mit Ihren eigenen OpenAPI-kompatiblen externen Tool-Servern.')}
							<br />
							{$i18n.t(
								'CORS muss vom Anbieter ordnungsgemäß konfiguriert werden, um Anfragen von OAKMIND HIVE zu ermöglichen.'
							)}
						</div>
					</div>

					<div class="mt-3 text-xs text-gray-600 dark:text-gray-400">
						<a
							class="underline hover:text-gray-800 dark:hover:text-gray-300 transition-colors"
							href="https://github.com/open-webui/openapi-servers"
							target="_blank">{$i18n.t('Erfahren Sie mehr über OpenAPI Tool-Server.')}</a
						>
					</div>
				</div>
			</div>
		{:else}
			<div class="flex h-full justify-center">
				<div class="my-auto">
					<Spinner className="size-6" />
				</div>
			</div>
		{/if}
	</div>

	<div class="flex justify-end pt-4 text-sm font-medium">
		<button
			class="px-6 py-2.5 text-sm font-medium bg-gray-700 dark:bg-gray-600 hover:bg-gray-800 dark:hover:bg-gray-700 text-white transition-all duration-200 rounded-xl shadow-lg border border-gray-600 dark:border-gray-500"
			type="submit"
		>
			{$i18n.t('Speichern')}
		</button>
	</div>
</form>
