<script lang="ts">
	import { onMount } from 'svelte';
	import { ClaudeStyleInput, type ModelOption } from '$lib/components/chat/ClaudeStyleInput';
	
	let selectedModel = '';
	let message = '';
	let webSearchEnabled = false;
	let imageGenerationEnabled = false;
	let codeInterpreterEnabled = false;
	
	// Static demo models - no dependency on stores
	const claudeModels: ModelOption[] = [
		{
			id: 'gpt-4',
			name: 'GPT-4',
			description: 'Most capable model for complex tasks',
			badge: 'Vision',
			info: {}
		},
		{
			id: 'gpt-3.5-turbo',
			name: 'GPT-3.5 Turbo',
			description: 'Fast and efficient for most tasks',
			badge: undefined,
			info: {}
		},
		{
			id: 'claude-3-opus',
			name: 'Claude 3 Opus',
			description: 'Anthropic\'s most powerful model',
			badge: 'Vision',
			info: {}
		},
		{
			id: 'llama-2-70b',
			name: 'Llama 2 70B',
			description: 'Open source large language model',
			badge: undefined,
			info: {}
		}
	];
	
	// Set default model
	onMount(() => {
		if (claudeModels.length > 0 && !selectedModel) {
			selectedModel = claudeModels[0].id;
		}
	});
	
	function handleSubmit(event: CustomEvent<string>) {
		console.log('Message submitted:', event.detail);
		alert(`Message sent: "${event.detail}"`);
	}
	
	function handleModelChange(event: CustomEvent<string>) {
		selectedModel = event.detail;
		console.log('Model changed to:', selectedModel);
	}
	
	function handleFileSelect(event: CustomEvent<FileList>) {
		console.log('Files selected:', Array.from(event.detail));
	}
	
	function handleWebSearchToggle(event: CustomEvent<boolean>) {
		webSearchEnabled = event.detail;
		console.log('Web search:', webSearchEnabled);
	}
	
	function handleImageGenerationToggle(event: CustomEvent<boolean>) {
		imageGenerationEnabled = event.detail;
		console.log('Image generation:', imageGenerationEnabled);
	}
	
	function handleCodeInterpreterToggle(event: CustomEvent<boolean>) {
		codeInterpreterEnabled = event.detail;
		console.log('Code interpreter:', codeInterpreterEnabled);
	}
	
	function handleVoiceRecord() {
		console.log('Voice recording requested');
		alert('Voice recording would start here');
	}
</script>

<svelte:head>
	<title>Claude-Style Interface Demo • NUKI</title>
</svelte:head>

<div class="min-h-screen bg-[#262624] flex items-center justify-center p-4">
	<div class="w-full max-w-4xl">
		<div class="mb-8 text-center py-16">
			<h1 class="text-3xl font-serif font-light text-[#C2C0B6] mb-2">
				Claude-Style Interface Demo
			</h1>
			<p class="text-zinc-400 text-sm">
				Modernes Chat-Interface im Claude-Stil für OpenWebUI
			</p>
		</div>
		
		<ClaudeStyleInput
			models={claudeModels}
			{selectedModel}
			bind:message
			{webSearchEnabled}
			{imageGenerationEnabled}
			{codeInterpreterEnabled}
			placeholder="Wie kann ich Ihnen heute helfen?"
			maxFiles={10}
			maxFileSize={10 * 1024 * 1024}
			on:submit={handleSubmit}
			on:modelChange={handleModelChange}
			on:fileSelect={handleFileSelect}
			on:webSearchToggle={handleWebSearchToggle}
			on:imageGenerationToggle={handleImageGenerationToggle}
			on:codeInterpreterToggle={handleCodeInterpreterToggle}
			on:voiceRecord={handleVoiceRecord}
		/>
		
		<div class="mt-8 text-sm text-zinc-500 space-y-2">
			<p><strong>Features:</strong></p>
			<ul class="list-disc list-inside space-y-1 ml-4">
				<li>Upload textual files (.md, .py, .html, .js, etc.) to see content preview</li>
				<li>Upload images/media files to see the traditional file preview</li>
				<li>Paste large text content to see pasted content cards</li>
				<li>Drag and drop files for easy uploading</li>
				<li>Copy content from textual files and pasted content</li>
				<li>Model selection with dropdown</li>
				<li>Tool toggles (Web Search, Image Generation, Code Interpreter)</li>
				<li>Voice recording button</li>
			</ul>
		</div>
		
		<div class="mt-6 p-4 bg-zinc-800 rounded-lg">
			<h3 class="text-zinc-200 font-medium mb-2">Current State:</h3>
			<div class="text-xs text-zinc-400 space-y-1">
				<p><strong>Selected Model:</strong> {selectedModel || 'None'}</p>
				<p><strong>Message:</strong> {message || 'Empty'}</p>
				<p><strong>Web Search:</strong> {webSearchEnabled ? 'Enabled' : 'Disabled'}</p>
				<p><strong>Image Generation:</strong> {imageGenerationEnabled ? 'Enabled' : 'Disabled'}</p>
				<p><strong>Code Interpreter:</strong> {codeInterpreterEnabled ? 'Enabled' : 'Disabled'}</p>
			</div>
		</div>
	</div>
</div>
