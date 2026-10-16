/* Wireframe behaviour. No framework. Every feature binds to a data attribute
   and does nothing if the attribute is missing. */
(function () {
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  // Mega menus: click to open, Escape or outside click to close.
  $$('[data-mega]').forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute('data-mega'));
    if (!panel) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = btn.getAttribute('aria-expanded') === 'true';
      closeMenus();
      if (!open) { btn.setAttribute('aria-expanded', 'true'); panel.classList.add('is-open'); }
    });
    panel.addEventListener('click', function (e) { e.stopPropagation(); });
  });
  function closeMenus() {
    $$('[data-mega]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    $$('.mega.is-open').forEach(function (p) { p.classList.remove('is-open'); });
  }
  document.addEventListener('click', closeMenus);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMenus(); closeModals(); } });

  // Mobile drawer and generic toggles.
  $$('[data-toggle]').forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute('data-toggle'));
    if (!target) return;
    btn.addEventListener('click', function () {
      var open = target.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Tabs: [data-tabs] container with buttons [aria-controls].
  $$('[data-tabs]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute('aria-selected', on ? 'true' : 'false');
          var p = document.getElementById(t.getAttribute('aria-controls'));
          if (p) p.hidden = !on;
        });
      });
    });
  });

  // Modals.
  function closeModals() { $$('[data-modal]').forEach(function (m) { m.hidden = true; }); }
  $$('[data-modal-open]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var m = document.querySelector('[data-modal="' + btn.getAttribute('data-modal-open') + '"]');
      if (!m) return;
      e.preventDefault();
      m.hidden = false;
      var f = m.querySelector('input, button'); if (f) f.focus();
    });
  });
  $$('[data-modal]').forEach(function (m) {
    m.addEventListener('click', function (e) { if (e.target === m || e.target.hasAttribute('data-modal-close')) closeModals(); });
  });

  // Version switcher: link to the same page on the other version.
  // URL source, in order: data/versions.json url, then the Vercel branch URL
  // pattern (<project>-git-<branch>-<scope>.vercel.app). Otherwise the link
  // stays on /hub/#versions, which explains how to set it.
  var vbar = document.querySelector('[data-versions]');
  if (vbar) {
    var cfg; try { cfg = JSON.parse(vbar.getAttribute('data-versions')); } catch (e) { cfg = null; }
    if (cfg) {
      var byId = {}; cfg.versions.forEach(function (v) { byId[v.id] = v; });
      var cur = byId[cfg.current];
      $$('[data-version]', vbar).forEach(function (a) {
        var target = byId[a.getAttribute('data-version')];
        var base = (target.url || '').replace(/\/$/, '');
        var host = location.hostname, marker = '-git-' + cur.branch + '-';
        if (!base && host.indexOf(marker) !== -1) {
          base = location.protocol + '//' + host.replace(marker, '-git-' + target.branch + '-');
        }
        if (!base) { a.classList.add('is-unset'); a.title = 'Set the ' + target.id + ' URL in data/versions.json'; return; }
        var path = location.pathname;
        var onlyHere = (cfg.only_in && cfg.only_in[cur.id]) || [];
        if (onlyHere.indexOf(path) !== -1) path = '/';
        a.href = base + path + location.search + location.hash;
      });
    }
  }

  // Cookie banner.
  var cookie = document.querySelector('[data-cookie]');
  if (cookie && !store.get('wf-cookie')) cookie.hidden = false;
  $$('[data-cookie-choice]').forEach(function (b) {
    b.addEventListener('click', function () { store.set('wf-cookie', b.getAttribute('data-cookie-choice')); cookie.hidden = true; });
  });

  // Wireframe notes toggle.
  var nt = document.querySelector('[data-notes-toggle]');
  if (store.get('wf-notes') === 'off') document.body.classList.add('hide-notes');
  if (nt) {
    var label = function () { nt.textContent = document.body.classList.contains('hide-notes') ? 'Show notes' : 'Hide notes'; };
    label();
    nt.addEventListener('click', function () {
      var off = document.body.classList.toggle('hide-notes');
      store.set('wf-notes', off ? 'off' : 'on');
      label();
    });
  }

  // Ads toggle (v2): compare the page with and without ad inventory.
  var at = document.querySelector('[data-ads-toggle]');
  if (store.get('wf-ads') === 'off') document.body.classList.add('hide-ads');
  if (at) {
    var adLabel = function () { at.textContent = document.body.classList.contains('hide-ads') ? 'Show ads' : 'Hide ads'; };
    adLabel();
    at.addEventListener('click', function () {
      var off = document.body.classList.toggle('hide-ads');
      store.set('wf-ads', off ? 'off' : 'on');
      adLabel();
    });
  }

  // Mobile anchor ad: closes for the rest of the session.
  var anchor = document.querySelector('.ad--anchor');
  var session = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  if (anchor && session.get('wf-anchor') === 'closed') { anchor.hidden = true; document.body.classList.remove('has-anchor'); }
  $$('[data-ad-close]').forEach(function (b) {
    b.addEventListener('click', function () {
      anchor.hidden = true;
      document.body.classList.remove('has-anchor');
      session.set('wf-anchor', 'closed');
    });
  });

  // Stepper (match tool): [data-stepper] with children [data-step].
  $$('[data-stepper]').forEach(function (root) {
    var steps = $$('[data-step]', root), bars = $$('.progress span', root), i = 0;
    function show() {
      steps.forEach(function (s, n) { s.hidden = n !== i; });
      bars.forEach(function (b, n) { b.classList.toggle('is-done', n <= i); });
    }
    $$('[data-next]', root).forEach(function (b) { b.addEventListener('click', function () { if (i < steps.length - 1) { i++; show(); } }); });
    $$('[data-prev]', root).forEach(function (b) { b.addEventListener('click', function () { if (i > 0) { i--; show(); } }); });
    show();
  });

  // Facet search: filter the labels inside the same facet.
  $$('.facet input[type="search"]').forEach(function (inp) {
    inp.addEventListener('input', function () {
      var q = inp.value.toLowerCase();
      $$('label', inp.closest('.facet')).forEach(function (l) { l.hidden = l.textContent.toLowerCase().indexOf(q) === -1; });
    });
  });

  // Forms in the wireframe never submit anywhere.
  $$('form[data-wf-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var go = f.getAttribute('data-wf-form');
      if (go && go !== 'stay') { window.location.href = go; return; }
      var msg = f.querySelector('[data-form-msg]'); if (msg) msg.hidden = false;
    });
  });
})();
