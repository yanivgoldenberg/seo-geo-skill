// Serves /llms.txt as text/plain from an App Router route handler.
// Note (2026): no major AI search engine consumes llms.txt yet (Google
// publicly declined it). Treat as low-cost hygiene / dev-tool aid, not a
// citation driver. Keep it accurate and small.
export const dynamic = 'force-static';

const SITE = 'https://yoursite.com';

const BODY = `# Your Company

> One-line description of what you do and who for.

## Core pages
- [Product](${SITE}/product): what it does
- [Pricing](${SITE}/pricing): plans and cost
- [Docs](${SITE}/docs): developer documentation

## About
Founded YEAR. Key facts, named people, verifiable claims.
`;

export async function GET() {
  return new Response(BODY, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'X-Robots-Tag': 'all',
    },
  });
}
