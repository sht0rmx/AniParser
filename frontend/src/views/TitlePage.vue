<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import pb from '@/pocketbase'

const route = useRoute()
const title = ref(null)
const loading = ref(true)

const loadTitle = async (alias) => {
  loading.value = true
  try {
    const items = await pb.collection('titles').getFullList(1, { filter: `alias="${alias}"` })
    title.value = items[0] || null
  } catch (e) {
    console.error("Error loading title", e)
  } finally {
    loading.value = false
  }
}

const syncTitle = async () => {
  if (!title.value) return
  // Здесь можно вызвать API для обновления данных с Shikimori / AniLiberty
  console.log("Sync title:", title.value.title)
}

onMounted(() => {
  if (route.params.alias) loadTitle(route.params.alias)
})
</script>

<template>
  <div v-if="loading" class="flex justify-center items-center h-64">
    <span class="text-gray-400 animate-pulse">Loading...</span>
  </div>

  <div v-else-if="title" class="flex flex-col md:flex-row gap-6 p-4 bg-base-100 rounded-xl shadow-md max-w-4xl mx-auto">
    <img
        v-if="title.posterScr"
        :src="title.posterOptScr || title.posterScr"
        :alt="title.title"
        class="w-full h-80 md:h-96 object-cover rounded-xl shadow-lg mb-4"
    />

    <!-- Info -->
    <div class="flex-1 flex flex-col justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">{{ title.title }}</h1>
        <p class="text-gray-500 flex gap-4 mt-2 text-sm">
          <span class="flex items-center gap-1"><i class="ri-calendar-fill"></i> {{ title.year }}</span>
          <span class="flex items-center gap-1"><i class="ri-heart-fill"></i> {{ title.favCount }}</span>
          <span class="flex items-center gap-1"><i class="ri-star-fill"></i> {{ title.score }}</span>
        </p>
        <p class="mt-2 text-gray-500">
          <span class="flex items-center gap-1"><i class="ri-tv-fill"></i> {{ title.type }}</span>
          <span class="flex items-center gap-1"><i class="ri-time-fill"></i> {{ title.avDuration }} min</span>
          <span class="flex items-center gap-1" v-if="title.season"><i class="ri-sun-line"></i> {{ title.season }}</span>
        </p>
        <p class="mt-2">{{ title.description }}</p>
        <div class="flex flex-wrap gap-2 mt-2">
          <span v-for="g in title.generes" :key="g" class="text-xs px-2 py-1 bg-base-200 rounded-full">{{ g }}</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex gap-3 mt-4">
        <a
          v-if="title.linkToView"
          :href="title.linkToView"
          class="btn btn-outline btn-accent flex items-center gap-2">
          <i class="ri-external-link-line"></i> Watch outside app
        </a>
        <button class="btn btn-outline btn-primary flex items-center gap-2 px-6.5" @click="syncTitle">
          <i class="ri-refresh-line"></i> Sync
        </button>
      </div>
      <button class="btn btn-outline btn-secondary flex items-center gap-2">
          <i class="ri-play-list-add-line"></i> Add to playlist
        </button>
    </div>
  </div>

  <div v-else class="flex flex-col items-center justify-center mt-20 text-gray-500">
  <i class="ri-error-warning-line text-6xl mb-4"></i>
  <span class="text-lg font-medium">Title not found</span>
</div>
</template>
