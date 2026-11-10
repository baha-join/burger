<template>
  <nav>
    <router-link to="/">Меню</router-link> |
    <router-link to="/cart">Корзина</router-link> |
    
    <template v-if="user">
      <span class="user-info">👤 {{ user.username }}</span> |
      <a href="#" @click.prevent="logout" class="logout-btn">Выйти</a>
    </template>
    
    <template v-else>
      <router-link to="/login">Войти</router-link>
    </template>
  </nav>
  <router-view :key="$route.fullPath" />
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
    alert('Вы вышли из системы')
  } catch (e) {
    alert('Ошибка при выходе')
  }
}

onMounted(() => {
  checkAuth()
})
</script>

<style>
nav { padding: 20px; background: #f8f9fa; text-align: center; }
nav a { margin: 0 10px; text-decoration: none; font-weight: bold; color: #4200ff; }
nav a:hover { text-decoration: underline; }
.user-info { font-weight: bold; color: #333; }
.logout-btn { color: #dc3545; cursor: pointer; }
</style>
