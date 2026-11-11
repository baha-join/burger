<template>
  <div>
    <h2 class="page-title">Кухня (Очередь заказов)</h2>
    <div v-if="orders.length === 0" class="empty-state">Нет активных заказов</div>

    <div class="staff-grid">
      <div v-for="order in orders" :key="order.id" class="order-card" :class="order.status">
        <h3>Заказ №{{ order.id }} ({{ order.username }})</h3>
        <p class="time">Выдача: {{ order.slot ? order.slot.time_from + ' - ' + order.slot.time_to : '?' }}</p>
        <ul>
          <li v-for="item in order.items" :key="item.id">{{ item.quantity }} × {{ item.name }}</li>
        </ul>
        <div class="actions">
          <button v-if="order.status === 'new'" @click="updateStatus(order.id, 'ready')" class="btn-ready">Готов</button>
          <button v-if="order.status === 'ready'" @click="updateStatus(order.id, 'completed')" class="btn-done">Выдан</button>
          <button @click="updateStatus(order.id, 'cancelled')" class="btn-cancel">Отменить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const orders = ref([])

const loadOrders = async () => {
  try {
    const res = await api.get('/staff/orders/')
    orders.value = res.data
  } catch (e) {
    alert("Нет доступа или ошибка сервера")
  }
}

const updateStatus = async (id, status) => {
  // Убираем обратные слэши (используем конкатенацию строк)
  const url = '/staff/orders/' + id + '/status/'
  await api.patch(url, { status })
  loadOrders()
}

onMounted(loadOrders)
</script>

<style scoped>
.staff-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.order-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #ccc; }
.order-card.new { border-left-color: #1976d2; }
.order-card.ready { border-left-color: #f57c00; }
h3 { margin-bottom: 10px; }
.time { color: #ff7f50; font-weight: bold; margin-bottom: 10px; }
ul { padding-left: 20px; margin-bottom: 15px; color: #555; }
.actions { display: flex; gap: 10px; }
.btn-ready { background: #f57c00; }
.btn-done { background: #388e3c; }
.btn-cancel { background: #d32f2f; padding: 10px; }
</style>
