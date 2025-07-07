<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '$lib/stores';

	onMount(async () => {
		if ($user?.role === 'admin') {
			await goto('/admin/users/overview');
		} else if ($user?.role === 'department_manager') {
			await goto('/admin/users/groups');
		} else {
			await goto('/');
		}
	});
</script>

<!-- This page redirects to the appropriate users section based on user role -->
