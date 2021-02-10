<?php
/**
 * Plugin Name: Testi
 */

function testi($content) {
    if(is_page('testi')) {
        $content .= file_get_contents($_SERVER["DOCUMENT_ROOT"]."\\wordpress\\wp-content\\plugins\\testi\\kayttoliittyma.html", FILE_USE_INCLUDE_PATH);
    }
    return $content;
}
function testi_css() {
    return null;
}
add_filter( 'the_content', 'testi');
?>