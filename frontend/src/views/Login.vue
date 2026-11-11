<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Вход в систему</h2>
      
      <div class="input-group">
        <label>Логин</label>
        <input v-model="username" type="text" placeholder="Введите логин" @keyup.enter="login" />
      </div>
      
      <div class="input-group">
        <label>Пароль</label>
        <input v-model="password" type="password" placeholder="Введите пароль" @keyup.enter="login" />
      </div>
      
      <button @click="login" class="auth-btn" :disabled="loading">
        {{ loading ? 'Вход...' : 'Войти' }}
      </button>
      
      <!-- Ссылка на регистрацию -->
      <p class="auth-hint">Нет аккаунта? <router-link to="/register" style="color: #ff7f50; font-weight: bold; text-decoration: none;">Зарегистрироваться</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const username = ref('')
const password = ref('')
const loading = ref(false)

const login = async () => {
  if (!username.value || !password.value) return alert('Заполните все поля')
  
  loading.value = true
  try {
    await api.post('/login/', { username: username.value, password: password.value })
    window.location.href = '/' 
  } catch (e) {
    alert(e.response?.data?.detail || 'Неверный логин или пароль')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container { display: flex; justify-content: center; align-items: center; min-height: 60vh; }
.auth-card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 400px; }
.auth-title { text-align: center; margin-bottom: 30px; color: #333; }
.input-group { margin-bottom: 20px; }
.input-group label { display: block; margin-bottom: 8px; color: #555; font-weight: 500; }
.input-group input { width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; outline: none; transition: border-color 0.2s; }
.input-group input:focus { border-color: #ff7f50; }
.auth-btn { width: 100%; padding: 14px; font-size: 18px; margin-top: 10px; }
.auth-hint { text-align: center; color: #888; margin-top: 20px; font-size: 14px; }
</style>
