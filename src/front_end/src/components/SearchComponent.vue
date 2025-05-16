<template>
  <div class="search-container">
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Tìm kiếm sản phẩm trên Chợ Tốt"
      class="search-input"
      @keyup.enter="performSearch"
    />
    <button @click="performSearch" class="search-button">
      <svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 -960 960 960" width="20"><path d="M784-120 532-372q-36 29-78 49t-85 20q-105 0-183.5-78.5T120-580q0-105 78.5-183.5T382-842q105 0 183.5 78.5T644-580q0 42-20 85t-49 78l252 252-56 56ZM382-440q75 0 127.5-52.5T562-620q0-75-52.5-127.5T382-800q-75 0-127.5 52.5T202-620q0 75 52.5 127.5T382-440Z"/></svg>
      Tìm kiếm
    </button>
  </div>
</template>

<script>
export default {
  name: 'SearchComponent',
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    performSearch() {
      // Phát ra sự kiện 'search' và gửi giá trị searchQuery lên component cha
      this.$emit('search', this.searchQuery);
      console.log('Tìm kiếm với từ khóa:', this.searchQuery);
    }
  }
};
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #ffefc0; /* Màu vàng nhạt tương tự Chợ Tốt */
  border-radius: 4px;
}

.search-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #ffb300; /* Màu cam đậm hơn khi focus */
  box-shadow: 0 0 5px rgba(255, 179, 0, 0.5);
}

.search-button {
  background-color: #ffb300; /* Màu cam tương tự Chợ Tốt */
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

.search-button:hover {
  background-color: #ff9800; /* Màu cam đậm hơn khi hover */
}

.search-button svg {
    fill: white; /* Màu icon */
}
</style>