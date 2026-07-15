/* STD International — shared behaviour */
(function () {
  'use strict';

  if (location.search.indexOf('shot') > -1) {
    document.documentElement.classList.add('shot-mode');
  }

  /* ---- overlay menu ---- */
  var burger = document.querySelector('.sidebar__burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- mark active menu item ---- */
  var page = document.body.getAttribute('data-page');
  if (page) {
    document.querySelectorAll('.menu-nav [data-nav]').forEach(function (li) {
      if (li.getAttribute('data-nav') === page) li.classList.add('active');
    });
  }

  /* ---- drag-scroll for horizontal sliders ---- */
  document.querySelectorAll('.brand-cards').forEach(function (el) {
    var down = false, startX = 0, startScroll = 0;
    el.addEventListener('pointerdown', function (e) {
      down = true; startX = e.clientX; startScroll = el.scrollLeft;
      el.setPointerCapture(e.pointerId);
    });
    el.addEventListener('pointermove', function (e) {
      if (down) el.scrollLeft = startScroll - (e.clientX - startX);
    });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      el.addEventListener(ev, function () { down = false; });
    });
  });

  /* ---- reveal on scroll ---- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('on'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('on'); });
  }

  /* ---- contact form -> mail client ---- */
  var form = document.querySelector('.contact-form form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { var f = form.querySelector('[name=' + n + ']'); return f ? f.value.trim() : ''; };
      var subject = v('subject') || 'Lien he tu website STD International';
      var body = 'Ten: ' + v('name') + '\nSo dien thoai: ' + v('phone') + '\nEmail: ' + v('email') + '\n\n' + v('message');
      window.location.href = 'mailto:info@stdpharma.vn?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }
})();
