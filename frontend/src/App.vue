<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="nav-links">
        <router-link to="/" class="logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
            <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
            <path d="M7 2v20"></path>
            <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>
          </svg>
          Столовая
        </router-link>
        
        <router-link to="/">Меню</router-link>
        <router-link to="/cart">Корзина</router-link>
        <router-link v-if="user" to="/orders">Мои заказы</router-link>
        <router-link v-if="user && user.is_staff" to="/staff" style="color: #d32f2f; font-weight: bold;">Кухня (Staff)</router-link>
      </div>
      
      <div class="nav-auth">
        <template v-if="user">
          <span class="user-info">{{ user.username }}</span>
          <a href="#" @click.prevent="logout" class="logout-btn">Выйти</a>
        </template>
        <template v-else>
          <!-- Оставили только одну кнопку -->
          <router-link to="/login" class="login-btn">Войти</router-link>
        </template>
      </div>
    </nav>
    <main class="container">
      <router-view :key="$route.fullPath" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from './api'
import { useRouter } from 'vue-router'

const user = ref(null)
const router = useRouter()

const checkAuth = async () => {
  try {
    const res = await api.get('/me/')
    user.value = res.data
  } catch (e) {
    user.value = null
  }
}

const logout = async () => {
  try {
    await api.post('/logout/')
    user.value = null
    router.push('/')
  } catch (e) {
    alert('Ошибка')
  }
}

onMounted(() => { checkAuth() })
</script>

<style scoped>
.navbar { display: flex; justify-content: space-between; align-items: center; background-color: white; padding: 15px 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 30px; }
.nav-links { display: flex; align-items: center; gap: 20px; }
.logo { font-size: 24px; font-weight: bold; color: #ff7f50 !important; text-decoration: none; margin-right: 20px; display: flex; align-items: center; }
.nav-links a:not(.logo) { text-decoration: none; color: #333; font-weight: 500; }
.nav-links a:not(.logo):hover { color: #ff7f50; }
.nav-auth { display: flex; align-items: center; gap: 15px; }
.user-info { font-weight: bold; color: #555; }
.logout-btn { color: #dc3545; text-decoration: none; font-weight: bold; }
.login-btn { background-color: #ff7f50; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; }
</style>
