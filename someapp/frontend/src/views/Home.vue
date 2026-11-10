<template>
  <div class="menu">
    <h2>Меню на сегодня</h2>
    <div v-for="item in items" :key="item.id" class="card">
      <h3>{{ item.name }}</h3>
      <p>{{ item.description }}</p>
      <p><b>{{ item.price }} ₽</b></p>
      <button @click="addToCart(item.id)">В корзину</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const items = ref([])

onMounted(async () => {
  const res = await api.get('/menu/')
  items.value = res.data.items
})

const addToCart = async (id) => {
  await api.post('/cart/add/', { item_id: id })
  alert('Добавлено!')
}
</script>

<style>
.card { border: 1px solid #ccc; padding: 15px; margin: 10px; border-radius: 8px; }
</style>
