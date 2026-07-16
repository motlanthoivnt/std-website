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

## Chỉnh sửa nội dung qua CMS (khuyên dùng — không cần biết code)

Toàn bộ nội dung (chữ, ảnh, ngày tháng) đã được tách ra thư mục `content/*.yaml`, KHÔNG còn nằm hardcode trong file HTML. Có 2 cách sửa:

**A. Qua trang quản trị Pages CMS (dành cho admin không rành kỹ thuật)**
1. Chủ repo cài GitHub App tại https://pagescms.org/docs/guides/installing/github-app/ cho repo này (làm 1 lần).
2. Vào https://app.pagescms.org, đăng nhập GitHub, chọn repo `std-website` — thấy danh sách các trang bằng tiếng Việt (Trang chủ, Nhãn hiệu, Tin tức...).
3. Sửa xong bấm **Save** — Pages CMS tự commit vào `content/*.yaml`.
4. GitHub Action `.github/workflows/build-content.yml` tự chạy `tools/build.py` để dựng lại HTML và đẩy lên — web cập nhật sau khoảng 1 phút.
5. Muốn mời thêm người sửa (không cần họ có tài khoản GitHub): trong Pages CMS chọn **Collaborators → Invite**, họ nhận email và đăng nhập trực tiếp — chỉ có quyền sửa nội dung/ảnh, không đụng được vào code hay cấu hình.

**B. Sửa thủ công (dành cho dev)**
1. Sửa file trong `content/` (đúng đường dẫn/khoá đã khai báo trong `.pages.yml`).
2. Chạy `pip install -r tools/requirements.txt` rồi `python tools/build.py` để dựng lại 17 file HTML.
3. Commit & push — hoặc để nguyên và push thẳng `content/`, GitHub Action sẽ tự build giúp.

> Muốn đổi khung giao diện/thêm trang mới thì sửa `tools/build.py` (cấu trúc) hoặc `assets/css/style.css` (giao diện) — hai việc này vẫn cần code, không làm qua CMS được.

## Ghi chú quan trọng

1. **Nội dung Lorem ipsum**: bản gốc năm 2022 nhiều chỗ vẫn để chữ giả (lorem ipsum) và tin tức mẫu — bản dựng lại giữ **nguyên văn** để "y hệt". Sửa trực tiếp trong `content/*.yaml` (hoặc qua CMS) rồi build lại.
2. **Lỗi chính tả của bản gốc được giữ nguyên** (vd "Các nhẫn hiệu", "khác hàng", "INTERNATIONNAL", "nhưng phương thức"…) — trừ 1 chỗ đã chuẩn hoá: tên công ty ở trang Liên hệ trước đây gõ "STD **I**nternational" (viết hoa I) lệch với 17 chỗ còn lại đều viết "STD **i**nternational" (viết thường), nay dùng chung 1 nguồn `content/site.yaml` nên đồng nhất viết thường như đa số.
3. **Form liên hệ**: web tĩnh không tự gửi mail được. Hiện form mở trình gửi mail của khách với nội dung điền sẵn (mailto tới info@stdpharma.vn). Muốn gửi thẳng từ web: dùng Formspree/Getform (miễn phí, chỉ cần đổi 1 dòng `<form action=...>`), hoặc backend riêng.
4. **Nút EN | VN**: bản chụp gốc chỉ có tiếng Việt nên bản EN chưa tồn tại; nút hiện là trang trí.
5. **Bản đồ trang Liên hệ**: đang dùng ảnh bản đồ tĩnh trích từ bản gốc. Muốn bản đồ tương tác thì nhúng iframe Google Maps thay thẻ `<img>`.
6. **Font**: Oswald (Google Fonts, có tiếng Việt) — cần internet lần đầu tải font; có fallback Arial Narrow khi offline.
7. `?shot` trên URL là chế độ phục vụ chụp màn hình so khớp (cố định chiều cao hero, tắt animation) — không ảnh hưởng người dùng.
