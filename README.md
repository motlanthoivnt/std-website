# Website STD International Co.,LTD (stdpharma.vn)

Website tĩnh được dựng lại **y hệt** từ bản chụp website cũ (file `STD international Website.pdf`, 18 trang, 2022).
Toàn bộ ảnh (hero, sản phẩm, tin tức, logo, bản đồ, huy hiệu Bộ Công Thương) được trích xuất từ chính file PDF gốc.

## Cấu trúc

```
website/
├── index.html                  Trang chủ
├── gioi-thieu.html             Giới thiệu về STD Quốc tế
│   ├── doi-ngu-nhan-su.html
│   ├── tam-nhin-su-menh.html
│   ├── doi-voi-khach-hang.html
│   ├── co-so-san-xuat.html
│   └── nghien-cuu-phat-trien.html
├── nhan-hieu-v2joy.html        Nhãn hiệu V2JOY
├── nhan-hieu-vready.html       Nhãn hiệu VREADY
├── nhan-hieu-otv.html          Nhãn hiệu OTVhitech
├── phat-trien-ben-vung.html    Phát triển bền vững
│   ├── van-hoa-doanh-nghiep.html
│   ├── chien-luoc-con-nguoi.html
│   └── moi-truong-cong-dong.html
├── tin-tuc.html                Tin tức & truyền thông
├── tuyen-dung.html             Tuyển dụng
├── lien-he.html                Liên hệ
└── assets/
    ├── css/style.css           Toàn bộ giao diện
    ├── js/main.js              Menu, slider, hiệu ứng, form
    └── img/                    Ảnh đã tối ưu cho web
```

## Xem thử trên máy

Mở thẳng `index.html` bằng trình duyệt, hoặc chạy server:

```
python -m http.server 8080
# rồi mở http://localhost:8080
```

## Đưa lên web (deploy)

Website là **HTML tĩnh thuần** — không cần database, không cần PHP/Node:

- **Hosting cPanel / hosting VN**: upload toàn bộ **nội dung bên trong** thư mục `website/` vào `public_html/` (giữ nguyên thư mục `assets/`). Xong.
- **Netlify / Vercel / Cloudflare Pages**: kéo-thả thư mục `website/` là chạy.
- **GitHub Pages**: push thư mục này lên repo, bật Pages.

Sau đó trỏ tên miền (vd `stdpharma.vn`) về hosting là hoàn tất.

## Ghi chú quan trọng

1. **Nội dung Lorem ipsum**: bản gốc năm 2022 nhiều chỗ vẫn để chữ giả (lorem ipsum) và tin tức mẫu — bản dựng lại giữ **nguyên văn** để "y hệt". Khi có nội dung thật chỉ cần thay text trong file HTML tương ứng.
2. **Lỗi chính tả của bản gốc được giữ nguyên** (vd "Các nhẫn hiệu", "khác hàng", "INTERNATIONNAL", "nhưng phương thức"…). Muốn sửa thì tìm-thay trong các file HTML.
3. **Form liên hệ**: web tĩnh không tự gửi mail được. Hiện form mở trình gửi mail của khách với nội dung điền sẵn (mailto tới info@stdpharma.vn). Muốn gửi thẳng từ web: dùng Formspree/Getform (miễn phí, chỉ cần đổi 1 dòng `<form action=...>`), hoặc backend riêng.
4. **Nút EN | VN**: bản chụp gốc chỉ có tiếng Việt nên bản EN chưa tồn tại; nút hiện là trang trí.
5. **Bản đồ trang Liên hệ**: đang dùng ảnh bản đồ tĩnh trích từ bản gốc. Muốn bản đồ tương tác thì nhúng iframe Google Maps thay thẻ `<img>`.
6. **Font**: Oswald (Google Fonts, có tiếng Việt) — cần internet lần đầu tải font; có fallback Arial Narrow khi offline.
7. `?shot` trên URL là chế độ phục vụ chụp màn hình so khớp (cố định chiều cao hero, tắt animation) — không ảnh hưởng người dùng.
