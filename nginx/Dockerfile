FROM nginx:stable

# Xóa cấu hình mặc định
RUN rm /etc/nginx/conf.d/default.conf

# Sao chép cấu hình tùy chỉnh
COPY conf.d/default.conf /etc/nginx/conf.d/

# Tạo thư mục logs nếu chưa tồn tại
RUN mkdir -p /var/log/nginx

# Expose ports
EXPOSE 80 443

# Khởi động NGINX
CMD ["nginx", "-g", "daemon off;"]