/* beezee.si – majhen skript brez odvisnosti.
   Stran deluje tudi brez njega; tukaj so samo izboljšave:
   mobilni meni, filter portfolia, čebela vodnica, polnjenje z medom, pošiljanje obrazcev brez osvežitve. */
(function () {
  'use strict';
  var d = document;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- mobilni meni ---------- */
  var menu = d.getElementById('mobile-menu');
  var burger = d.getElementById('burger');
  function toggleMenu(open) {
    if (!menu) return;
    var isOpen = typeof open === 'boolean' ? open : !menu.classList.contains('open');
    menu.classList.toggle('open', isOpen);
    d.body.classList.toggle('menu-open', isOpen);
    if (burger) burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }
  if (burger) burger.addEventListener('click', function () { toggleMenu(); });
  if (menu) {
    menu.querySelectorAll('a, .close').forEach(function (el) { el.addEventListener('click', function () { toggleMenu(false); }); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') toggleMenu(false); });
  }

  /* ---------- filter portfolia (satovje 3-2-3) ---------- */
  var grid = d.getElementById('grid');
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.hex'));
    var empty = d.getElementById('empty');
    function layout(key) {
      var list = cards.filter(function (c) { return key === 'all' || c.getAttribute('data-cat') === key; });
      grid.innerHTML = '';
      var i = 0, n = 3;
      while (i < list.length) {
        var row = d.createElement('div'); row.className = 'row';
        list.slice(i, i + n).forEach(function (c) { row.appendChild(c); });
        grid.appendChild(row);
        i += n; n = n === 3 ? 2 : 3;
      }
      if (empty) empty.classList.toggle('show', list.length === 0);
    }
    d.querySelectorAll('.filters .pill').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('.filters .pill').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        layout(b.getAttribute('data-filter'));
      });
    });
  }

  /* ---------- polnjenje korakov z medom ---------- */
  var steps = d.getElementById('steps');
  if (steps) {
    if (!('IntersectionObserver' in window) || reduce) { steps.classList.add('honey'); }
    else {
      var io = new IntersectionObserver(function (es) {
        if (es.some(function (e) { return e.isIntersecting; })) { steps.classList.add('honey'); io.disconnect(); }
      }, { threshold: 0.25 });
      io.observe(steps);
    }
  }

  /* ---------- čebela vodnica ---------- */
  var bee = d.getElementById('bee');
  if (bee && !reduce && window.innerWidth > 760 && 'requestAnimationFrame' in window) {
    var flip = bee.querySelector('.bee-flip');
    var spots = d.querySelectorAll('[data-bee-spot]');
    if (spots.length) {
      var cur = { x: -100, y: 200, init: false }, lastX = 0, idle = 0;
      var loop = function () {
        requestAnimationFrame(loop);
        var vh = window.innerHeight, best = null, bd = Infinity;
        for (var i = 0; i < spots.length; i++) {
          var r = spots[i].getBoundingClientRect();
          var dist = Math.abs(r.top - vh * 0.42);
          if (dist < bd) { bd = dist; best = r; }
        }
        var tx = best.right + 24, ty = best.top - 50;
        tx = Math.max(8, Math.min(window.innerWidth - 70, tx));
        ty = Math.max(90, Math.min(vh - 80, ty));
        if (!cur.init) { cur.x = tx; cur.y = ty; cur.init = true; bee.style.opacity = '1'; }
        var dx = tx - cur.x, dy = ty - cur.y;
        if (Math.abs(dx) < 0.2 && Math.abs(dy) < 0.2) { if (++idle > 120) return; } else idle = 0;
        cur.x += dx * 0.06; cur.y += dy * 0.06;
        bee.style.transform = 'translate(' + cur.x + 'px,' + cur.y + 'px)';
        if (flip) { var dir = cur.x - lastX; if (Math.abs(dir) > 0.3) flip.style.transform = dir < 0 ? 'scaleX(-1)' : 'scaleX(1)'; }
        lastX = cur.x;
      };
      loop();
    }
  }

  /* ---------- obrazci (fetch, brez osvežitve) ---------- */
  function ajaxForm(form, onOk, onErr) {
    if (!form || !window.fetch || !window.FormData) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = form.getAttribute('data-sending') || '…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j && j.ok, j: j }; }); })
        .then(function (res) { if (res.ok) onOk(res.j); else onErr(res.j); })
        .catch(function () { onErr(); })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = label; } });
    });
  }

  var cf = d.getElementById('contact-form');
  if (cf) {
    var sentBox = d.getElementById('sent-box');
    var cmsg = d.getElementById('contact-msg');
    ajaxForm(cf,
      function () { cf.style.display = 'none'; if (sentBox) sentBox.classList.add('show'); },
      function () { if (cmsg) { cmsg.textContent = cf.getAttribute('data-error'); cmsg.classList.add('err'); cmsg.hidden = false; } });
  }

  var hf = d.getElementById('hive-form');
  if (hf) {
    var hmsg = d.getElementById('hive-msg');
    var hnote = d.getElementById('hive-note');
    ajaxForm(hf,
      function () { hf.style.display = 'none'; if (hnote) hnote.style.display = 'none'; if (hmsg) { hmsg.textContent = hf.getAttribute('data-thanks'); hmsg.hidden = false; } },
      function () { if (hmsg) { hmsg.textContent = hf.getAttribute('data-error'); hmsg.hidden = false; } });
  }
})();
