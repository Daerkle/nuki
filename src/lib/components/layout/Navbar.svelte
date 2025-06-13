<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	import {
		WEBUI_NAME,
		chatId,
		mobile,
		settings,
		showArchivedChats,
		showControls,
		showSidebar,
		temporaryChatEnabled,
		user
	} from '$lib/stores';

	import { slide } from 'svelte/transition';
	import ShareChatModal from '../chat/ShareChatModal.svelte';
	import ModelSelector from '../chat/ModelSelector.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Menu from './Navbar/Menu.svelte';
	import { page } from '$app/stores';
	import UserMenu from './Sidebar/UserMenu.svelte';
	import MenuLines from '../icons/MenuLines.svelte';
	import AdjustmentsHorizontal from '../icons/AdjustmentsHorizontal.svelte';
	import Map from '../icons/Map.svelte';
	import { stringify } from 'postcss';
	import PencilSquare from '../icons/PencilSquare.svelte';
	import Plus from '../icons/Plus.svelte';

	const i18n = getContext('i18n');

	export let initNewChat: Function;
	export let title: string = $WEBUI_NAME;
	export let shareEnabled: boolean = false;

	export let chat;
	export let selectedModels;
	export let showModelSelector = true;

	let showShareChatModal = false;
	let showDownloadChatModal = false;
</script>

<ShareChatModal bind:show={showShareChatModal} chatId={$chatId} />

<!-- Navbar mit angepasstem Padding für Model Selector -->
<div class="sticky top-0 z-30 w-full bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
	<div class="flex items-center px-3 py-3">
		<!-- Sidebar Toggle -->
		<div class="{$showSidebar ? 'md:hidden' : ''} mr-2">
			<button
				id="sidebar-toggle-button"
				class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
				on:click={() => {
					showSidebar.set(!$showSidebar);
				}}
				aria-label="Toggle Sidebar"
			>
				<MenuLines />
			</button>
		</div>

		<!-- Model Selector mit mehr Platz -->
		<div class="flex-1 min-w-0 mx-2">
			{#if showModelSelector}
				<ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
			{/if}
		</div>

		<!-- Action Buttons -->
		<div class="flex items-center gap-1 ml-2">
			{#if shareEnabled && chat && (chat.id || $temporaryChatEnabled)}
				<Menu
					{chat}
					{shareEnabled}
					shareHandler={() => {
						showShareChatModal = !showShareChatModal;
					}}
					downloadHandler={() => {
						showDownloadChatModal = !showDownloadChatModal;
					}}
				>
					<button
						class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
						id="chat-context-menu-button"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="size-5"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
							/>
						</svg>
					</button>
				</Menu>
			{/if}

			{#if $mobile || !$mobile}
				<Tooltip content={$i18n.t('Controls')}>
					<button
						class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
						on:click={async () => {
							await showControls.set(!$showControls);
						}}
						aria-label="Controls"
					>
						<AdjustmentsHorizontal className="size-5" strokeWidth="1.5" />
					</button>
				</Tooltip>
			{/if}

			<Tooltip content={$i18n.t('New Chat')}>
				<button
					id="new-chat-button"
					class="p-1.5 {$showSidebar ? 'md:hidden' : ''} rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
					on:click={() => {
						initNewChat();
					}}
					aria-label="New Chat"
				>
					<PencilSquare className="size-5" strokeWidth="1.5" />
				</button>
			</Tooltip>

			{#if $user !== undefined}
				<UserMenu
					className="max-w-[240px]"
					role={$user?.role}
					help={true}
					on:show={(e) => {
						if (e.detail === 'archived-chat') {
							showArchivedChats.set(true);
						}
					}}
				>
					<button
						class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
						aria-label="User Menu"
					>
						<img
							src={$user?.profile_image_url}
							class="size-7 object-cover rounded-full"
							alt="User profile"
							draggable="false"
						/>
					</button>
				</UserMenu>
			{/if}
		</div>
	</div>
</div>
