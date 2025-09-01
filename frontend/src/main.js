import 'remixicon/fonts/remixicon.css'
import '@/assets/main.css'

import { createApp } from 'vue'
import { init, backButton, LaunchParamsRetrieveError } from '@telegram-apps/sdk'
import App from './App.vue'
import router from './router'

export let isTgEnv = false

try {
  init();
  isTgEnv = true
} catch (err) {
  if (err instanceof LaunchParamsRetrieveError) {
    isTgEnv = false
    console.warn('Not running inside Telegram. Redirecting to /need_auth')
    router.push('/need_auth')
  } else {
    throw err
  }
}

if (backButton.mount.isAvailable()) {
  backButton.mount()
  if (backButton.show.isAvailable()) {
    backButton.show()
  }
  const off = backButton.onClick(() => {
    off()
    window.history.back()
  })
}

const app = createApp(App)
app.use(router)
app.mount('#app')
