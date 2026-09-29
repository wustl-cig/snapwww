/* SNaP project page — interactions */

document.addEventListener('DOMContentLoaded', function () {

  /* ---- progressive teaser load + lightbox ---- */
  var teaser  = document.getElementById('teaser');
  var lightbox = document.getElementById('lightbox');

  if (teaser) {
    var full = new Image();
    full.onload = function () {
      teaser.src = teaser.dataset.full;
      teaser.style.filter = 'blur(0)';
    };
    full.src = teaser.dataset.full;

    teaser.parentElement.addEventListener('click', function () {
      if (lightbox) lightbox.style.display = 'flex';
    });
  }

  if (lightbox) {
    lightbox.addEventListener('click', function () { lightbox.style.display = 'none'; });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lightbox) lightbox.style.display = 'none';
  });

  /* ---- tab groups ---- */
  document.querySelectorAll('.tabs').forEach(function (group) {
    var scope = group.closest('[data-tabgroup]') || document;
    group.querySelectorAll('.tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        group.querySelectorAll('.tab').forEach(function (t) { t.classList.remove('active'); });
        scope.querySelectorAll('.panel').forEach(function (p) { p.classList.remove('active'); });
        tab.classList.add('active');
        var target = document.getElementById(tab.dataset.target);
        if (target) target.classList.add('active');
      });
    });
  });

  /* ---- bibtex copy ---- */
  window.copyBibtex = function (btn) {
    var code = document.getElementById('bibtex-code');
    if (!code) return;
    navigator.clipboard.writeText(code.innerText).then(function () {
      var original = btn.innerHTML;
      btn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.innerHTML = original;
        btn.classList.remove('copied');
      }, 2000);
    });
  };

  /* ---- scroll reveal ---- */
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.fade-in').forEach(function (el) { observer.observe(el); });
});
