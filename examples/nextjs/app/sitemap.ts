import type { MetadataRoute } from 'next';

const SITE = 'https://yoursite.com';

// Build this list from your real routes (filesystem, CMS, or DB query).
const ROUTES = ['', '/about', '/pricing', '/blog'];

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return ROUTES.map((path) => ({
    url: `${SITE}${path}`,
    lastModified,
    changeFrequency: path === '' ? 'daily' : 'weekly',
    priority: path === '' ? 1 : 0.7,
  }));
}
