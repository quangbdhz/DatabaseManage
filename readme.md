# Xây dựng ứng dụng trên AWS cho phép tạo Database và cung cấp API để thêm,xóa sửa trên Database 

#### Đây là source code project cuối kỳ môn Cloud Computing của nhóm 14

## Các tính năng chính

- Đăng ký tài khoản để sử dụng các dịch vụ của Website
- Thêm, xóa, sửa Database của MySQL
- Thêm, xóa, sửa Table trong Database
- Thêm, xóa, sửa dữ liệu trong Table

## Công nghệ sử dụng

##### Front End: HTML, CSS3, BOOTSTRAP 4, JavaScript

##### Back End: Flask Framework, AWS Lambda, AWS SQS, AWS EC2

##### Database: AWS RDS (MySQL)

## Thành viên của nhóm

- 19110470	Nguyễn Công Tiến
- 19110443  Trần Quang
- 19110501  Võ Thành Vinh

## Chạy trên Localhost

Clone project từ github

```bash
  git clone https://github.com/quangbdhz/DatabaseManage.git
```

Truy cập thư mục chứa project

```bash
  cd DatabaseManage
```

Tạo môi trường ảo

```bash
  virtualenv venv
```

Kích hoạt môi trường ảo

```bash
  .\venv\Scripts\activate
```

Cài đặt các thư viện 

```bash
  pip install -r requirements.txt
```

Chạy file models

```bash
  python 3
```

```bash
  from my_app import db
```

```bash
  from my_app.models import *
```

```bash
  db.create_all()
```

Chạy file run.py

```bash
  python3 run.py
```

## Deploy lên AWS EC2

Để deploy project, thực hiện các lệnh sau

```bash
  sudo apt-get update
```

clone project về máy ảo

```bash
  git clone https://github.com/quangbdhz/DatabaseManage.git
```

Update các library cần thiết

```bash
  pip3 install --upgrade pip
```

```bash
  python3 -m pip install setuptools-rust
```

Truy cập vào thư mục chứa project

```bash
 cd DatabaseManage
```

Install các thư viện mà project yêu cầu

```bash
  python3 -m pip install -r requirements.txt
```

Chạy file models

```bash
  python 3
```

```bash
  from my_app import db
```

```bash
  from my_app.models import *
```

```bash
  db.create_all()
```

Truy cập file run.py

```bash
  vi run.py
```

Thay đổi từ 

```python3
  from my_app import app
  app.run(debug=True)
```

sang cấu hình phù hợp với máy ảo EC2

```python3
  from my_app import app
  app.run(host='0.0.0.0', port=8080)
```

Sau khi thực hiện các cấu hình cần thiết, để chạy chương trình thực hiện lệnh

```bash
  python3 run.py
```

