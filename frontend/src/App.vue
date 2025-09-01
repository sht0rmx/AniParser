<template>
  <div :class="['flex flex-col min-h-screen', { 'pb-14': $route.path !== '/need_auth' }]">
    
    <main :class="['flex-1 text-sm text-base-content flex justify-center', { 'p-4': $route.path !== '/need_auth' }]">
      <div :class="[
        'w-full',
        $route.path === '/need_auth' ? 'max-w-sm' : 'max-w-2xl'
      ]">
        <router-view />
      </div>
    </main>

    <BottomDock v-if="$route.path !== '/need_auth'"/>
  </div>
</template>

<script setup>
import BottomDock from '@/components/BottomDock.vue'
import pb from '@/pocketbase';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const initData = ref(null);

async function authWithTelegram() {
  if (!initData.value) {
    console.error('No initData available');
    return;
  }
  try {
    const res = await pb.collection('users').authWithTelegram(initData.value);
    console.log('Auth successful:', res);
  } catch (err) {
    console.error('Auth failed:', err);
    router.push('/need_auth');
  }
}

onMounted(() => {
  if (window.Telegram && window.Telegram.WebApp) {
    initData.value = window.Telegram.WebApp.initData;
    console.log('Telegram WebApp is ready!');
    authWithTelegram();
  } else {
    console.error('window.Telegram.WebApp is not available.');
    router.push('/need_auth');
  }
});
</script>