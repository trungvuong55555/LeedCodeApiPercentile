# Tối ưu Concurrency và Memory Footprint

## 1. Tối ưu Concurency và Memory

### Phân tích Yêu cầu
1. **Không có cơ sở dữ liệu** → Dữ liệu được lưu trong RAM, do đó quản lý bộ nhớ là quan trọng.
2. **Không giới hạn số lượng yêu cầu đồng thời** → Có nguy cơ xảy ra tình trạng race condition.
3. **Không có yêu cầu nghiêm ngặt về hiệu suất cao hoặc xử lý dữ liệu lớn** → Cần tối ưu hợp lý.
4. **Không có yêu cầu mở rộng rõ ràng** → Chưa cần đa luồng hoặc nhiều worker trừ khi thực sự cần thiết.

### Kết luận:
- **Cần tối ưu về tính đồng thời** để tránh lỗi race condition.
- **Không cần tối ưu bộ nhớ quá mức** trừ khi phải xử lý số lượng pool cực lớn.

---

## 2. Chiến lược tối ưu phù hợp nhất

### **1️⃣ Sử dụng `threading.Lock` để xử lý đồng thời**
Vì tất cả yêu cầu đều cập nhật vào một dictionary chung (`pools`), nhiều luồng ghi cùng lúc có thể gây lỗi race condition.

#### **Giải pháp:**
- Dùng **dictionary chứa `threading.Lock` cho từng `poolId`** để tránh khóa toàn bộ hệ thống.
- Chỉ khóa pool cần thiết khi cập nhật dữ liệu.

#### **Triển khai:**
```python
import threading

pools = {}  # Lưu trữ dữ liệu
locks = {}  # Lưu trữ khóa cho từng poolId

def get_lock(pool_id):
    if pool_id not in locks:
        locks[pool_id] = threading.Lock()
    return locks[pool_id]

def add_values(pool_id, values):
    lock = get_lock(pool_id)
    with lock:
        if pool_id in pools:
            pools[pool_id].extend(values)
        else:
            pools[pool_id] = values
```

#### **Lợi ích:**
✔️ Đảm bảo an toàn dữ liệu khi nhiều luồng ghi đồng thời.  
✔️ Không làm chậm toàn bộ hệ thống do khóa toàn cục.

---

### **2️⃣ Giới hạn Sử dụng Bộ nhớ với `OrderedDict`**
Nếu số lượng pool quá lớn (hàng triệu pool), RAM có thể bị quá tải.

#### **Giải pháp:**
- Sử dụng `OrderedDict` để **giới hạn số lượng pool lưu trữ** (ví dụ: chỉ giữ lại 1000 pool gần nhất).

#### **Triển khai:**
```python
from collections import OrderedDict

class PoolStorage:
    def __init__(self, max_size=1000):
        self.pools = OrderedDict()
        self.max_size = max_size

    def add_values(self, pool_id, values):
        if pool_id in self.pools:
            self.pools.move_to_end(pool_id)  # Cập nhật thứ tự truy cập
            self.pools[pool_id].extend(values)
        else:
            if len(self.pools) >= self.max_size:
                self.pools.popitem(last=False)  # Xóa pool lâu không sử dụng
            self.pools[pool_id] = values
```

#### **Lợi ích:**
✔️ Giữ RAM ổn định, tránh sử dụng bộ nhớ quá mức.  
✔️ Duy trì hiệu suất tối ưu bằng cách giữ lại các pool quan trọng.



