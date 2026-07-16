# -*- coding: utf-8 -*-
"""Build the STD International static site from content/*.yaml.

Run from anywhere: python tools/build.py
Writes the *.html files into the repo root (next to this tools/ folder).
"""
import os
import re
import html
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content')


def load(rel_path):
    with open(os.path.join(CONTENT, rel_path), encoding='utf-8') as f:
        return yaml.safe_load(f)


SITE = load('site.yaml')

# ----------------------------------------------------------------- helpers
def esc(s):
    return html.escape(str(s), quote=True)


def br_join(text, para=False):
    """Join lines/paragraphs with a single <br>, escaping each piece."""
    text = str(text).strip()
    if para:
        parts = [p.strip().replace('\n', ' ') for p in re.split(r'\n\s*\n', text)]
    else:
        parts = text.split('\n')
    return '<br>'.join(esc(p) for p in parts)


def article_paragraphs(text):
    """Blank-line separated paragraphs, each wrapped in its own <p>."""
    parts = re.split(r'\n\s*\n', str(text).strip())
    return ''.join(f'<p>{esc(p.strip())}</p>' for p in parts if p.strip())


def img_url(v):
    v = str(v).strip()
    if v.startswith('http') or v.startswith('/'):
        return v.lstrip('/')
    if v.startswith('assets/'):
        return v
    return 'assets/img/' + v


def fmt_date(d):
    return f'{d.day}/{d.month}/{d.year}'


# ----------------------------------------------------------------- svg bits
SVG_SEARCH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">'
'<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.5" y1="15.5" x2="21" y2="21"/></svg>')

SVG_HOME = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3 2.5 11h2.7v9h5.3v-6h3v6h5.3v-9h2.7z"/></svg>')

SVG_FB = ('<svg viewBox="0 0 24 24" aria-label="Facebook"><circle cx="12" cy="12" r="11" fill="#fff"/>'
'<path d="M13.4 20v-6.5h2.2l.33-2.6H13.4v-1.6c0-.74.2-1.24 1.26-1.24h1.35V5.77c-.23-.03-1.03-.1-1.96-.1-1.94 0-3.27 1.18-3.27 3.36v1.87H8.6v2.6h2.18V20z" fill="#FF6700"/></svg>')

SVG_ZALO = ('<svg viewBox="0 0 46 20" aria-label="Zalo"><rect x="0" y="0" width="46" height="20" rx="10" fill="#fff"/>'
'<text x="23" y="14" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#FF6700">Zalo</text></svg>')

DIAGRAM = '''<svg class="tri-diagram" viewBox="0 0 1520 1020" role="img" aria-label="Sơ đồ phát triển bền vững STD">
  <path class="tri" d="M248 156 H537 L392 346 Z"/>
  <path class="tri" d="M748 78 L1054 462 H442 Z"/>
  <path class="tri" d="M958 156 H1247 L1102 346 Z"/>
  <path class="tri" d="M390 512 L700 903 H80 Z"/>
  <path class="tri" d="M1108 512 L1418 903 H798 Z"/>
  <g>
    <text x="392" y="212" text-anchor="middle" font-size="26">From the People</text>
    <text x="392" y="248" text-anchor="middle" font-size="26">of Vietnam</text>
    <text x="1102" y="212" text-anchor="middle" font-size="26">Together with</text>
    <text x="1102" y="248" text-anchor="middle" font-size="26">Community</text>
    <text x="748" y="430" text-anchor="middle" font-size="30">Love Our Products</text>
    <text x="390" y="868" text-anchor="middle" font-size="30">Life Enhancement</text>
    <text x="1108" y="868" text-anchor="middle" font-size="30">Save The Planet</text>
  </g>
  <g class="ic" transform="translate(748 290)">
    <path d="M-52 -28 L0 -52 L52 -28 L52 26 L0 50 L-52 26 Z"/>
    <path d="M-52 -28 L0 -6 L52 -28 M0 -6 L0 50"/>
    <path d="M18 16 l12 12 22 -26" stroke-width="9"/>
  </g>
  <g class="ic-fill" transform="translate(390 740)">
    <path d="M-46 -62 h24 v20 l12 -3 -24 30 -24 -30 12 3 Z" transform="scale(.9)"/>
    <path d="M22 -62 h24 v20 l12 -3 -24 30 -24 -30 12 3 Z" transform="scale(.9)"/>
    <circle cx="-38" cy="18" r="13"/><path d="M-58 58 c0 -16 9 -26 20 -26 s20 10 20 26 Z"/>
    <circle cx="0" cy="8" r="15"/><path d="M-23 58 c0 -19 10 -30 23 -30 s23 11 23 30 Z"/>
    <circle cx="38" cy="18" r="13"/><path d="M18 58 c0 -16 9 -26 20 -26 s20 10 20 26 Z"/>
  </g>
  <g transform="translate(1108 712)">
    <circle class="ic" cx="0" cy="0" r="62" stroke-width="9"/>
    <path class="ic-fill" d="M-34 -46 c14 -8 30 -10 44 -5 l-6 14 8 12 -12 4 -4 12 -14 -4 -8 -14 6 -10 -14 -9 Z"/>
    <path class="ic-fill" d="M18 8 l22 6 4 12 -10 16 -14 2 -6 -14 4 -22 Z"/>
    <path class="ic-fill" d="M-56 -8 l12 10 -2 14 -12 -6 Z"/>
  </g>
  <image href="assets/img/logo-std.png" x="565" y="545" width="366" height="128"/>
</svg>'''

MOUSE = '<span class="mouse" aria-hidden="true"></span>'

# ----------------------------------------------------------------- partials
def head(title, desc):
    return f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {esc(SITE['company_name'])}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" type="image/png" href="assets/img/logo-std.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>'''


def sidebar():
    return f'''
<aside class="sidebar">
  <a href="index.html" aria-label="STD international - Trang chủ"><img class="sidebar__logo" src="assets/img/logo-std.png" alt="STD"></a>
  <div class="sidebar__vertical">STD INTERNATIONAL CO.,LTD</div>
  <button class="sidebar__burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <div class="sidebar__bottom">
    <button class="sidebar__search" aria-label="Tìm kiếm">{SVG_SEARCH}</button>
    <div class="sidebar__lang"><span class="active">EN</span> | <span>VN</span></div>
  </div>
</aside>'''


def menu():
    return '''
<nav class="menu-overlay" aria-label="Menu chính">
  <div class="menu-overlay__inner">
    <ul class="menu-nav">
      <div class="menu-nav__main">
        <li data-nav="home"><a href="index.html">Trang chủ</a></li>
        <li data-nav="about"><a href="gioi-thieu.html">Giới thiệu về STD Quốc tế</a>
          <ul class="menu-nav__sub">
            <li><a href="doi-ngu-nhan-su.html">Đội ngũ nhân sự</a></li>
            <li><a href="tam-nhin-su-menh.html">Tầm nhìn, sứ mệnh và giá trị cốt lõi</a></li>
            <li><a href="doi-voi-khach-hang.html">Đối với khách hàng</a></li>
            <li><a href="co-so-san-xuat.html">Cơ sở sản xuất</a></li>
            <li><a href="nghien-cuu-phat-trien.html">Nghiên cứu &amp; phát triển</a></li>
          </ul>
        </li>
        <li data-nav="brands"><a href="nhan-hieu-v2joy.html">Các nhãn hiệu</a>
          <ul class="menu-nav__sub">
            <li><a href="nhan-hieu-v2joy.html">V2JOY</a></li>
            <li><a href="nhan-hieu-vready.html">VREADY</a></li>
            <li><a href="nhan-hieu-otv.html">OTVhitech</a></li>
          </ul>
        </li>
        <li data-nav="sustain"><a href="phat-trien-ben-vung.html">Phát triển bền vững</a>
          <ul class="menu-nav__sub">
            <li><a href="van-hoa-doanh-nghiep.html">Văn hóa doanh nghiệp</a></li>
            <li><a href="chien-luoc-con-nguoi.html">Chiến lược con người</a></li>
            <li><a href="moi-truong-cong-dong.html">Môi trường và cộng đồng</a></li>
          </ul>
        </li>
        <li data-nav="news"><a href="tin-tuc.html">Tin tức &amp; truyền thông</a></li>
      </div>
      <div class="menu-nav__minor">
        <li data-nav="jobs"><a href="tuyen-dung.html">Tuyển dụng</a></li>
        <li data-nav="contact"><a href="lien-he.html">Liên hệ</a></li>
      </div>
    </ul>
    <img class="menu-overlay__mark" src="assets/img/logo-std.png" alt="">
  </div>
</nav>'''


def footer():
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer__main">
      <div class="footer__brand">
        <h3>{esc(SITE['company_name'])}</h3>
        <p>{esc(SITE['business_reg'])}<br>
        Địa chỉ: {esc(SITE['address'])}<br>
        Điện thoại: {esc(SITE['phone'])} | Email: {esc(SITE['email'])}</p>
        <img class="footer__badge" src="assets/img/badge-bct.png" alt="Đã thông báo Bộ Công Thương">
      </div>
      <nav class="footer__links" aria-label="Liên kết chân trang">
        <div>
          <a href="gioi-thieu.html">Về STD Quốc tế</a>
          <a href="nhan-hieu-v2joy.html">Các nhẫn hiệu</a>
          <a href="phat-trien-ben-vung.html">Phát triển bền vững</a>
          <a href="phat-trien-ben-vung.html">From the People of Vietnam</a>
        </div>
        <div>
          <a href="lien-he.html">Liên hệ</a>
          <a href="tuyen-dung.html">Tuyển dụng</a>
          <a href="#">Đối tác chiến lược</a>
          <a href="#">Trợ giúp</a>
        </div>
        <div class="sep"></div>
      </nav>
    </div>
  </div>
  <div class="footer__bar">
    <div class="container">
      <div class="footer__bar-in">
        <div>Bản quyền đã được bảo hộ bởi ⓒ {esc(SITE['short_name'])}.</div>
        <div class="footer__social">Social Networks: {SVG_FB} {SVG_ZALO}</div>
      </div>
    </div>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>'''


def breadcrumb(items):
    lis = f'<li class="home"><a href="index.html" aria-label="Trang chủ">{SVG_HOME}</a></li>'
    for label, href in items:
        lis += f'<li><a href="{href}">{label}</a></li>' if href else f'<li>{label}</li>'
    return f'<div class="breadcrumb"><div class="container"><ol>{lis}</ol></div></div>'


def hero(img, kind='tall', overlay='', pos=''):
    cls = f'hero hero--{kind}'
    posc = ' hero__img--top' if pos == 'top' else ''
    return f'''<section class="{cls}">
  <img class="hero__img{posc}" src="{img_url(img)}" alt="">
  {overlay}
</section>'''


def quote_overlay(text):
    return f'''<div class="hero__overlay">
    <h1 class="hero__quote">{br_join(text)}</h1>
  </div>'''


SCROLL_OVERLAY = f'''<div class="hero__scroll">{MOUSE}<span>Trượt xuống để khám phá</span></div>'''

BRAND_OVERLAY = '''<div class="hero__overlay">
    <p class="hero__brandline">STD Internationnal Brand</p>
  </div>'''


def page(fname, nav, title, desc, body):
    out = head(title, desc) + f'\n<body data-page="{nav}">\n' + sidebar() + menu() + \
          f'\n<main class="page">\n{body}\n</main>\n' + footer()
    with open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as f:
        f.write(out)
    print('wrote', fname)


def news_card(img, title, date, category, orange=False):
    t = ' news-card__title--orange' if orange else ''
    meta = f'{category} | {fmt_date(date)}'
    return f'''<article class="news-card rv">
      <div class="news-card__img"><img src="{img_url(img)}" alt="" loading="lazy"></div>
      <h3 class="news-card__title{t}">{esc(title)}</h3>
      <div class="news-card__meta">{esc(meta)}</div>
    </article>'''


def story_section(home, tag='section'):
    brands_li = ''.join(f'<li>{esc(b)}</li>' for b in home['story_brands'])
    return f'''<{tag} class="story watermark-wrap">
  <span class="watermark" style="top:36px;left:13%;font-size:clamp(80px,12vw,190px);">Story</span>
  <div class="container">
    <div class="story__grid">
      <div class="rv">
        <h2 class="story__title">{br_join(home['story_title'])}</h2>
        <p class="story__text">{esc(home['story_intro'])}</p>
        <ul class="story__brands">{brands_li}</ul>
        <div class="story__hint">
          {MOUSE}
          <div class="scroll-hint"><span class="arr">⟵</span> Trượt để khám phá <span class="arr">⟶</span></div>
        </div>
      </div>
      <div class="rv">
        <div class="brand-cards">
          <a class="brand-card" href="nhan-hieu-v2joy.html">
            <div class="brand-card__head">
              <span class="brand-card__tag">Nhãn hiệu:</span>
              <div class="brand-card__logo"><img src="assets/img/logo-v2joy.jpg" alt="V2JOY"></div>
              <hr class="brand-card__rule">
              <h3 class="brand-card__title">Thực phẩm chăm<br>sóc sức khỏe</h3>
            </div>
            <div class="brand-card__img"><img src="assets/img/card-v2joy.jpg" alt="V2JOY"></div>
          </a>
          <a class="brand-card" href="nhan-hieu-vready.html">
            <div class="brand-card__head">
              <span class="brand-card__tag">Nhãn hiệu:</span>
              <div class="brand-card__logo"><img src="assets/img/logo-vready.jpg" alt="VREADY"></div>
              <hr class="brand-card__rule">
              <h3 class="brand-card__title">Trà thảo mộc<br>từ dược liệu</h3>
            </div>
            <div class="brand-card__img"><img src="assets/img/card-vready.jpg" alt="VREADY"></div>
          </a>
          <a class="brand-card" href="nhan-hieu-otv.html">
            <div class="brand-card__head">
              <span class="brand-card__tag">Nhãn hiệu:</span>
              <div class="brand-card__logo"><span class="otv-word">OTVhitech</span></div>
              <hr class="brand-card__rule">
              <h3 class="brand-card__title">Cung cấp, mua bán<br>dược liệu Việt</h3>
            </div>
            <div class="brand-card__img"><img src="assets/img/prod-otv-dangsam.jpg" alt="OTV"></div>
          </a>
        </div>
      </div>
    </div>
  </div>
</{tag}>'''


# ================================================================= PAGES
HOME = load('home.yaml')
ABOUT_INDEX = load('about_index.yaml')
SUSTAIN_INDEX = load('sustain_index.yaml')
NEWS = load('news.yaml')
JOBS = load('jobs.yaml')
CONTACT = load('contact.yaml')

ABOUT_LINKS = ['doi-ngu-nhan-su.html', 'tam-nhin-su-menh.html', 'doi-voi-khach-hang.html']
SUSTAIN_LINKS = ['van-hoa-doanh-nghiep.html', 'chien-luoc-con-nguoi.html', 'moi-truong-cong-dong.html']

# ---------- index ----------
home_hero = hero('hero-handshake-wide.jpg', 'full', quote_overlay(HOME['hero_quote']) + SCROLL_OVERLAY)

sustain_home = f'''<section class="sustain watermark-wrap">
  <div class="container">
    <div class="sustain__grid">
      <div class="rv">
        <h2 class="sustain__title">Phát triển bền vững</h2>
        <p class="sustain__text">{br_join(HOME['sustain_intro'], para=True)}</p>
        <a class="btn-outline" href="phat-trien-ben-vung.html">Khám phá</a>
      </div>
      <div class="rv">{DIAGRAM}</div>
    </div>
  </div>
</section>'''

news_home = f'''<section class="news watermark-wrap">
  <span class="watermark" style="top:56px;left:15%;font-size:clamp(60px,9vw,150px);">News/Media</span>
  <div class="container">
    <div class="news__head"><h2 class="section-label" style="font-size:30px;">Tin tức &amp; truyền thông</h2></div>
    <div class="news-grid">
      {''.join(news_card(it['image'], it['title'], it['date'], 'Tin tức & Truyền thông') for it in HOME['news_teaser'])}
    </div>
  </div>
</section>'''

page('index.html', 'home', 'Trang chủ',
     'STD international Co.,LTD - Vì một tương lai sức khỏe, an toàn cho cộng đồng. Sản phẩm sức khỏe từ dược liệu Việt: V2JOY, VREADY, OTV.',
     home_hero + story_section(HOME) + sustain_home + news_home)

# ---------- gioi-thieu ----------
about_cards = ''.join(f'''
      <a class="info-card rv" href="{href}">
        <h3 class="info-card__title">{br_join(ABOUT_INDEX[f'card_{key}_title'])}</h3>
        <p class="info-card__text">{esc(ABOUT_INDEX[f'card_{key}_text'])}</p>
        <span class="info-card__more">Xem chi tiết <span class="arr">⟶</span></span>
      </a>''' for key, href in zip(['team', 'vision', 'customer'], ABOUT_LINKS))

page('gioi-thieu.html', 'about', 'Giới thiệu về STD',
     'Giới thiệu về STD international Co.,LTD - thành lập từ năm 2011, nghiên cứu và phát triển sản phẩm sức khỏe từ dược liệu Việt.',
     hero('hero-handshake-wide.jpg', 'tall', quote_overlay(HOME['hero_quote']))
     + breadcrumb([('Giới thiệu về STD', '')])
     + story_section(HOME)
     + f'<section class="content"><div class="container"><div class="info-cards">{about_cards}</div></div></section>')

# ---------- doi-ngu-nhan-su ----------
d = load('about/nhan-su.yaml')
page('doi-ngu-nhan-su.html', 'about', 'Đội ngũ nhân sự',
     'Đội ngũ nhân sự STD international - những con người làm nên giá trị của STD.',
     hero('hero-hands-tree.jpg', 'mid', '')
     + breadcrumb([('Giới thiệu về STD', 'gioi-thieu.html'), ('Đội ngũ nhân sự', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Đội ngũ nhân sự</h1>
    <p class="page-lead">{esc(d['lead'])}</p>
    <figure class="article-figure rv"><img src="{img_url(d['image'])}" alt="Đội ngũ nhân sự STD"></figure>
    <div class="article-body">{article_paragraphs(d['body'])}</div>
  </div>
</section>''')

# ---------- tam-nhin-su-menh ----------
d = load('about/tam-nhin.yaml')
page('tam-nhin-su-menh.html', 'about', 'Tầm nhìn, sứ mệnh và giá trị cốt lõi',
     'Tầm nhìn, sứ mệnh và giá trị cốt lõi của STD international.',
     hero('hero-skyline.jpg', 'mid', '')
     + breadcrumb([('Giới thiệu về STD', 'gioi-thieu.html'), ('Tầm nhìn, sứ mệnh và giá trị cốt lõi', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Tầm nhìn, sứ mệnh và giá trị cốt lõi</h1>
    <p class="page-lead">{esc(d['lead'])}</p>
    <div class="article-narrow" style="margin-top:44px;">
      <div class="vmc-block rv">
        <h3>Tầm nhìn</h3>
        <p class="vmc-quote">{esc(d['vision'])}</p>
      </div>
      <div class="vmc-block rv">
        <h3>Sứ mệnh</h3>
        <p class="vmc-quote">{esc(d['mission'])}</p>
      </div>
      <div class="vmc-block rv">
        <h3>Giá trị cốt lõi</h3>
        <p class="vmc-quote">{esc(d['core_values'])}</p>
      </div>
    </div>
  </div>
</section>''')

# ---------- doi-voi-khach-hang ----------
d = load('about/khach-hang.yaml')
actions_html = ''.join(f'<p>{esc(a)}</p>' for a in d['actions'])
page('doi-voi-khach-hang.html', 'about', 'Đối với khách hàng',
     'Lấy người dùng làm trung tâm - tôn chỉ của STD international đối với khách hàng.',
     hero('hero-skyline.jpg', 'mid', '')
     + breadcrumb([('Giới thiệu về STD', 'gioi-thieu.html'), ('Đối với khách hàng', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">{esc(d['title'])}</h1>
    <p class="page-lead">{br_join(d['intro'])}</p>
    <div class="article-narrow" style="margin-top:44px;">
      <h3 class="section-label" style="font-size:19px;">Hành động</h3>
      <div class="action-list rv">{actions_html}</div>
    </div>
  </div>
</section>''')

# ---------- co-so-san-xuat ----------
d = load('about/san-xuat.yaml')
partner_cells = ''.join(f'<div class="cell rv"><img src="{img_url(d["partner_logo"])}" alt="VINATEA - since 1958"></div>' for _ in range(4))
page('co-so-san-xuat.html', 'about', 'Cơ sở sản xuất',
     'Cơ sở sản xuất của STD international.',
     hero('hero-handshake-wide.jpg', 'mid', '')
     + breadcrumb([('Giới thiệu về STD', 'gioi-thieu.html'), ('Cơ sở sản xuất', '')])
     + f'''<section class="content watermark-wrap">
  <span class="watermark" style="top:10px;left:0;font-size:clamp(56px,8.5vw,130px);">Manufacturing<br>Facilities</span>
  <div class="container" style="position:relative;z-index:1;">
    <h1 class="page-title" style="padding-top:56px;">Cơ sở sản xuất</h1>
    <div class="article-body">{article_paragraphs(d['body'])}</div>
    <div class="partner-band">
      <div class="partner-band__grid">{partner_cells}</div>
    </div>
  </div>
</section>''')

# ---------- nghien-cuu-phat-trien ----------
d = load('about/nghien-cuu.yaml')
page('nghien-cuu-phat-trien.html', 'about', 'Nghiên cứu & phát triển',
     'Hoạt động nghiên cứu và phát triển sản phẩm của STD international.',
     hero('hero-handshake-wide.jpg', 'mid', '')
     + breadcrumb([('Giới thiệu về STD', 'gioi-thieu.html'), ('Nghiên cứu &amp; phát triển', '')])
     + f'''<section class="content watermark-wrap">
  <span class="watermark" style="top:10px;left:0;font-size:clamp(56px,8.5vw,130px);">Research and<br>development</span>
  <div class="container" style="position:relative;z-index:1;">
    <h1 class="page-title" style="padding-top:56px;">nghiên cứu &amp; phát triển</h1>
    <div class="article-body">{article_paragraphs(d['body'])}</div>
  </div>
</section>''')

# ---------- brand pages ----------
def brand_page(fname, slug, watermark, hero_img, d, active):
    switch = f'''<div class="brand-switch">
      <a href="nhan-hieu-v2joy.html" class="{'active' if active == 'v2joy' else ''}">V2JOY</a>
      <a href="nhan-hieu-vready.html" class="{'active' if active == 'vready' else ''}">VREADY</a>
      <a href="nhan-hieu-otv.html" class="{'active' if active == 'otv' else ''}">OTVhitech</a>
    </div>'''
    prods = ''.join(f'''<div class="product-card rv">
        <div class="product-card__img"><img src="{img_url(p['image'])}" alt="{esc(p['name'])}" loading="lazy"></div>
        <div class="product-card__name">{esc(p['name'])}</div>
      </div>''' for p in d['products'])
    name = d['display_name']
    bullet = d['bullet']
    body = (hero(d['hero_image'], 'mid', BRAND_OVERLAY, pos='top')
      + breadcrumb([('Các nhãn hàng', 'nhan-hieu-v2joy.html'), (esc(name), '')])
      + f'''<section class="content">
  <div class="container">
    <div class="brand-head watermark-wrap">
      <span class="watermark brand-head__mark">{esc(watermark)}</span>
      <div class="brand-head__row">
        <div>
          <h1 class="brand-head__name">{esc(name)}</h1>
          <p class="brand-head__bullet">{esc(bullet)}</p>
          <p class="brand-head__desc">{esc(d['description'])}</p>
          {switch}
        </div>
        <div class="scroll-hint--col scroll-hint" style="padding-bottom:10px;">
          {MOUSE}
          <div class="scroll-hint"><span class="arr">⟵</span> Trượt để khám phá <span class="arr">⟶</span></div>
        </div>
      </div>
    </div>
    <div class="products">
      <div class="products__grid">{prods}</div>
    </div>
  </div>
</section>''')
    page(fname, 'brands', name, f'{name} - {bullet} | Nhãn hiệu của STD international.', body)


brand_page('nhan-hieu-v2joy.html', 'v2joy', 'V2JOY', 'hero-handshake.jpg', load('brands/v2joy.yaml'), 'v2joy')
brand_page('nhan-hieu-vready.html', 'vready', 'VREADY', 'hero-herbs.jpg', load('brands/vready.yaml'), 'vready')
brand_page('nhan-hieu-otv.html', 'otv', 'OTVhitech', 'hero-herbs.jpg', load('brands/otv.yaml'), 'otv')

# ---------- phat-trien-ben-vung ----------
si = SUSTAIN_INDEX
sustain_cards = ''.join(f'''
      <a class="info-card rv" href="{href}">
        <h3 class="info-card__title">{br_join(si[f'card_{key}_title'])}</h3>
        <p class="info-card__text">{esc(si[f'card_{key}_text'])}</p>
        <span class="info-card__more">Xem chi tiết <span class="arr">⟶</span></span>
      </a>''' for key, href in zip(['culture', 'strategy', 'environment'], SUSTAIN_LINKS))

page('phat-trien-ben-vung.html', 'sustain', 'Phát triển bền vững',
     'Phát triển bền vững tại STD international - Khát vọng tiên phong.',
     hero('hero-skyline.jpg', 'tall', '')
     + breadcrumb([('Phát triển bền vững', '')])
     + f'''<section class="content watermark-wrap" style="padding-bottom:0;">
  <span class="watermark" style="top:20px;left:50%;transform:translateX(-50%);text-align:center;font-size:clamp(56px,8.5vw,130px);">Sustainable<br>Development</span>
  <div class="container" style="position:relative;z-index:1;">
    <h1 class="page-title sd-hero-title">Khát vọng tiên phong</h1>
    <p class="page-lead">{br_join(si['intro'], para=True)}</p>
    <div class="sd-diagram rv">{DIAGRAM}</div>
  </div>
</section>
<section class="cards-band">
  <div class="container">
    <div class="info-cards">{sustain_cards}</div>
  </div>
</section>''')

# ---------- van-hoa-doanh-nghiep ----------
d = load('sustain/van-hoa.yaml')
page('van-hoa-doanh-nghiep.html', 'sustain', 'Văn hóa doanh nghiệp',
     'Văn hóa doanh nghiệp tại STD international.',
     hero('hero-office.jpg', 'mid', '')
     + breadcrumb([('Phát triển bền vững', 'phat-trien-ben-vung.html'), ('Văn hóa doanh nghiệp', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Văn hóa doanh nghiệp</h1>
    <p class="page-lead">{esc(d['lead'])}</p>
    <figure class="article-figure rv"><img src="{img_url(d['image'])}" alt="Văn hóa doanh nghiệp STD"></figure>
    <div class="article-body">{article_paragraphs(d['body'])}</div>
  </div>
</section>''')

# ---------- chien-luoc-con-nguoi ----------
d = load('sustain/chien-luoc.yaml')
page('chien-luoc-con-nguoi.html', 'sustain', 'Chiến lược con người',
     'Chiến lược con người của STD international.',
     hero('hero-office.jpg', 'mid', '')
     + breadcrumb([('Phát triển bền vững', 'phat-trien-ben-vung.html'), ('Chiến lược con người', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Chiến lược con người</h1>
    <p class="page-lead">{esc(d['lead'])}</p>
    <figure class="article-figure rv"><img src="{img_url(d['image'])}" alt="Chiến lược con người STD"></figure>
    <div class="article-body">{article_paragraphs(d['body'])}</div>
  </div>
</section>''')

# ---------- moi-truong-cong-dong ----------
d = load('sustain/moi-truong.yaml')
page('moi-truong-cong-dong.html', 'sustain', 'Môi trường và cộng đồng',
     'Môi trường và cộng đồng - cam kết phát triển bền vững của STD international.',
     hero('hero-hands-tree.jpg', 'mid', '')
     + breadcrumb([('Phát triển bền vững', 'phat-trien-ben-vung.html'), ('Môi trường và cộng đồng', '')])
     + f'''<section class="content" style="padding-bottom:0;">
  <div class="container">
    <h1 class="page-title">Môi trường &amp; cộng đồng</h1>
    <p class="page-lead">{esc(d['lead'])}</p>
  </div>
  <div class="env-band">
    <div class="container">
      <div class="env-band__grid">
        <div class="rv">
          <h2 class="env-band__title">{br_join(d['band_title'])}</h2>
          <p class="env-band__sub">{esc(d['band_sub'])}</p>
        </div>
        <div class="env-band__img rv"><img src="{img_url(d['band_image'])}" alt="Cộng đồng STD"></div>
      </div>
    </div>
  </div>
  <div class="container">
    <p class="env-after rv">{esc(d['after'])}</p>
  </div>
</section>''')

# ---------- tin-tuc ----------
notices_html = ''.join(news_card(n['image'], n['title'], n['date'], 'Công bố sản phẩm', orange=True) for n in NEWS['notices'])
articles_html = ''.join(news_card(n['image'], n['title'], n['date'], 'Tin tức & Truyền thông') for n in NEWS['articles'])

page('tin-tuc.html', 'news', 'Tin tức & truyền thông',
     'Tin tức, truyền thông và thông báo công bố sản phẩm của STD international.',
     '<div class="topbar"></div>'
     + breadcrumb([('Tin tức &amp; truyền thông', '')])
     + f'''<section class="content" style="padding-bottom:0;">
  <div class="container"><h1 class="page-title">Tin tức &amp; truyền thông</h1></div>
  <div class="notice-band" style="margin-top:40px;">
    <div class="container">
      <div class="notice-band__head">
        <h2 class="section-label">Thông báo</h2>
        <div class="scroll-hint">{MOUSE} <span class="arr">⟵</span> Trượt để khám phá <span class="arr">⟶</span></div>
      </div>
      <div class="news-grid">{notices_html}</div>
    </div>
  </div>
  <div class="news watermark-wrap">
    <span class="watermark" style="top:46px;left:15%;font-size:clamp(60px,9vw,150px);">News/Media</span>
    <div class="container">
      <div class="news__head"><h2 class="section-label" style="font-size:28px;">Tin tức &amp; truyền thông</h2></div>
      <div class="news-grid">{articles_html}</div>
    </div>
  </div>
</section>''')

# ---------- tuyen-dung ----------
postings_html = ''.join(news_card(j['image'], j['title'], j['date'], 'Tuyển dụng') for j in JOBS['postings'])
page('tuyen-dung.html', 'jobs', 'Tuyển dụng',
     'Cơ hội nghề nghiệp tại STD international.',
     '<div class="topbar"></div>'
     + breadcrumb([('Tuyển dụng', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Tuyển dụng</h1>
    <p class="page-lead">{esc(JOBS['lead'])}</p>
    <div class="news-grid" style="margin-top:48px;">{postings_html}</div>
  </div>
</section>''')

# ---------- lien-he ----------
page('lien-he.html', 'contact', 'Liên hệ',
     'Liên hệ STD international Co.,LTD - Tòa nhà H8, Ngõ 80 Trung Kính, Yên Hòa, Cầu Giấy, Hà Nội.',
     '<div class="topbar"></div>'
     + breadcrumb([('Liên hệ', '')])
     + f'''<section class="content">
  <div class="container">
    <h1 class="page-title">Liên hệ</h1>
    <p class="page-lead">{esc(CONTACT['intro'])}<br>
    {esc(CONTACT['hotline_note'])} <span class="tel">{esc(CONTACT['hotline'])}</span>.</p>
    <div class="contact-grid">
      <div class="rv">
        <div class="contact-map"><img src="{img_url(CONTACT['map_image'])}" alt="Bản đồ trụ sở STD - Hà Nội"></div>
        <div class="contact-hq">
          <div class="contact-hq__label">Trụ sở chính:</div>
          <div>
            <h2 class="contact-hq__name">{esc(SITE['company_name'])}</h2>
            <p class="contact-hq__info">{esc(SITE['business_reg'])}<br>
            Địa chỉ: {esc(SITE['address'])}<br>
            Điện thoại: {esc(SITE['phone'])} | Email: {esc(SITE['email'])}</p>
          </div>
        </div>
      </div>
      <div class="contact-form rv">
        <h2 class="contact-form__title">Gửi cho chúng tôi một lời nhắn</h2>
        <form novalidate>
          <div class="field"><input type="text" name="name" placeholder="Tên của bạn*" required></div>
          <div class="field"><input type="tel" name="phone" placeholder="Số điện thoại*" required></div>
          <div class="field"><input type="email" name="email" placeholder="Email*" required></div>
          <div class="field"><input type="text" name="subject" placeholder="Tiêu đề"></div>
          <div class="field"><textarea name="message" placeholder="Lời nhắn của bạn"></textarea></div>
          <p class="contact-form__note">{esc(CONTACT['form_note'])}</p>
          <div class="contact-form__actions"><button class="btn-outline" type="submit" style="margin-top:0;">Gửi lời nhắn</button></div>
        </form>
      </div>
    </div>
  </div>
</section>''')

print('SITE GENERATED')
