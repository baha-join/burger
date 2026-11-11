<template>
  <div>
    <h2 class="page-title">Меню на сегодня</h2>
    
    <!-- Фильтр по категориям -->
    <div class="categories" v-if="categories.length > 0">
      <button :class="{ active: selectedCategory === null }" @click="selectedCategory = null">Все</button>
      <button v-for="cat in categories" :key="cat.id" 
              :class="{ active: selectedCategory === cat.id }" 
              @click="selectedCategory = cat.id">
        {{ cat.name }}
      </button>
    </div>

    <div v-if="filteredItems.length === 0" class="empty-state">Нет доступных блюд 😔</div>

    <div class="menu-grid">
      <div v-for="item in filteredItems" :key="item.id" class="dish-card">
        <div class="dish-image">
          <img v-if="item.image" :src="item.image" alt="Фото" />
          <div v-else class="no-image">Нет фото</div>
        </div>
        <div class="dish-info">
          <div class="dish-header">
            <h3 class="dish-name">{{ item.name }}</h3>
            <span class="dish-cat">{{ item.category.name }}</span>
          </div>
          <p class="dish-desc">{{ item.description }}</p>
          
          <div class="dish-macros" v-if="item.calories">
            <span>{{ item.weight_g }} г</span> |
            <span>{{ item.calories }} ккал</span> |
            <span>Б: {{ item.proteins }} Ж: {{ item.fats }} У: {{ item.carbs }}</span>
          </div>

          <div class="dish-bottom">
            <span class="dish-price">{{ item.price }} ₽</span>
            <button @click="addToCart(item.id)" class="add-btn">В корзину</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const items = ref([])
const selectedCategory = ref(null)

onMounted(async () => {
  const res = await api.get('/menu/')
  items.value = res.data.items
})

// Собираем уникальные категории из блюд
const categories = computed(() => {
  const cats = {}
  items.value.forEach(item => { cats[item.category.id] = item.category })
  return Object.values(cats)
})

const filteredItems = computed(() => {
  if (!selectedCategory.value) return items.value
  return items.value.filter(i => i.category.id === selectedCategory.value)
})

const addToCart = async (id) => {
  await api.post('/cart/add/', { item_id: id })
  alert('Добавлено!')
}
</script>

<style scoped>
.page-title { margin-bottom: 20px; color: #333; }
.categories { display: flex; gap: 10px; margin-bottom: 25px; flex-wrap: wrap; }
.categories button { background: #fff; color: #333; border: 1px solid #ddd; }
.categories button.active { background: #ff7f50; color: white; border-color: #ff7f50; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }
.dish-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: 0.2s; display: flex; flex-direction: column; }
.dish-card:hover { transform: translateY(-5px); }
.dish-image img { width: 100%; height: 180px; object-fit: cover; }
.no-image { height: 180px; background: #e9ecef; display: flex; align-items: center; justify-content: center; color: #888; }
.dish-info { padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }
.dish-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.dish-name { font-size: 20px; margin: 0; }
.dish-cat { font-size: 12px; background: #f0f0f0; padding: 2px 8px; border-radius: 10px; color: #666; }
.dish-desc { color: #666; font-size: 14px; margin-bottom: 10px; }
.dish-macros { font-size: 12px; color: #888; margin-bottom: 15px; background: #f9f9f9; padding: 5px; border-radius: 5px; }
.dish-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }
.dish-price { font-size: 22px; font-weight: bold; color: #ff7f50; }
.add-btn { padding: 8px 15px; font-size: 14px; }
</style>
