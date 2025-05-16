<script>
import axios from "axios";
export default {
  name: "Home",
  data() {
    return {
      products: [],
      page: 1,
      pageSize: 10,
      categories: [
        { id: 1, name: "Tất cả" },
        { id: 2, name: "Gà" },
        { id: 3, name: "Chó" },
        { id: 4, name: "Chim" },
        { id: 5, name: "Mèo" },
        { id: 6, name: "Thú cưng khác" },
        { id: 7, name: "Phụ kiện, Thức ăn, Dịch vụ" },
      ],
      searchQuery: "",
      categoryValue: "Tất cả",
      selectedCategory: 1,
    };
  },
  methods: {
    selectedCategoryMethod(id) {
      this.selectedCategory = id;
      this.categoryValue = this.categories.find(
        (category) => category.id === id
      ).name;
      console.log("Selected category:", this.categoryValue);
      this.fetchData();
    },
    search() {
      this.fetchData();
    },
    next() {
      this.page++;
      this.fetchData();
    },
    prev() {
        this.page--;
        this.fetchData();
    },
    fetchData() {
      const params = new URLSearchParams({
        page: this.page,
        size: this.pageSize,
      });

      if (this.selectedCategory !== 1) {
        params.append("filter", this.categoryValue);
      }

      if (this.searchQuery.trim() !== "") {
        params.append("search", this.searchQuery.trim());
      }

      const url = `${import.meta.env.VITE_API_URL}/pet?${params.toString()}`;
      console.log("URL gọi API:", url);

      axios
        .get(url)
        .then((res) => {
          this.products = res.data.data;
          console.log("Dữ liệu sản phẩm:", res);
        })
        .catch((err) => {
          console.error("Lỗi khi fetch:", err);
        });
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<template>
  <div class="container-fluid bg-warning">
    <div class="row justify-content-center py-3">
      <header class="app-header px-0 col-10">
        <div class="row g-2 align-items-center">
          <div class="header-left col-md-2 col-sm-12 text-md-start text-center">
            <a
              href="/"
              class="logo-link fs-2 fw-bold text-white text-decoration-none d-block py-2"
            >
              <span class="logo-text">Chợ tốt</span>
            </a>
          </div>
          <div class="header-center col-md-10 col-sm-12">
            <div class="input-group">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Tìm kiếm sản phẩm trên Chợ Tốt"
                class="form-control"
                @keyup.enter="search"
              />
              <button
                @click="search"
                class="btn btn-dark d-flex align-items-center"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="16"
                  viewBox="0 -960 960 960"
                  width="16"
                  fill="#FFFFFF"
                  class="me-2"
                >
                  <path
                    d="M784-120 532-372q-36 29-78 49t-85 20q-105 0-183.5-78.5T120-580q0-105 78.5-183.5T382-842q105 0 183.5 78.5T644-580q0 42-20 85t-49 78l252 252-56 56ZM382-440q75 0 127.5-52.5T562-620q0-75-52.5-127.5T382-800q-75 0-127.5 52.5T202-620q0 75 52.5 127.5T382-440Z"
                  />
                </svg>
                Tìm kiếm
              </button>
            </div>
          </div>
        </div>
      </header>
    </div>
  </div>
  <div class="row bg-light my-2 p-3 px-5">
    <div class="category-menu-container">
      <div class="row justify-content-center align-items-center">
        <div class="col-1">
          <p class="text-muted fw-bold fs-6 m-0">Danh mục:</p>
        </div>
        <div class="col-8">
          <div class="category-list">
            <div
              v-for="category in categories"
              :key="category.id"
              class="category-item btn btn-outline-secondary me-3"
              :class="{ active: this.selectedCategory === category.id }"
              @click="selectedCategoryMethod(category.id)"
            >
              <span>{{ category.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="row justify-content-center">
    <div v-if="products.length === 0">Không tìm thấy sản phẩm nào phù hợp.</div>
    <div
      v-else
      v-for="product in products"
      :key="product.id"
      class="card product-card col-lg-7 p-0"
    >
      <div class="row g-0 justify-content-center align-items-center">
        <div class="col-md-3">
          <img
            :src="product.image_url"
            class="img-cover rounded-start"
            style="width: 200px; height: 200px"
            alt="Product Image"
          />
        </div>
        <div class="col-md-9">
          <div class="product-details d-flex flex-column h-100">
            <div class="flex-grow-1">
              <h5 class="card-title product-title">{{ product.subject }}</h5>
              <p class="card-text product-category">
                {{ product.category_name }} | {{ product.param_value }}
              </p>
              <div class="product-price">{{ product.price_string }}</div>
              <div class="location-info">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-geo-alt-fill"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"
                  />
                </svg>
                {{ product.area_name }}
              </div>
            </div>
            <div
              class="d-flex justify-content-between align-items-center mt-auto"
            >
              <div class="seller-info d-flex align-items-center">
                <span>{{ product.seller_name }}</span>
                <span class="seller-rating ms-2">
                  <span class="star">★</span> {{ product.average_rating }}
                </span>
                <span class="ms-2">{{ product.sold_ads }} đã bán</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row justify-content-end align-items-center m-2">
      <div class="col-4 ">
        <nav aria-label="Page navigation example" >
          <ul class="pagination  prev">
            <li class="page-item" :class="{disabled: page === 1}">
              <a class="page-link" @click="prev" tabindex="-1" >Trước</a>
            </li>
            <li class="page-item active" aria-current="page">
              <a class="page-link" href="#">{{this.page}}</a>
            </li>
            <li class="page-item next">
              <a class="page-link" @click="next">Sau</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}
.prev,
.next {
    outline: none;
    cursor: pointer;
}
.image-count {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8em;
}
.product-details {
  padding: 15px;
}
.product-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 5px;
}
.product-category {
  font-size: 0.9em;
  color: #555;
  margin-bottom: 10px;
}
.product-price {
  font-size: 1.3em;
  color: #dc3545; /* Bootstrap danger color */
  font-weight: bold;
  margin-bottom: 10px;
}
.location-info,
.seller-info {
  font-size: 0.9em;
  color: #555;
  margin-bottom: 5px;
}
.seller-info img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 5px;
}
.seller-rating .star {
  color: #ffc107; /* Bootstrap warning color */
}
.favorite-icon {
  font-size: 1.5em;
  color: #dc3545; /* Bootstrap danger color */
  cursor: pointer;
}
</style>