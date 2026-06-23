// Renders JSON-LD in a React Server Component with XSS-safe escaping.
// Never pass untrusted user-generated content into `data`.

type JsonLdProps = { data: Record<string, unknown> };

export function JsonLd({ data }: JsonLdProps) {
  const json = JSON.stringify(data).replace(/</g, '\\u003c');
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: json }}
    />
  );
}

// Usage in a page (app/page.tsx):
//
// import { JsonLd } from './components/JsonLd';
//
// export default function Page() {
//   return (
//     <>
//       <JsonLd data={{
//         '@context': 'https://schema.org',
//         '@type': 'Organization',
//         name: 'Your Company',
//         url: 'https://yoursite.com',
//         sameAs: ['https://www.linkedin.com/company/you'],
//       }} />
//       {/* page content */}
//     </>
//   );
// }
