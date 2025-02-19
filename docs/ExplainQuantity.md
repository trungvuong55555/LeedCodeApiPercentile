### 📌 **Phân tích kỹ yêu cầu bài toán**  

Bài toán yêu cầu xây dựng một REST API với hai endpoint chính:  

1. **POST /append_pool**  
   - Nhận dữ liệu gồm `poolId` (số nguyên) và `poolValues` (mảng số).  
   - Nếu `poolId` đã tồn tại, ta **thêm giá trị** vào pool hiện có.  
   - Nếu `poolId` chưa tồn tại, ta **tạo pool mới** và lưu giá trị vào.  
   - Kết quả trả về:  
     - `"inserted"` nếu là pool mới.  
     - `"appended"` nếu đã cập nhật pool hiện có.  

2. **POST /query_pool**  
   - Nhận `poolId` (số nguyên) và `percentile` (giá trị phần trăm).  
   - Trả về **quantile** (phân vị) của tập dữ liệu trong pool.  
   - Nếu không có pool tương ứng, báo lỗi **404**.  
   - Nếu pool rỗng, báo lỗi **400**.  
   - Kết quả trả về:  
     - Giá trị **quantile** được tính toán.  
     - Số lượng phần tử trong pool.  

---

### 🔗 **Phân tích bài toán tính toán quantile**  

#### 😓 **Quantile (Phân vị) là gì?**  
Quantile là một cách chia tập dữ liệu thành các phần có kích thước bằng nhau. Khi ta nói **percentile**, ta đang đề cập đến giá trị ở vị trí phần trăm cụ thể trong tập dữ liệu đã sắp xếp.  

Ví dụ, **90th percentile** có nghĩa là:  
> 90% các phần tử trong tập dữ liệu có giá trị **nhỏ hơn hoặc bằng** giá trị này.  

---

#### 🧩 **Cách tính percentile (quantile)**  

##### 📌 **Bước 1: Sắp xếp tập dữ liệu theo thứ tự tăng dần**  
Giả sử ta có tập dữ liệu:  
```
D = [10, 20, 30, 40, 50]
```

##### 📌 **Bước 2: Xác định chỉ số cần lấy**  
Giả sử ta cần tìm **80th percentile** (p = 80):  
```
index = (p / 100) * (N - 1)
       = (80 / 100) * (5 - 1)
       = 3.2
```
Vậy, vị trí cần lấy là **index = 3.2**.

##### 📌 **Bước 3: Tìm giá trị tại chỉ số đó**  
- Chỉ số `3.2` nằm giữa phần tử **index = 3 (40)** và **index = 4 (50)**.  
- Ta dùng nội suy tuyến tính để tính toán:  
```
value = (1 - weight) * D[lower] + weight * D[upper]
      = (1 - 0.2) * 40 + 0.2 * 50
      = 0.8 * 40 + 0.2 * 50
      = 32 + 10
      = 42
```
Vậy **80th percentile** của tập dữ liệu `[10, 20, 30, 40, 50]` là **42**.  

---

### 🛠️ **Tổng kết thuật toán tính quantile**  
1. **Sắp xếp** tập dữ liệu.  
2. **Tính chỉ số index** = `(percentile / 100) * (N - 1)`.  
3. Nếu index là số nguyên, lấy phần tử tại vị trí 

