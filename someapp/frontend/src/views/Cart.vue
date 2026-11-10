<template>
  <div>
    <h2>Корзина</h2>
    <ul>
      <li v-for="item in cart.items" :key="item.id">
        {{ item.name }} - {{ item.quantity }} шт. = {{ item.subtotal }} ₽
      </li>
    </ul>
    <h3>Итого: {{ cart.total }} ₽</h3>
    
    <select v-model="slotId">
      <option value="">Выберите время</option>
      <option v-for="slot in slots" :key="slot.id" :value="slot.id">
        {{ slot.time_from }} - {{ slot.time_to }}
      </option>
    </select>
    <button @click="checkout" :disabled="!slotId">Оформить заказ</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const cart = ref({ items: [], total: 0 })
const slots = ref([])
const slotId = ref('')
const router = useRouter()

onMounted(async () => {
  cart.value = (await api.get('/cart/')).data
  slots.value = (await api.get('/slots/')).data
})

const checkout = async () => {
  try {
    await api.post('/orders/create/', { slot_id: slotId.value })
    alert('Заказ создан!')
    router.push('/')
  } catch (e) {
    alert('Ошибка или не авторизован')
  }
}
</script>
