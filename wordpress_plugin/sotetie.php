<?php
/**
 * Plugin Name: Testi
 */
function sotetie($content) {
    if(is_page('testi')) {
        $content .= "<table><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></table>";
    }
    return $content;
}
add_filter( 'the_content', 'sotetie');
?>