import { DEFAULT_ALIAS } from './site.mjs';

/** The configured base path without a trailing slash (e.g. `/rich-click/latest`). */
export const base = import.meta.env.BASE_URL.replace(/\/$/, '');

/** Each docs version is deployed to its own directory under one root (see docs/_deploy.py). */
export const deployRoot = base.slice(0, Math.max(base.lastIndexOf('/'), 0));
export const currentVersion = base.slice(base.lastIndexOf('/') + 1);
/** Where canonical URLs point; unchanged for a build without a version directory. */
export const canonicalBase = currentVersion ? `${deployRoot}/${DEFAULT_ALIAS}` : base;

/** A page URL's path within the site, from the leading slash after the base. */
export const sitePath = (url: URL): string => url.pathname.slice(base.length) || '/';

export interface DocsVersion {
  version: string;
  title: string;
  aliases: string[];
}
/** Deployed docs versions, passed in by docs/_deploy.py (absent in local development). */
export const docsVersions: DocsVersion[] = JSON.parse(process.env.DOCS_VERSIONS ?? '[]');
