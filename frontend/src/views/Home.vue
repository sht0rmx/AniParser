<script setup>
import { ref, onMounted, computed } from "vue";
import pb from '@/pocketbase';
import { useRouter } from 'vue-router';

const router = useRouter();

const titles = ref([]);
const page = ref(1);
const perPage = 20;
const totalPages = ref(1);
const loading = ref(true);
const searchQuery = ref("");

const goToTitle = (alias) => {
  if (!alias) return;
  router.push(`/titles/${alias}`);
};

const loadTitles = async (p = 1) => {
  loading.value = true;
  try {
    const res = await pb.collection("titles").getList(p, perPage, {
      filter: 'isOngoing=true',
      sort: "-created"
    });
    titles.value = res.items;
    page.value = res.page;
    totalPages.value = res.totalPages;
  } catch (e) {
    console.error("Error loading titles", e);
  } finally {
    loading.value = false;
  }
}

const filteredTitles = computed(() => {
  if (!searchQuery.value) return titles.value;
  return titles.value.filter(t =>
    t.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (t.titleEn && t.titleEn.toLowerCase().includes(searchQuery.value.toLowerCase()))
  );
});

const fetchFromAniLib = async (name) => {
  console.log("Fetch from AniLiberty:", name);

}


const handleSearch = () => {
  if (!filteredTitles.value.length && searchQuery.value.trim()) {
  }
}

onMounted(() => loadTitles());
</script>

<template>
  <!-- Info -->
  <div class="flex flex-col items-center justify-center space-y-3 mt-8 mb-12"> <i
      class="ri-drop-line text-8xl text-accent"></i>
    <h1 class="text-3xl font-bold">AniParseBot</h1>
    <p class="text-gray-400 text-base max-w-sm text-center"> AniParser is a bot for tracking the current season anime,
      collecting all anime, sending notifications about new episodes, and providing information about the selected
      anime. </p>
  </div>

  <!-- Search -->
  <div class="flex flex-col w-full max-w mx-auto p-2 mb-4">
    <label class="input input-bordered w-full relative">
      <i class="ri-search-line"></i>
      <input type="search" class="grow" placeholder="Search" v-model="searchQuery" @input="handleSearch" />
    </label>
  </div>

  <ul class="list bg-base-100 rounded-box shadow-md">
    <!-- Skeleton при загрузке -->
    <li v-if="loading" v-for="n in 8" :key="n" class="p-3 flex items-center gap-3">
      <div class="w-16 h-16 rounded-full bg-base-200 animate-pulse"></div>
      <div class="flex flex-col gap-2 w-full">
        <div class="h-4 w-40 bg-base-200 animate-pulse rounded"></div>
        <div class="h-3 w-24 bg-base-200 animate-pulse rounded"></div>
      </div>
    </li>

    <!-- Список найденных тайтлов -->
    <template v-else-if="filteredTitles.length">
      <li v-for="(t, i) in filteredTitles" :key="t.id" class="p-3 hover:bg-base-150 transition"
        :class="{ 'rounded-t-box': i === 0, 'rounded-b-box': i === filteredTitles.length - 1 }"
        @click="goToTitle(t.alias)">

        <div class="flex items-center gap-3">
          <img v-if="t.posterScr" :src="t.posterOptScr || t.posterScr" :alt="t.title"
            class="w-16 h-16 rounded-full object-cover shadow-md" />
          <div>
            <h3 class="text-lg font-semibold">{{ t.title }}</h3>
            <p class="text-gray-500 text-sm flex items-center gap-4">
              <span class="flex items-center gap-1"><i class="ri-calendar-fill"></i>{{ t.year }}</span>
              <span class="flex items-center gap-1"><i class="ri-heart-fill"></i>{{ t.favCount }}</span>
              <span class="flex items-center gap-1"><i class="ri-star-fill"></i>{{ t.score }}</span>
            </p>
          </div>
        </div>
      </li>
    </template>

    <!-- Если нет результатов -->
    <li v-else @click="fetchFromAniLib(searchQuery)"
      class="p-4 flex items-center gap-3 cursor-pointer hover:bg-base-200 rounded-box transition">
      <i class="ri-add-line text-3xl text-accent"></i>
      <span class="font-medium">Fetch "{{ searchQuery }}" from AniLiberty</span>
    </li>
  </ul>

  <!-- Pagination -->
  <div class="mt-6 flex items-center justify-center gap-4">
    <button v-if="!searchQuery" class="btn btn-ghost btn-sm" :disabled="page <= 1" @click="loadTitles(page - 1)">
      <i class="ri-arrow-left-line text-xl"></i>
    </button>
    <span class="text-lg font-semibold">{{ page }}</span>
    <button v-if="!searchQuery" class="btn btn-ghost btn-sm" :disabled="page >= totalPages" @click="loadTitles(page + 1)" >
      <i class="ri-arrow-right-line text-xl"></i>
    </button>
  </div>
</template>
