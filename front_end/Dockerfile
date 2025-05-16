# Stage 1: Build the Vue.js application with Vite
FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package.json package-lock.json ./
# Cài đặt dependencies. Vite dùng npm install như bình thường.
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the application using 'serve' (Node.js based)
FROM node:18-alpine AS run-stage 

# Cài đặt gói 'serve' global
RUN npm install -g serve

# Đặt thư mục làm việc trong stage chạy
WORKDIR /app

# Copy các file build đã được tạo bởi Vite ở build-stage
# /app/dist từ build-stage sẽ được copy vào thư mục /app/dist trong run-stage
COPY --from=build-stage /app/dist /app/dist

# Cổng mặc định mà 'serve' sử dụng là 3000
EXPOSE 3000

# Command mặc định để chạy 'serve'.
# '-s' flag là để bật chế độ SPA fallback, quan trọng cho Vue Router history mode.
# '/app/dist' là thư mục chứa các file tĩnh (output của Vite build)
CMD ["serve", "-s", "/app/dist"]