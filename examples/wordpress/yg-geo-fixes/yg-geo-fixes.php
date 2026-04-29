<?php
/**
 * Plugin Name: Auto-GEO Fixes
 * Description: GEO pattern: serves /llms.txt, patches robots.txt with AI UAs + Sitemap, enriches Person JSON-LD with sameAs, auto-fills Rank Math meta descriptions and FAQPage schema on publish for service-type pages.
 * Version: 1.2.0
 * Author: seo-geo-skill (https://github.com/yanivgoldenberg/seo-geo-skill)
 * License: PolyForm Noncommercial 1.0.0
 *
 * CONFIGURATION: edit the constants below for your site.
 * See README.md for what this plugin does and how each hook contributes to GEO score.
 */

if (!defined('ABSPATH')) { exit; }

// === CONFIGURE FOR YOUR SITE ===
define('AUTO_GEO_VERSION', '1.2.0');
define('AUTO_GEO_SITEMAP_URL', 'https://YOUR_DOMAIN/sitemap_index.xml');
define('AUTO_GEO_SERVICES_SLUG', 'services');
define('AUTO_GEO_DESC_SUFFIX', ' - YOUR_BRAND_TAGLINE.');
define('AUTO_GEO_CONTACT_URL', 'https://YOUR_DOMAIN/contact/');

// sameAs URLs to append to Person entity in Rank Math JSON-LD.
// Example: ['https://www.youtube.com/@YOUR_HANDLE', 'https://medium.com/@YOUR_HANDLE']
// Note: PHP 7+ allows arrays in define(); we avoid serialize()/unserialize() to
// eliminate the object-injection class of bugs even when the source is trusted.
define('AUTO_GEO_PERSON_SAMEAS_EXTRAS', [
    'YOUR_YOUTUBE_URL',
]);

// AI crawler user agents to explicitly allow in robots.txt.
define('AUTO_GEO_AI_CRAWLERS', [
    'OAI-SearchBot',
    'Bytespider',
    'Amazonbot',
    'FacebookBot',
    'Cohere-ai',
    'PerplexityBot',
    'ClaudeBot',
    'GPTBot',
    'Google-Extended',
    'ChatGPT-User',
    'Applebot-Extended',
    'Meta-ExternalAgent',
    'DuckAssistBot',
    'CCBot',
]);

// llms.txt body. Replace with your own. See https://llmstxt.org for the spec.
define('AUTO_GEO_LLMS_TXT', <<<'LLMS'
# YOUR_BRAND_NAME

> One-paragraph summary of what you do, your positioning, and your primary audience. Lead with the most citation-worthy claim. 2-4 sentences max.

## About

Longer About section. Who you are, what you've done, how long you've been doing it, who your clients are. Include at least one numeric proof point (revenue scaled, clients served, years operating).

## Core Services

- [Service Name](https://YOUR_DOMAIN/services/service-slug/): one-sentence description with price range
- [Another Service](https://YOUR_DOMAIN/services/other-slug/): one-sentence description

## Contact

- Email: you@YOUR_DOMAIN
- LinkedIn: https://linkedin.com/in/YOUR_HANDLE
- Book intro call: https://YOUR_DOMAIN/contact/

## Site

- Homepage: https://YOUR_DOMAIN/
- All services: https://YOUR_DOMAIN/services/
LLMS
);

// === END CONFIGURATION ===

add_action('init', function () {
    $req = isset($_SERVER['REQUEST_URI']) ? parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) : '';
    if ($req === '/llms.txt') {
        status_header(200);
        header('Content-Type: text/plain; charset=utf-8');
        header('Cache-Control: public, max-age=3600');
        header('X-Robots-Tag: all');
        echo AUTO_GEO_LLMS_TXT;
        exit;
    }
}, 0);

add_filter('robots_txt', function ($output, $public) {
    $extras = AUTO_GEO_AI_CRAWLERS;
    if (!is_array($extras)) { return $output; }
    $append = "\n";
    foreach ($extras as $ua) {
        $ua = preg_replace('/[^A-Za-z0-9\-_]/', '', (string) $ua);
        if ($ua === '') { continue; }
        $append .= "User-agent: {$ua}\nAllow: /\n\n";
    }
    $append .= "Sitemap: " . esc_url_raw(AUTO_GEO_SITEMAP_URL) . "\n";
    return $output . $append;
}, 20, 2);

add_filter('rank_math/json_ld', function ($data) {
    if (!is_array($data)) { return $data; }
    $extra = AUTO_GEO_PERSON_SAMEAS_EXTRAS;
    if (!is_array($extra)) { return $data; }
    $extra = array_filter($extra, function ($u) { return $u !== 'YOUR_YOUTUBE_URL' && !empty($u) && filter_var($u, FILTER_VALIDATE_URL); });
    if (empty($extra)) { return $data; }
    foreach ($data as $k => $node) {
        if (is_array($node) && isset($node['@type']) && $node['@type'] === 'Person') {
            $existing = isset($node['sameAs']) && is_array($node['sameAs']) ? $node['sameAs'] : [];
            $data[$k]['sameAs'] = array_values(array_unique(array_merge($existing, $extra)));
        }
    }
    return $data;
}, 99);

function auto_geo_synthesize_description($post) {
    $excerpt = trim((string) $post->post_excerpt);
    $source = $excerpt;
    if (strlen($source) < 60) {
        $content = (string) $post->post_content;
        $content = preg_replace('/\[[^\]]+\]/', ' ', $content);
        $content = wp_strip_all_tags($content);
        $content = preg_replace('/\s+/', ' ', $content);
        $content = trim($content);
        if (strlen($content) >= 60) {
            $sentences = preg_split('/(?<=[.!?])\s+/', $content, 3);
            $source = trim(implode(' ', array_slice($sentences, 0, 2)));
        }
    }
    if (strlen($source) < 60) {
        $source = trim((string) $post->post_title);
    }
    $suffix = AUTO_GEO_DESC_SUFFIX;
    $target_max = 160;
    $room_for_suffix = $target_max - strlen($suffix);
    if (strlen($source) > $room_for_suffix) {
        $source = substr($source, 0, $room_for_suffix);
        $last_space = strrpos($source, ' ');
        if ($last_space !== false && $last_space > 80) {
            $source = substr($source, 0, $last_space);
        }
        $source = rtrim($source, " ,.-;:");
    }
    $desc = $source;
    if (strlen($desc) + strlen($suffix) <= $target_max) {
        $desc = $desc . $suffix;
    }
    if (strlen($desc) < 80) {
        error_log('[auto-geo] thin synthesized description for post ' . $post->ID . ' (len=' . strlen($desc) . ')');
    }
    return $desc;
}

function auto_geo_is_services_child($post) {
    if ($post->post_type !== 'page') { return false; }
    if (strpos($post->post_name, AUTO_GEO_SERVICES_SLUG . '/') === 0) { return true; }
    $parent = get_page_by_path(AUTO_GEO_SERVICES_SLUG);
    if ($parent && (int)$post->post_parent === (int)$parent->ID) { return true; }
    return false;
}

add_action('transition_post_status', function ($new_status, $old_status, $post) {
    if ($new_status !== 'publish') { return; }
    if (!in_array($post->post_type, ['page', 'post'], true)) { return; }
    if (wp_is_post_autosave($post->ID) || wp_is_post_revision($post->ID)) { return; }

    $existing_desc = get_post_meta($post->ID, 'rank_math_description', true);
    if (empty($existing_desc)) {
        $desc = auto_geo_synthesize_description($post);
        if (!empty($desc)) {
            update_post_meta($post->ID, 'rank_math_description', $desc);
        }
    }

    if (auto_geo_is_services_child($post)) {
        $snippet_type = get_post_meta($post->ID, 'rank_math_rich_snippet', true);
        if (empty($snippet_type)) {
            update_post_meta($post->ID, 'rank_math_rich_snippet', 'article');
        }
    }

    $canonical = get_post_meta($post->ID, 'rank_math_canonical_url', true);
    if (empty($canonical)) {
        $permalink = get_permalink($post->ID);
        if (!$permalink) {
            error_log('[auto-geo] canonical missing and permalink unresolvable for post ' . $post->ID);
        }
    }
}, 10, 3);

add_filter('rank_math/json_ld', function ($data) {
    if (!is_singular('page')) { return $data; }
    $post = get_post();
    if (!$post || !auto_geo_is_services_child($post)) { return $data; }

    foreach ((array) $data as $node) {
        if (is_array($node) && isset($node['@type']) && $node['@type'] === 'FAQPage') {
            return $data;
        }
    }

    $override = get_post_meta($post->ID, '_yg_faq_json', true);
    if (!empty($override)) {
        $decoded = json_decode($override, true);
        if (is_array($decoded) && !empty($decoded)) {
            $data['auto_geo_faq'] = [
                '@context' => 'https://schema.org',
                '@type' => 'FAQPage',
                'mainEntity' => $decoded,
            ];
            return $data;
        }
    }

    $title = get_the_title($post);
    $url = get_permalink($post);
    $contact = AUTO_GEO_CONTACT_URL;
    $default_qa = [
        [
            '@type' => 'Question',
            'name' => "What does {$title} include?",
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text' => "See the full scope and deliverables at {$url}.",
            ],
        ],
        [
            '@type' => 'Question',
            'name' => 'How long is a typical engagement?',
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text' => 'Replace this default answer via the _yg_faq_json post meta key (JSON array of Question nodes).',
            ],
        ],
        [
            '@type' => 'Question',
            'name' => 'How do we start?',
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text' => "Book an intro call at {$contact}.",
            ],
        ],
    ];

    $data['auto_geo_faq'] = [
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => $default_qa,
    ];
    return $data;
}, 100);

add_action('admin_notices', function () {
    if (!current_user_can('activate_plugins')) { return; }
    $screen = function_exists('get_current_screen') ? get_current_screen() : null;
    if (!$screen || $screen->id !== 'plugins') { return; }
    $crawler_count = is_array(AUTO_GEO_AI_CRAWLERS) ? count(AUTO_GEO_AI_CRAWLERS) : 0;
    echo '<div class="notice notice-info"><p><strong>Auto-GEO Fixes v' . esc_html(AUTO_GEO_VERSION) . '</strong> auto-wires: ';
    echo '(1) serves <code>/llms.txt</code> at root, ';
    echo '(2) patches <code>robots.txt</code> with ' . (int) $crawler_count . ' AI crawlers + Sitemap, ';
    echo '(3) appends sameAs URLs to Person in Rank Math JSON-LD, ';
    echo '(4) auto-fills empty Rank Math meta descriptions on publish (140-160 chars), ';
    echo '(5) injects FAQPage schema on <code>/' . esc_html(AUTO_GEO_SERVICES_SLUG) . '/*</code> children (override via <code>_yg_faq_json</code> post meta), ';
    echo '(6) logs canonical-missing warnings.</p></div>';
});
