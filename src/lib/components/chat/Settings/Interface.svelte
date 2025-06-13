<script lang="ts">
	import { config, models, settings, user } from '$lib/stores';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { updateUserInfo } from '$lib/apis/users';
	import { getUserPosition } from '$lib/utils';
	const dispatch = createEventDispatcher();

	const i18n = getContext('i18n');

	export let saveSettings: Function;

	let backgroundImageUrl = null;
	let inputFiles = null;
	let filesInputElement;

	// Addons
	let titleAutoGenerate = true;
	let autoFollowUps = true;
	let autoTags = true;

	let responseAutoCopy = false;
	let widescreenMode = false;
	let splitLargeChunks = false;
	let scrollOnBranchChange = true;
	let userLocation = false;

	// Interface
	let defaultModelId = '';
	let showUsername = false;

	let notificationSound = true;
	let notificationSoundAlways = false;

	let highContrastMode = false;

	let detectArtifacts = true;

	let richTextInput = true;
	let promptAutocomplete = false;

	let largeTextAsFile = false;

	let landingPageMode = '';
	let chatBubble = true;
	let chatDirection: 'LTR' | 'RTL' | 'auto' = 'auto';
	let ctrlEnterToSend = false;
	let copyFormatted = false;

	let collapseCodeBlocks = false;
	let expandDetails = false;

	let imageCompression = false;
	let imageCompressionSize = {
		width: '',
		height: ''
	};

	// chat export
	let stylizedPdfExport = true;

	// Admin - Show Update Available Toast
	let showUpdateToast = true;
	let showChangelog = true;

	let showEmojiInCall = false;
	let voiceInterruption = false;
	let hapticFeedback = false;

	let webSearch = null;

	let iframeSandboxAllowSameOrigin = false;
	let iframeSandboxAllowForms = false;

	const toggleExpandDetails = () => {
		expandDetails = !expandDetails;
		saveSettings({ expandDetails });
	};

	const toggleCollapseCodeBlocks = () => {
		collapseCodeBlocks = !collapseCodeBlocks;
		saveSettings({ collapseCodeBlocks });
	};

	const toggleSplitLargeChunks = async () => {
		splitLargeChunks = !splitLargeChunks;
		saveSettings({ splitLargeChunks: splitLargeChunks });
	};

	const toggleHighContrastMode = async () => {
		highContrastMode = !highContrastMode;
		saveSettings({ highContrastMode: highContrastMode });
	};

	const togglePromptAutocomplete = async () => {
		promptAutocomplete = !promptAutocomplete;
		saveSettings({ promptAutocomplete: promptAutocomplete });
	};

	const togglesScrollOnBranchChange = async () => {
		scrollOnBranchChange = !scrollOnBranchChange;
		saveSettings({ scrollOnBranchChange: scrollOnBranchChange });
	};

	const toggleWidescreenMode = async () => {
		widescreenMode = !widescreenMode;
		saveSettings({ widescreenMode: widescreenMode });
	};

	const toggleChatBubble = async () => {
		chatBubble = !chatBubble;
		saveSettings({ chatBubble: chatBubble });
	};

	const toggleLandingPageMode = async () => {
		landingPageMode = landingPageMode === '' ? 'chat' : '';
		saveSettings({ landingPageMode: landingPageMode });
	};

	const toggleShowUpdateToast = async () => {
		showUpdateToast = !showUpdateToast;
		saveSettings({ showUpdateToast: showUpdateToast });
	};

	const toggleNotificationSound = async () => {
		notificationSound = !notificationSound;
		saveSettings({ notificationSound: notificationSound });
	};

	const toggleNotificationSoundAlways = async () => {
		notificationSoundAlways = !notificationSoundAlways;
		saveSettings({ notificationSoundAlways: notificationSoundAlways });
	};

	const toggleShowChangelog = async () => {
		showChangelog = !showChangelog;
		saveSettings({ showChangelog: showChangelog });
	};

	const toggleShowUsername = async () => {
		showUsername = !showUsername;
		saveSettings({ showUsername: showUsername });
	};

	const toggleEmojiInCall = async () => {
		showEmojiInCall = !showEmojiInCall;
		saveSettings({ showEmojiInCall: showEmojiInCall });
	};

	const toggleVoiceInterruption = async () => {
		voiceInterruption = !voiceInterruption;
		saveSettings({ voiceInterruption: voiceInterruption });
	};

	const toggleImageCompression = async () => {
		imageCompression = !imageCompression;
		saveSettings({ imageCompression });
	};

	const toggleHapticFeedback = async () => {
		hapticFeedback = !hapticFeedback;
		saveSettings({ hapticFeedback: hapticFeedback });
	};

	const toggleStylizedPdfExport = async () => {
		stylizedPdfExport = !stylizedPdfExport;
		saveSettings({ stylizedPdfExport: stylizedPdfExport });
	};

	const toggleUserLocation = async () => {
		userLocation = !userLocation;

		if (userLocation) {
			const position = await getUserPosition().catch((error) => {
				toast.error(error.message);
				return null;
			});

			if (position) {
				await updateUserInfo(localStorage.token, { location: position });
				toast.success($i18n.t('User location successfully retrieved.'));
			} else {
				userLocation = false;
			}
		}

		saveSettings({ userLocation });
	};

	const toggleTitleAutoGenerate = async () => {
		titleAutoGenerate = !titleAutoGenerate;
		saveSettings({
			title: {
				...$settings.title,
				auto: titleAutoGenerate
			}
		});
	};

	const toggleAutoFollowUps = async () => {
		autoFollowUps = !autoFollowUps;
		saveSettings({ autoFollowUps });
	};

	const toggleAutoTags = async () => {
		autoTags = !autoTags;
		saveSettings({ autoTags });
	};

	const toggleDetectArtifacts = async () => {
		detectArtifacts = !detectArtifacts;
		saveSettings({ detectArtifacts });
	};

	const toggleRichTextInput = async () => {
		richTextInput = !richTextInput;
		saveSettings({ richTextInput });
	};

	const toggleLargeTextAsFile = async () => {
		largeTextAsFile = !largeTextAsFile;
		saveSettings({ largeTextAsFile });
	};

	const toggleResponseAutoCopy = async () => {
		const permission = await navigator.clipboard
			.readText()
			.then(() => {
				return 'granted';
			})
			.catch(() => {
				return '';
			});

		console.log(permission);

		if (permission === 'granted') {
			responseAutoCopy = !responseAutoCopy;
			saveSettings({ responseAutoCopy: responseAutoCopy });
		} else {
			toast.error(
				$i18n.t(
					'Clipboard write permission denied. Please check your browser settings to grant the necessary access.'
				)
			);
		}
	};

	const toggleCopyFormatted = async () => {
		copyFormatted = !copyFormatted;
		saveSettings({ copyFormatted });
	};

	const toggleChangeChatDirection = async () => {
		if (chatDirection === 'auto') {
			chatDirection = 'LTR';
		} else if (chatDirection === 'LTR') {
			chatDirection = 'RTL';
		} else if (chatDirection === 'RTL') {
			chatDirection = 'auto';
		}
		saveSettings({ chatDirection });
	};

	const togglectrlEnterToSend = async () => {
		ctrlEnterToSend = !ctrlEnterToSend;
		saveSettings({ ctrlEnterToSend });
	};

	const updateInterfaceHandler = async () => {
		saveSettings({
			models: [defaultModelId],
			imageCompressionSize: imageCompressionSize
		});
	};

	const toggleWebSearch = async () => {
		webSearch = webSearch === null ? 'always' : null;
		saveSettings({ webSearch: webSearch });
	};

	const toggleIframeSandboxAllowSameOrigin = async () => {
		iframeSandboxAllowSameOrigin = !iframeSandboxAllowSameOrigin;
		saveSettings({ iframeSandboxAllowSameOrigin });
	};

	const toggleIframeSandboxAllowForms = async () => {
		iframeSandboxAllowForms = !iframeSandboxAllowForms;
		saveSettings({ iframeSandboxAllowForms });
	};

	onMount(async () => {
		titleAutoGenerate = $settings?.title?.auto ?? true;
		autoTags = $settings?.autoTags ?? true;
		autoFollowUps = $settings?.autoFollowUps ?? true;

		highContrastMode = $settings?.highContrastMode ?? false;

		detectArtifacts = $settings?.detectArtifacts ?? true;
		responseAutoCopy = $settings?.responseAutoCopy ?? false;

		showUsername = $settings?.showUsername ?? false;
		showUpdateToast = $settings?.showUpdateToast ?? true;
		showChangelog = $settings?.showChangelog ?? true;

		showEmojiInCall = $settings?.showEmojiInCall ?? false;
		voiceInterruption = $settings?.voiceInterruption ?? false;

		richTextInput = $settings?.richTextInput ?? true;
		promptAutocomplete = $settings?.promptAutocomplete ?? false;
		largeTextAsFile = $settings?.largeTextAsFile ?? false;
		copyFormatted = $settings?.copyFormatted ?? false;

		collapseCodeBlocks = $settings?.collapseCodeBlocks ?? false;
		expandDetails = $settings?.expandDetails ?? false;

		landingPageMode = $settings?.landingPageMode ?? '';
		chatBubble = $settings?.chatBubble ?? true;
		widescreenMode = $settings?.widescreenMode ?? false;
		splitLargeChunks = $settings?.splitLargeChunks ?? false;
		scrollOnBranchChange = $settings?.scrollOnBranchChange ?? true;
		chatDirection = $settings?.chatDirection ?? 'auto';
		userLocation = $settings?.userLocation ?? false;

		notificationSound = $settings?.notificationSound ?? true;
		notificationSoundAlways = $settings?.notificationSoundAlways ?? false;

		iframeSandboxAllowSameOrigin = $settings?.iframeSandboxAllowSameOrigin ?? false;
		iframeSandboxAllowForms = $settings?.iframeSandboxAllowForms ?? false;

		stylizedPdfExport = $settings?.stylizedPdfExport ?? true;

		hapticFeedback = $settings?.hapticFeedback ?? false;
		ctrlEnterToSend = $settings?.ctrlEnterToSend ?? false;

		imageCompression = $settings?.imageCompression ?? false;
		imageCompressionSize = $settings?.imageCompressionSize ?? { width: '', height: '' };

		defaultModelId = $settings?.models?.at(0) ?? '';
		if ($config?.default_models) {
			defaultModelId = $config.default_models.split(',')[0];
		}

		backgroundImageUrl = $settings?.backgroundImageUrl ?? null;
		webSearch = $settings?.webSearch ?? null;
	});
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm text-gray-700 dark:text-gray-200"
	on:submit|preventDefault={() => {
		updateInterfaceHandler();
		dispatch('save');
	}}
>
	<input
		bind:this={filesInputElement}
		bind:files={inputFiles}
		type="file"
		hidden
		accept="image/*"
		on:change={() => {
			let reader = new FileReader();
			reader.onload = (event) => {
				let originalImageUrl = `${event.target.result}`;

				backgroundImageUrl = originalImageUrl;
				saveSettings({ backgroundImageUrl });
			};

			if (
				inputFiles &&
				inputFiles.length > 0 &&
				['image/gif', 'image/webp', 'image/jpeg', 'image/png'].includes(inputFiles[0]['type'])
			) {
				reader.readAsDataURL(inputFiles[0]);
			} else {
				console.log(`Unsupported File Type '${inputFiles[0]['type']}'.`);
				inputFiles = null;
			}
		}}
	/>

	<div class="space-y-4 overflow-y-scroll max-h-[28rem] lg:max-h-full pr-2">
		<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
			<div class="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100">{$i18n.t('Benutzeroberfläche')}</div>

			<div class="space-y-3">
				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">
						{$i18n.t('Hoher Kontrast Modus')} ({$i18n.t('Beta')})
					</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{highContrastMode
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleHighContrastMode();
						}}
						type="button"
					>
						<span class="font-medium">{highContrastMode ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Startseiten-Modus')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
						on:click={() => {
							toggleLandingPageMode();
						}}
						type="button"
					>
						<span class="font-medium">{landingPageMode === '' ? $i18n.t('Standard') : $i18n.t('Chat')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Chat-Blasen UI')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{chatBubble
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleChatBubble();
						}}
						type="button"
					>
						<span class="font-medium">{chatBubble ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
					</button>
				</div>

				{#if !$settings.chatBubble}
					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs text-gray-600 dark:text-gray-300">
							{$i18n.t('Benutzername statt "Du" im Chat anzeigen')}
						</div>

						<button
							class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
							{showUsername
								? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
								: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
							on:click={() => {
								toggleShowUsername();
							}}
							type="button"
						>
							<span class="font-medium">{showUsername ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
						</button>
					</div>
				{/if}

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Breitbild-Modus')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{widescreenMode
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleWidescreenMode();
						}}
						type="button"
					>
						<span class="font-medium">{widescreenMode ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Chat-Richtung')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
						on:click={toggleChangeChatDirection}
						type="button"
					>
						{#if chatDirection === 'LTR'}
							<span class="ml-2 self-center">{$i18n.t('LTR')}</span>
						{:else if chatDirection === 'RTL'}
							<span class="ml-2 self-center">{$i18n.t('RTL')}</span>
						{:else}
							<span class="ml-2 self-center">{$i18n.t('Auto')}</span>
						{/if}
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">
						{$i18n.t('Notification Sound')}
					</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{notificationSound
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleNotificationSound();
						}}
						type="button"
					>
						<span class="font-medium">{notificationSound ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				{#if notificationSound}
					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs text-gray-600 dark:text-gray-300">
							{$i18n.t('Benachrichtigungston immer abspielen')}
						</div>

						<button
							class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
							{notificationSoundAlways
								? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
								: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
							on:click={() => {
								toggleNotificationSoundAlways();
							}}
							type="button"
						>
							<span class="font-medium">{notificationSoundAlways ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
						</button>
					</div>
				{/if}

				{#if $user?.role === 'admin'}
					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs text-gray-600 dark:text-gray-300">
							{$i18n.t('Toast-Benachrichtigungen für neue Updates')}
						</div>

						<button
							class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
							{showUpdateToast
								? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
								: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
							on:click={() => {
								toggleShowUpdateToast();
							}}
							type="button"
						>
							<span class="font-medium">{showUpdateToast ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
						</button>
					</div>

					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs text-gray-600 dark:text-gray-300">
							{$i18n.t('"Was ist neu" Modal beim Login anzeigen')}
						</div>

						<button
							class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
							{showChangelog
								? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
								: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
							on:click={() => {
								toggleShowChangelog();
							}}
							type="button"
						>
							<span class="font-medium">{showChangelog ? $i18n.t('Ein') : $i18n.t('Aus')}</span>
						</button>
					</div>
				{/if}
			</div>
		</div>

		<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
			<div class="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100">{$i18n.t('Chat')}</div>

			<div class="space-y-3">
				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Titel-Automatische Generierung')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{titleAutoGenerate
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleTitleAutoGenerate();
						}}
						type="button"
					>
						<span class="font-medium">{titleAutoGenerate ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Follow-Up Automatische Generierung')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{autoFollowUps
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleAutoFollowUps();
						}}
						type="button"
					>
						<span class="font-medium">{autoFollowUps ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">{$i18n.t('Chat Tags Auto-Generation')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{autoTags
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleAutoTags();
						}}
						type="button"
					>
						<span class="font-medium">{autoTags ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">
						{$i18n.t('Detect Artifacts Automatically')}
					</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{detectArtifacts
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleDetectArtifacts();
						}}
						type="button"
					>
						<span class="font-medium">{detectArtifacts ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">
						{$i18n.t('Auto-Copy Response to Clipboard')}
					</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{responseAutoCopy
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleResponseAutoCopy();
						}}
						type="button"
					>
						<span class="font-medium">{responseAutoCopy ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>

				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs text-gray-600 dark:text-gray-300">
						{$i18n.t('Rich Text Input for Chat')}
					</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{richTextInput
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-400 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleRichTextInput();
						}}
						type="button"
					>
						<span class="font-medium">{richTextInput ? $i18n.t('On') : $i18n.t('Off')}</span>
					</button>
				</div>
			</div>
		</div>
	</div>

	<div class="flex justify-end pt-3">
		<button
			class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-lg transition-all duration-200"
			type="submit"
		>
			{$i18n.t('Save')}
		</button>
	</div>
</form>
