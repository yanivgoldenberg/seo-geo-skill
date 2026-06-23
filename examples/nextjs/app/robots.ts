import type { MetadataRoute } from 'next';

const SITE = 'https://yoursite.com';

// Search/answer crawlers drive AI-search visibility. Training crawlers only
// affect whether your content is used to train models. Allowing GPTBot
// (training) does NOT make you visible in ChatGPT search - that needs
// OAI-SearchBot and ChatGPT-User.
const SEARCH_CRAWLERS = [
  'OAI-SearchBot',
  'ChatGPT-User',
  'Claude-SearchBot',
  'Claude-User',
  'PerplexityBot',
  'Perplexity-User',
  'Google-CloudVertexBot',
  'DuckAssistBot',
  'MistralAI-User',
];

const TRAINING_CRAWLERS = [
  'GPTBot',
  'ClaudeBot',
  'Google-Extended',
  'Applebot-Extended',
  'anthropic-ai',
  'cohere-ai',
  'meta-externalagent',
  'Amazonbot',
  'CCBot',
  'Bytespider',
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/' },
      { userAgent: SEARCH_CRAWLERS, allow: '/' },
      { userAgent: TRAINING_CRAWLERS, allow: '/' },
    ],
    sitemap: `${SITE}/sitemap.xml`,
  };
}
