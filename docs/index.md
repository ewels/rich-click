---
title: rich-click
hide:
  - title
  - navigation
glightbox: false
---

<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

<p align="center">
<img src="images/rich-click-logo.png#only-light" align="center" class="glightbox-disable">
<img src="images/rich-click-logo-darkmode.png#only-dark" align="center" class="glightbox-disable">
</p>
<p align="center">
    <em>Richly rendered command line interfaces in click.</em>
</p>
<p align="center">
    <img src="https://img.shields.io/pypi/v/rich-click?logo=pypi" alt="PyPI"/>
    <img src="https://github.com/ewels/rich-click/workflows/Test%20Coverage/badge.svg" alt="Test Coverage badge">
    <img src="https://github.com/ewels/rich-click/workflows/Lint%20code/badge.svg" alt="Lint code badge">
</p>


---

<p align="center">
    <a href="https://ewels.github.io/rich-click">Documentation</a>&nbsp&nbsp·&nbsp&nbsp<a href="https://github.com/ewels/rich-click">Source Code</a>&nbsp&nbsp·&nbsp&nbsp<a href="https://github.com/ewels/rich-click">Changelog</a>
</p>

---

{%
    include-markdown '../README.md'
    start="<!--include-start-->"
%}

<script>
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[src^="images/"]:not(.glightbox-disable)');
    images.forEach(function(img) {
        img.classList.add('screenshot');
    });
});
</script>
