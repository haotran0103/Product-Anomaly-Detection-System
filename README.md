## Anomaly Detection App

### 1. Xây dựng mô hình AI

#### Mục tiêu
Dự án nhằm phát triển một hệ thống phát hiện khuyết tật hoặc bất thường trên các sản phẩm trong dây chuyền sản xuất. Hệ thống sẽ tự động phát hiện các lỗi như vết xước, lỗ hổng, hoặc các điểm không đạt chuẩn trên bề mặt sản phẩm. Điều này giúp giảm thiểu lỗi sản xuất và cải thiện hiệu quả kiểm soát chất lượng.

#### Dữ liệu
Dữ liệu sử dụng cho dự án được lấy từ bộ dữ liệu [MVTec Anomaly Detection Dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad), bao gồm các hình ảnh của sản phẩm "good" (không bị lỗi) và các hình ảnh "anomaly" (bị lỗi) cùng với các mặt nạ (mask) cho biết vị trí khuyết tật trên sản phẩm. Cấu trúc thư mục như sau:
- `train/good`: Hình ảnh sản phẩm không có lỗi.
- `test/anomaly_type`: Hình ảnh sản phẩm có lỗi, chia theo các loại khuyết tật.
- `ground_truth/anomaly_type`: Các mặt nạ tương ứng với hình ảnh lỗi, cho biết vùng bị lỗi.

#### Tiền xử lý dữ liệu
- Dữ liệu được tiền xử lý bằng cách đọc ảnh từ các thư mục và ghép nối ảnh lỗi với ảnh mặt nạ tương ứng.
- Ảnh được resize về kích thước (256x256) và chuẩn hóa về dải giá trị từ 0 đến 1.

#### Kiến trúc mô hình
Mô hình sử dụng là `DeepLabV3+`, một kiến trúc phân đoạn ảnh mạnh mẽ được tối ưu hóa cho việc phân loại và xác định vị trí của các khuyết tật. Trong dự án này, mô hình được fine-tune lại từ các trọng số tiền huấn luyện trên tập dữ liệu `ImageNet`.

#### Huấn luyện mô hình
- Sử dụng `SparseCategoricalCrossentropy` làm hàm loss và `Adam` làm thuật toán tối ưu.
- Mô hình được huấn luyện trong 35 epoch với learning rate ban đầu là 1e-4.
- Sử dụng kỹ thuật augmentation để tăng cường dữ liệu và cải thiện khả năng tổng quát của mô hình.
- Mô hình đạt độ chính xác khoảng 85% trên tập kiểm tra.

### 2. Phát triển ứng dụng web

#### Công nghệ sử dụng
Ứng dụng web được phát triển bằng `FastAPI` cho phần backend và sử dụng `HTML`, `CSS`, và `JavaScript` cho phần frontend.
- **Backend**: Xử lý các yêu cầu từ client, thực hiện dự đoán bằng mô hình và trả về kết quả.
- **Frontend**: Cho phép người dùng tải lên một hoặc nhiều hình ảnh để thực hiện dự đoán và hiển thị kết quả.

#### API backend
- **/predict/**: Dự đoán cho một hình ảnh. Trả về kết quả có bất thường hay không và hình ảnh chồng với mặt nạ.
- **/predict_multiple/**: Dự đoán cho nhiều hình ảnh. Trả về danh sách kết quả cho từng hình ảnh.

#### Giao diện người dùng
- Giao diện bao gồm hai chức năng chính: dự đoán cho một ảnh và dự đoán cho nhiều ảnh.
- Ảnh kết quả sẽ hiển thị với các vùng phát hiện bất thường được tô màu đỏ.

#### Triển khai ứng dụng
- Ứng dụng được triển khai trên máy chủ cục bộ (`localhost:8000`).

### Hướng dẫn cài đặt và chạy thử

1. **Cài đặt môi trường**
   - Tạo môi trường ảo và cài đặt các thư viện cần thiết từ `requirements.txt`.

2. **Chạy ứng dụng**
   - Chạy lệnh `uvicorn main:app --reload` để khởi động server.
   - Mở trình duyệt và truy cập `http://localhost:8000` để sử dụng ứng dụng.
