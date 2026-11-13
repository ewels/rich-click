# Legacy logo copies

The site's logos are the SVGs in `docs/public/images/`. These PNG renders of `rich-click-light.svg` and `rich-click-dark.svg` (at 2x) stay here because the README of every rich-click release up to 1.9.x (as shown on PyPI) loads the logo from `https://raw.githubusercontent.com/ewels/rich-click/main/docs/images/`. Deleting them would break the logo on those PyPI pages.

Keep them as real files (raw.githubusercontent.com doesn't follow symlinks) and re-render them if the logos change.
