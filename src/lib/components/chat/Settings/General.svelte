<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { getLanguages, changeLanguage } from '$lib/i18n';
	const dispatch = createEventDispatcher();

	import { models, settings, theme, user } from '$lib/stores';

	const i18n = getContext('i18n');

	import AdvancedParams from './Advanced/AdvancedParams.svelte';
	import Textarea from '$lib/components/common/Textarea.svelte';
	export let saveSettings: Function;
	export let getModels: Function;

	// General
	let themes = ['dark', 'light'];
	let selectedTheme = 'system';

	let languages: Awaited<ReturnType<typeof getLanguages>> = [];
	let lang = $i18n.language;
	let notificationEnabled = false;
	let system = '';

	let showAdvanced = false;

	const toggleNotification = async () => {
		const permission = await Notification.requestPermission();

		if (permission === 'granted') {
			notificationEnabled = !notificationEnabled;
			saveSettings({ notificationEnabled: notificationEnabled });
		} else {
			toast.error(
				$i18n.t(
					'Response notifications cannot be activated as the website permissions have been denied. Please visit your browser settings to grant the necessary access.'
				)
			);
		}
	};

	let params = {
		// Advanced
		stream_response: null,
		function_calling: null,
		seed: null,
		temperature: null,
		reasoning_effort: null,
		logit_bias: null,
		frequency_penalty: null,
		presence_penalty: null,
		repeat_penalty: null,
		repeat_last_n: null,
		mirostat: null,
		mirostat_eta: null,
		mirostat_tau: null,
		top_k: null,
		top_p: null,
		min_p: null,
		stop: null,
		tfs_z: null,
		num_ctx: null,
		num_batch: null,
		num_keep: null,
		max_tokens: null,
		num_gpu: null
	};

	const saveHandler = async () => {
		saveSettings({
			system: system !== '' ? system : undefined,
			params: {
				stream_response: params.stream_response !== null ? params.stream_response : undefined,
				function_calling: params.function_calling !== null ? params.function_calling : undefined,
				seed: (params.seed !== null ? params.seed : undefined) ?? undefined,
				stop: params.stop ? params.stop.split(',').filter((e) => e) : undefined,
				temperature: params.temperature !== null ? params.temperature : undefined,
				reasoning_effort: params.reasoning_effort !== null ? params.reasoning_effort : undefined,
				logit_bias: params.logit_bias !== null ? params.logit_bias : undefined,
				frequency_penalty: params.frequency_penalty !== null ? params.frequency_penalty : undefined,
				presence_penalty: params.presence_penalty !== null ? params.presence_penalty : undefined,
				repeat_penalty: params.repeat_penalty !== null ? params.repeat_penalty : undefined,
				repeat_last_n: params.repeat_last_n !== null ? params.repeat_last_n : undefined,
				mirostat: params.mirostat !== null ? params.mirostat : undefined,
				mirostat_eta: params.mirostat_eta !== null ? params.mirostat_eta : undefined,
				mirostat_tau: params.mirostat_tau !== null ? params.mirostat_tau : undefined,
				top_k: params.top_k !== null ? params.top_k : undefined,
				top_p: params.top_p !== null ? params.top_p : undefined,
				min_p: params.min_p !== null ? params.min_p : undefined,
				tfs_z: params.tfs_z !== null ? params.tfs_z : undefined,
				num_ctx: params.num_ctx !== null ? params.num_ctx : undefined,
				num_batch: params.num_batch !== null ? params.num_batch : undefined,
				num_keep: params.num_keep !== null ? params.num_keep : undefined,
				max_tokens: params.max_tokens !== null ? params.max_tokens : undefined,
				use_mmap: params.use_mmap !== null ? params.use_mmap : undefined,
				use_mlock: params.use_mlock !== null ? params.use_mlock : undefined,
				num_thread: params.num_thread !== null ? params.num_thread : undefined,
				num_gpu: params.num_gpu !== null ? params.num_gpu : undefined,
				think: params.think !== null ? params.think : undefined,
				keep_alive: params.keep_alive !== null ? params.keep_alive : undefined,
				format: params.format !== null ? params.format : undefined
			}
		});
		dispatch('save');
	};

	onMount(async () => {
		selectedTheme = localStorage.theme ?? 'system';

		languages = await getLanguages();

		notificationEnabled = $settings.notificationEnabled ?? false;
		system = $settings.system ?? '';

		params = { ...params, ...$settings.params };
		params.stop = $settings?.params?.stop ? ($settings?.params?.stop ?? []).join(',') : null;
	});

	const applyTheme = (_theme: string) => {
		let themeToApply = _theme;

		if (_theme === 'system') {
			themeToApply = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
		}

		if (themeToApply === 'dark') {
			document.documentElement.style.setProperty('--color-gray-800', '#1f2937');
			document.documentElement.style.setProperty('--color-gray-850', '#111827');
			document.documentElement.style.setProperty('--color-gray-900', '#030712');
			document.documentElement.style.setProperty('--color-gray-950', '#020617');
		}

		themes
			.filter((e) => e !== themeToApply)
			.forEach((e) => {
				e.split(' ').forEach((e) => {
					document.documentElement.classList.remove(e);
				});
			});

		themeToApply.split(' ').forEach((e) => {
			document.documentElement.classList.add(e);
		});

		const metaThemeColor = document.querySelector('meta[name="theme-color"]');
		if (metaThemeColor) {
			if (_theme.includes('system')) {
				const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
					? 'dark'
					: 'light';
				console.log('Setting system meta theme color: ' + systemTheme);
				metaThemeColor.setAttribute('content', systemTheme === 'light' ? '#ffffff' : '#030712');
			} else {
				console.log('Setting meta theme color: ' + _theme);
				metaThemeColor.setAttribute(
					'content',
					_theme === 'dark' ? '#030712' : '#ffffff'
				);
			}
		}

		if (typeof window !== 'undefined' && window.applyTheme) {
			window.applyTheme();
		}

		console.log(_theme);
	};

	const themeChangeHandler = (_theme: string) => {
		theme.set(_theme);
		localStorage.setItem('theme', _theme);
		applyTheme(_theme);
	};
</script>

<div class="flex flex-col h-full justify-between text-sm text-gray-900 dark:text-gray-200">
	<div class="overflow-y-scroll max-h-[28rem] lg:max-h-full pr-2">
		<div class="space-y-4">
			<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
				<div class="mb-3 text-sm font-semibold text-gray-900 dark:text-gray-100">{$i18n.t('OAKMIND HIVE Einstellungen')}</div>

				<div class="space-y-3">
					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs font-medium text-gray-700 dark:text-gray-300">{$i18n.t('Design')}</div>
						<div class="flex items-center relative">
							<select
								class="bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 w-fit pr-8 rounded-lg py-2 px-3 text-xs text-gray-900 dark:text-gray-200 outline-none focus:border-gray-500 dark:focus:border-gray-500 transition-colors"
								bind:value={selectedTheme}
								placeholder="Select a theme"
								on:change={() => themeChangeHandler(selectedTheme)}
							>
								<option value="system">⚙️ {$i18n.t('System')}</option>
								<option value="dark">🌑 {$i18n.t('Dunkel')}</option>
								<option value="light">☀️ {$i18n.t('Hell')}</option>
							</select>
						</div>
					</div>

					<div class="flex w-full justify-between items-center">
						<div class="self-center text-xs font-medium text-gray-700 dark:text-gray-300">{$i18n.t('Sprache')}</div>
						<div class="flex items-center relative">
							<select
								class="bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 w-fit pr-8 rounded-lg py-2 px-3 text-xs text-gray-900 dark:text-gray-200 outline-none focus:border-gray-500 dark:focus:border-gray-500 transition-colors"
								bind:value={lang}
								placeholder="Select a language"
								on:change={(e) => {
									changeLanguage(lang);
								}}
							>
								{#each languages as language}
									<option value={language['code']}>{language['title']}</option>
								{/each}
							</select>
						</div>
					</div>
				</div>
			</div>
			{#if $i18n.language === 'en-US'}
				<div class="mb-2 text-xs text-gray-600 dark:text-gray-400">
					Couldn't find your language?
					<a
						class="text-gray-700 dark:text-gray-300 font-medium underline hover:text-gray-900 dark:hover:text-gray-200"
						href="https://github.com/open-webui/open-webui/blob/main/docs/CONTRIBUTING.md#-translations-and-internationalization"
						target="_blank"
					>
						Help us translate OAKMIND HIVE!
					</a>
				</div>
			{/if}

			<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
				<div class="flex w-full justify-between items-center">
					<div class="self-center text-xs font-medium text-gray-700 dark:text-gray-300">{$i18n.t('Benachrichtigungen')}</div>

					<button
						class="px-4 py-1.5 text-xs rounded-lg transition-all duration-200
						{notificationEnabled
							? 'bg-gray-700 dark:bg-gray-600 text-white border border-gray-600 dark:border-gray-500'
							: 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}"
						on:click={() => {
							toggleNotification();
						}}
						type="button"
					>
						{#if notificationEnabled === true}
							<span class="font-medium">{$i18n.t('Ein')}</span>
						{:else}
							<span class="font-medium">{$i18n.t('Aus')}</span>
						{/if}
					</button>
				</div>
			</div>

		</div>

		{#if $user?.role === 'admin' || $user?.permissions.chat?.controls}
			<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 mt-4">
				<div class="mb-3 text-sm font-semibold text-gray-900 dark:text-gray-100">{$i18n.t('System-Prompt')}</div>
				<Textarea
					bind:value={system}
					className="w-full text-sm text-gray-900 dark:text-gray-200 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg outline-none focus:border-gray-500 dark:focus:border-gray-500 transition-colors resize-none"
					rows="4"
					placeholder={$i18n.t('System-Prompt hier eingeben')}
				/>
			</div>

			<div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 mt-4">
				<div class="flex justify-between items-center text-sm mb-3">
					<div class="font-semibold text-gray-900 dark:text-gray-100">{$i18n.t('Erweiterte Parameter')}</div>
					<button
						class="text-xs font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 transition-colors"
						type="button"
						on:click={() => {
							showAdvanced = !showAdvanced;
						}}>{showAdvanced ? $i18n.t('Verbergen') : $i18n.t('Anzeigen')}</button
					>
				</div>

				{#if showAdvanced}
					<AdvancedParams admin={$user?.role === 'admin'} bind:params />
				{/if}
			</div>
		{/if}
	</div>

	<div class="flex justify-end pt-4 text-sm font-medium">
		<button
			class="px-6 py-2.5 text-sm font-medium bg-gray-700 dark:bg-gray-600 hover:bg-gray-800 dark:hover:bg-gray-700 text-white transition-all duration-200 rounded-xl shadow-lg border border-gray-600 dark:border-gray-500"
			on:click={() => {
				saveHandler();
			}}
		>
			{$i18n.t('Save')}
		</button>
	</div>
</div>
