<?php
/**
 * Force public HTTPS URLs behind Caddy (no ports, no LAN).
 */
if (!defined('ABSPATH')) {
    return;
}
$public = 'https://church.giize.com';
if (!defined('WP_HOME')) {
    define('WP_HOME', $public);
}
if (!defined('WP_SITEURL')) {
    define('WP_SITEURL', $public);
}
$strip = static function ($url) use ($public) {
    if (!is_string($url) || $url === '') {
        return $url;
    }
    return preg_replace('#https?://[^/]+(:\d+)?#', $public, $url, 1);
};
add_filter('option_home', static fn () => $public);
add_filter('option_siteurl', static fn () => $public);
add_filter('home_url', $strip, 1);
add_filter('site_url', $strip, 1);
add_filter('content_url', $strip, 1);
add_filter('plugins_url', $strip, 1);
add_filter('script_loader_src', $strip, 1);
add_filter('style_loader_src', $strip, 1);
add_filter('wp_redirect', $strip, 1);
add_filter('redirect_canonical', static function ($redirect) use ($strip) {
    return $redirect ? $strip($redirect) : $redirect;
}, 1);
