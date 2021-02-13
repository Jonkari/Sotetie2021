<?php
/**
 * Plugin Name: Sotetie
 */

function sotetie($content) {
    if(is_page('testi')) {
        $content .= file_get_contents(plugins_url('kayttoliittyma.html', __FILE__));
    }
    return $content;
}
function tiedostoLiitto() {
    $tyyli_tiedosto = null;
    if($tyyli_tiedosto != null) {
        wp_register_style('sotetie_haku', plugins_url($tyyli_tiedosto, __FILE__));
        wp_enqueue_style('sotetie_haku');
    }
}

add_filter('the_content', 'sotetie');
add_action('wp_enqueue_scripts', 'tiedostoLiitto')
?>