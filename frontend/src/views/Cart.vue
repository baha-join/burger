<template>
  <div class="cart-page">
    <h2 class="page-title">Ваш заказ</h2>

    <div v-if="cart.items.length === 0" class="empty-cart">
      <h3>Корзина пуста</h3>
      <router-link to="/" class="btn">Перейти в меню</router-link>
    </div>

    <div v-else class="cart-grid">
      <!-- Список товаров -->
      <div class="cart-items">
        <div v-for="item in cart.items" :key="item.id" class="cart-item">
          <div class="item-info">
            <h4>{{ item.name }}</h4>
            <p class="item-price">{{ item.price }} ₽ × {{ item.quantity }} шт.</p>
          </div>
          <div class="item-actions">
            <span class="item-subtotal">{{ item.subtotal }} ₽</span>
            <button @click="removeItem(item.id)" class="remove-btn">✕</button>
          </div>
        </div>
      </div>

      <!-- Блок оформления -->
      <div class="checkout-panel">
        <h3>Итого: <span class="total-price">{{ cart.total }} ₽</span></h3>
        <hr />
        
        <div class="slot-select">
          <label>Время выдачи:</label>
          <select v-model="slotId">
            <option value="">Выберите время</option>
            <option v-for="slot in slots" :key="slot.id" :value="slot.id">
              {{ slot.time_from }} - {{ slot.time_to }}
            </option>
          </select>
        </div>

        <button @click="checkout" class="checkout-btn" :disabled="!slotId || loading">
          {{ loading ? 'Оформление...' : 'Оформить заказ' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const cart = ref({ items: [], total: 0 })
const slots = ref([])
const slotId = ref('')
const loading = ref(false)
const router = useRouter()

const loadData = async () => {
  try {
    const cartRes = await api.get('/cart/')
    cart.value = cartRes.data
    
    const slotsRes = await api.get('/slots/')
    slots.value = slotsRes.data
  } catch (e) {
    console.error(e)
  }
}

const removeItem = async (id) => {
  // Для удаления мы просто очищаем корзину (в упрощенной версии API нет отдельного метода удаления)
  await api.post('/cart/clear/')
  await loadData()
}

const checkout = async () => {
  loading.value = true
  try {
    await api.post('/orders/create/', { slot_id: slotId.value })
    alert('Заказ успешно оформлен!')
    router.push('/')
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка при оформлении заказа')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-title {
  margin-bottom: 25px;
  color: #333;
}

.empty-cart {
  background: white;
  padding: 50px;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.empty-cart h3 {
  margin-bottom: 20px;
  color: #666;
}

.cart-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.cart-items {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-info h4 {
  margin-bottom: 5px;
  font-size: 18px;
}

.item-price {
  color: #888;
  font-size: 14px;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.item-subtotal {
  font-weight: bold;
  color: #ff7f50;
  font-size: 18px;
}

.remove-btn {
  background: #ffe5e5;
  color: #ff4d4d;
  padding: 5px 10px;
  border-radius: 6px;
  font-weight: bold;
}

.remove-btn:hover {
  background: #ff4d4d;
  color: white;
}

.checkout-panel {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  height: fit-content;
}

.checkout-panel h3 {
  margin-bottom: 15px;
  color: #333;
}

.total-price {
  color: #ff7f50;
  font-size: 28px;
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin-bottom: 20px;
}

.slot-select {
  margin-bottom: 25px;
}

.slot-select label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

.slot-select select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
}

.checkout-btn {
  width: 100%;
  padding: 14px;
  font-size: 18px;
}
</style>
