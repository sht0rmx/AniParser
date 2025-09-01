<script setup>
</script>

<template>
  <!-- Info -->
  <div class="flex flex-col items-center justify-center space-y-3 mt-8 mb-12">
    <!-- <img src="/logo.jpg" alt="Logo" class="w-24 h-24 rounded-full object-cover" /> -->
    <i class="ri-drop-line text-8xl text-accent"></i>
    <h1 class="text-3xl font-bold">AniParseBot</h1>
    <p class="text-gray-400 text-base max-w-sm text-center">
      AniParser is a bot for tracking the current season anime, 
      collecting all anime, sending notifications about new 
      episodes, and providing information about the selected anime.
    </p>
  </div>
  <!-- Search -->
  <div class="flex flex-col w-full max-w- mx-auto p-2">
    <label class="input input-bordered w-full relative">
      <i class="ri-search-line"></i>
      <input type="search" class="grow" placeholder="Search" />
    </label>
  </div>

</template>
