<template>
  <div>
    <h2 class="page-title">Мои заказы</h2>
    
    <div v-if="orders.length === 0" class="empty-state">У вас пока нет заказов</div>

    <div class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span>Заказ №{{ order.id }} от {{ new Date(order.created_at).toLocaleDateString() }}</span>
          <span :class="['badge', order.status]">{{ order.status_display }}</span>
        </div>
        <div class="order-body">
          <ul>
            <li v-for="item in order.items" :key="item.id">
              {{ item.name }} — {{ item.quantity }} шт.
            </li>
          </ul>
        </div>
        <div class="order-footer">
          <span>Время выдачи: {{ order.slot ? order.slot.time_from + ' - ' + order.slot.time_to : 'Не указано' }}</span>
          <span class="order-total">Итого: {{ order.total_amount }} ₽</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const orders = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/orders/my/')
    orders.value = res.data
  } catch (e) {
    console.error("Ошибка загрузки заказов")
  }
})
</script>

<style scoped>
.page-title { margin-bottom: 20px; color: #333; }
.empty-state { background: white; padding: 40px; text-align: center; border-radius: 12px; color: #888; }
.orders-list { display: flex; flex-direction: column; gap: 20px; }
.order-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.order-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }
.badge { padding: 4px 10px; border-radius: 20px; font-size: 14px; }
.badge.new { background: #e3f2fd; color: #1976d2; }
.badge.ready { background: #fff3e0; color: #f57c00; }
.badge.completed { background: #e8f5e9; color: #388e3c; }
.badge.cancelled { background: #ffebee; color: #d32f2f; }
.order-body ul { list-style: none; padding: 0; margin-bottom: 15px; }
.order-body li { padding: 5px 0; color: #555; }
.order-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #eee; padding-top: 15px; font-size: 14px; color: #888; }
.order-total { font-size: 20px; font-weight: bold; color: #ff7f50; }
</style>
