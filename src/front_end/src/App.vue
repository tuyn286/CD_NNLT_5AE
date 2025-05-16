<script>
</script>

<template>

  <RouterView />
  <footer className="footer">
    <div className="footer-container">
      <div className="footer-section">
        <h3>PetMarket</h3>
        <p>Nền tảng mua bán thú cưng nhanh chóng, uy tín và tiện lợi.</p>
      </div>
      <div className="footer-section">
        <h4>Về chúng tôi</h4>
        <ul>
          <li><a href="#">Giới thiệu</a></li>
          <li><a href="#">Liên hệ</a></li>
          <li><a href="#">Điều khoản</a></li>
          <li><a href="#">Chính sách bảo mật</a></li>
        </ul>
      </div>
      <div className="footer-section">
        <h4>Danh mục</h4>
        <ul>
          <li><a href="#">Chó cảnh</a></li>
          <li><a href="#">Mèo cảnh</a></li>
          <li><a href="#">Chim cảnh</a></li>
          <li><a href="#">Thú cưng khác</a></li>
        </ul>
      </div>
    </div>
    <div className="footer-bottom">
      <p>&copy; 2025 PetMarket. All rights reserved.</p>
    </div>
  </footer>
</template>
<style scoped>
.footer {
    background-color: #f5f5f5;
    padding: 40px 0 20px;
    font-family: Arial, sans-serif;
    color: #333;
    border-top: 1px solid #e0e0e0;
}

.footer-container {
    max-width: 1200px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 40px;
    padding: 0 20px;
}

.footer-section {
    flex: 1;
    min-width: 200px;
}

.footer-section h3 {
    margin-bottom: 12px;
    font-size: 20px;
    color: #ff6600;
}

.footer-section h4 {
    margin-bottom: 10px;
    font-size: 16px;
    color: #444;
}

.footer-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-section ul li {
    margin-bottom: 8px;
}

.footer-section ul li a {
    text-decoration: none;
    color: #333;
    transition: color 0.2s;
}

.footer-section ul li a:hover {
    color: #ff6600;
}

.footer-bottom {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid #ddd;
    font-size: 14px;
    color: #777;
}


/* Style cho SearchComponent bên trong Header */
/* Bạn có thể cần điều chỉnh style của SearchComponent để phù hợp khi nằm trong header */
/* Ví dụ: bỏ padding hoặc margin của search-container trong SearchComponent */

</style>
