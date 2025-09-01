<template>
    <div class="flex flex-col space-y-2 mt-8 mb-12">
        <h1 class="text-4xl font-bold">
            Settings
        </h1>
        <p class="text-gray-400 text-base">Setup notifications and see other info</p>
    </div>
    <div class="flex flex-col w-full max-w- mx-auto p-2 mb-10">
        <ul class="list bg-base-100 rounded-box shadow-md w-full relative">
            <li class="list-row items-center">
                <i class="ri-notification-line text-2xl"></i>
                <div>
                    <div>Notifications</div>
                </div>
                <button class="btn btn-square btn-ghost">
                    <i class="ri-arrow-right-s-line"></i>
                </button>
            </li>

            <li class="list-row items-center">
                <i class="ri-github-fill text-2xl"></i>
                <div>
                    <div>Authors</div>
                </div>
                <button class="btn btn-square btn-ghost">
                    <i class="ri-arrow-right-s-line"></i>
                </button>
            </li>

            <li class="list-row items-center">
                <i class="ri-delete-bin-6-line text-2xl text-error"></i>
                <div>
                    <div>Clear data</div>
                </div>
                <button class="btn btn-square btn-ghost">
                    <i class="ri-arrow-right-s-line"></i>
                </button>
            </li>
        </ul>
    </div>
    <div class="text-center items-center text-sm text-gray-400 mt-5 space-y-2">
        Made with ❤️ <div class="badge-sm" :class="buttonClass" @click="fetchStatus();">{{ status }}</div>
        <br/>
        <div class="badge badge-sm badge-soft badge-info" @click="checkAuth();">{{ status_auth }}</div>
    </div>
</template>

<script setup lang="js">
import { ref } from 'vue';
import pb from '@/pocketbase';


const buttonClass = ref('badge badge-outline badge-info');
const status = ref('Loading...');
const status_auth = ref('...')

async function checkAuth() {
    const result = pb.authStore.isValid
    if (result) {
        status_auth.value = "Auth: Ok"
    }
    else {
        status_auth.value = "Auth: Error"
    }
}

async function fetchStatus() {
  try {
    const result = await pb.health.check();
    if (result.code != 200) {
      buttonClass.value = 'badge badge-error';
      status.value = 'API Unavailable';
    } 
    else {
      buttonClass.value = 'badge badge-success';
      status.value = result.message;
    }
  } catch (error) {
    console.error('Failed to fetch PocketBase status:', error);
    buttonClass.value = 'badge badge-warning';
    status.value = 'DB Unavailable';
  }
}

fetchStatus();
checkAuth();
</script>