<template>
  <div class="category-menu-container">
    <h2>Danh mục:</h2>
    <div class="category-list">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-item"
        :class="{ 'is-active': selectedCategory === category.id }"
        @click="selectCategory(category.id)"
      >
        <img v-if="category.icon" :src="category.icon" :alt="category.name" class="category-icon">
        <span>{{ category.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryMenu',
  data() {
    return {
      categories: [
        { id: 1, name: 'Tất cả', icon: null },
        { id: 2, name: 'Gà', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🐔' }, // Placeholder icon
        { id: 3, name: 'Chó', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🐶' }, // Placeholder icon
        { id: 4, name: 'Chim', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🐦' }, // Placeholder icon
        { id: 5, name: 'Mèo', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🐱' }, // Placeholder icon
        { id: 6, name: 'Thú cưng khác', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🐾' }, // Placeholder icon
        { id: 7, name: 'Phụ kiện, Thức ăn...', icon: 'https://via.placeholder.com/30/FFB300/FFFFFF?text=🦴' }, // Placeholder icon
      ],
      selectedCategory: 1 // Mặc định chọn 'Tất cả'
    };
  },
  methods: {
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
      // Phát ra sự kiện 'category-selected' với ID của danh mục
      this.$emit('category-selected', categoryId);
      console.log('Chọn danh mục:', categoryId);
    }
  }
};
</script>

<style scoped>
.category-menu-container {
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.category-menu-container h2 {
    font-size: 1.1rem;
    margin-bottom: 10px;
    color: #333;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* Khoảng cách giữa các danh mục */
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 15px;
  border: 1px solid #eee;
  border-radius: 20px; /* Hình viên thuốc */
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 0.9rem;
  color: #555;
}

.category-item:hover {
  background-color: #f0f0f0;
}

.category-item.is-active {
  background-color: #ffb300; /* Màu cam khi được chọn */
  color: white;
  border-color: #ffb300;
}

.category-item.is-active .category-icon {
    filter: brightness(0) invert(1); /* Đảo màu icon khi active nếu icon là dạng đen trắng */
}

.category-icon {
    width: 30px;
    height: 30px;
    margin-bottom: 5px;
}
</style>