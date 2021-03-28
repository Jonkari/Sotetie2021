<?php
/**
 * Plugin Name: Sotetie
 */

function sotetie($content) {
    if(is_page('testi')) {
        if ( get_query_var('haku') ) {
            $content .= "
            <script>
            var valmisHaku = function(genOsaamiset) {if(\"".get_query_var('haku')."\" in genOsaamiset) {document.querySelector(\".aihe\").value = \"".get_query_var('haku')."\"}}
            </script>
            ";
            }
        $content .= file_get_contents(plugin_dir_path(__FILE__).'kayttoliittyma.html');

    }
    
    return $content;
}
function add_query_vars_filter( $vars ){
    $vars[] = "haku";
    return $vars;
  }

function tiedostoLiitto() {
    if(is_page('testi')) {
        $tyyli_tiedosto = "styles.css";
        if($tyyli_tiedosto != null) {
            wp_register_style('sotetie_haku', plugins_url($tyyli_tiedosto, __FILE__));
            wp_enqueue_style('sotetie_haku');
            wp_deregister_script('jquery');
            wp_enqueue_script('jquery', 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js');
        }
    }
}

add_filter('the_content', 'sotetie');
add_action('wp_enqueue_scripts', 'tiedostoLiitto');
add_filter( 'query_vars', 'add_query_vars_filter' );
?>