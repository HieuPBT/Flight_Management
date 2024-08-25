<h1>Quản Lý Chuyến Bay<h1>

<p align="center">
     <a href="https://flask.palletsprojects.com/en/3.0.x/">
        <img src="https://img.shields.io/badge/Flask-white.svg?logo=flask&labelColor=black"/>
    </a>
    <a href="https://www.mysql.com/">
        <img src="https://img.shields.io/badge/MySQL-4479A1.svg?logo=mysql&labelColor=white"/>
    </a>
    <a href="https://gunicorn.org/">
        <img src="https://img.shields.io/badge/Gunicorn-499848.svg?logo=gunicorn&labelColor=white"/>
    </a>
    <a href="https://nginx.org/en/">
        <img src="https://img.shields.io/badge/Nginx-009639.svg?logo=nginx&labelColor=green"/>
    </a>
    <a href="https://www.docker.com/">
        <img src="https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&labelColor=white"/>
    </a>

# Tổng quan
Viết báo cáo và phát triển hệ thống quản lý chuyến bay. Báo cáo bao gồm các nội dung
- Lược đồ và đặc tả use case
- Sơ đồ sequence diagram
- Sơ đồ activity diagram
- Sơ đồ lớp -> lược đồ CSDL quan hệ
- Thiết kế giao diện

Truy cập [TẠI ĐÂY](/BaoCaoDeTai5-Nhom6-CNPM.docx) để xem đầy đủ nội dung báo cáo

# Nội dung

- [Chức năng](#chức-năng)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Cơ sở dữ liệu](#cơ-sở-dữ-liệu)
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
- [Giao diện](#giao-diện)
- [Tài liệu](#tài-liệu)

# Chức năng
1. <b>Tra cứu chuyến bay</b>
    - Khách hàng có thể tra cứu theo điểm đi, điểm đến, ngày đi, hạng vé và số lượng vé
2. <b>Đặt vé</b>
    - Khách hàng có thể đặt vé online (bắt buộc thanh toán trực tuyến)

    - Chỉ có thể đặt những vé còn chỗ và cho các chuyến bay trước 12h lúc khởi hàng

![feat1](/images/feat1.png)

3. <b>Lập lịch chuyến bay</b>
    - Cho phép nhân viên lập lịch chuyến bay

![feat2](/images/feat2.png)

4. <b>Thống kê báo cáo</b>
    - Quản trị viên xem thống kê dạng bảng và biểu đồ (sử dụng chartjs)

    - Thống kê doanh thu theo từng tháng và từng tuyến bay

![feat3](/images/feat3.png)

5. <b>Thay đổi quy định</b>
    - Quản trị viên được thay đổi quy định
        * hay đổi số lượng sân bay, thời gian bay tối thiểu, số sân bay trung gian tối đa, thới gian dừng tối thiểu và tối đa tại các sân bay trung gian

        * Thay đối số lượng hạng vé, bảng đơn giá vé

        * Thay đổi thời gian bán vé và đặt vé

    - Quản tri viên quản lý tuyến bay, chuyến bay(thêm/xóa/cập nhật/tìm kiếm)

# Kiến trúc hệ thống

![system](/images/system.svg)

# Cơ sở dữ liệu

![database](/images/database.jpg)

# Hướng dẫn cài đặt
### Yêu cầu
1. [Docker](https://www.docker.com/)

2. 
````bash
# Clone the project
git clone https://github.com/locnguyn/TrainingPointsManagement_SpringMVC_ReactJS
````

### Cài đặt

````bash
cd Flask_Flight_Management

# Build docker 
docker compose build

# Chạy docker
docker compose up -d

# Tắt docker
docker compose down
````

Truy cập `localhost:8200` để sử dụng giao diện người dùng và `localhost:5020` để sử dụng trang admin `username:admin, password:123456`

# Giao diện
### Người dùng
<img src="./images/user1.png" width="40%"></img>
<img src="./images/user2.png" width="40%"></img>

<img src="./images/user3.png" width="40%"></img>
<img src="./images/user4.png" width="40%"></img>
### Quản trị viên
<img src="./images/admin1.png" width="40%"></img>
<img src="./images/admin2.png" width="40%"></img>

<img src="./images/admin3.png" width="40%"></img>
<img src="./images/admin4.png" width="40%"></img>

# Tài liệu
* 🔗 [FLask](https://flask.palletsprojects.com/en/3.0.x/)

* 🔗 [Gunicorn](https://gunicorn.org/)

* 🔗 [Nginx](https://nginx.org/en/)

* 🔗 [MySQL](https://www.mysql.com/)


* 🔗 [Docker](https://www.docker.com/)