<template>
  <div>
    <h2>Вход</h2>
    <input v-model="username" placeholder="Логин" />
    <input v-model="password" type="password" placeholder="Пароль" />
    <button @click="login">Войти</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const username = ref('')
const password = ref('')

const login = async () => {
  try {
    await api.post('/login/', { username: username.value, password: password.value })
    alert('Успех!')
    window.location.href = '/' // Перезагружаем страницу, чтобы App.vue обновил навигацию
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка')
  }
}
</script>
