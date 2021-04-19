<?php
/**
 * Plugin Name: Sotetie
 */

class Sotetie2021 {
    public function __construct() {
        add_action('admin_menu', array($this, 'luo_sivu'));
        add_shortcode('sotetie', array($this, 'sotetie') );
        add_filter('query_vars', array($this,'haku_muuttuja'));
        add_action('admin_init', array($this,'rekisteroi_asetus'));
    }
    public function luo_sivu() {
        $sivu_otsikko = "Asetukset";
        $plugin_nimi = 'Sotetie2021';
        $ss = 'manage_options';
        $slug = 'sotetie2021';
        $callback = array($this, 'sivun_sisalto');
        add_menu_page($sivu_otsikko, $plugin_nimi, $ss, $slug, $callback);
    }
    public function rekisteroi_asetus() {
        register_setting('sotetie2021_asetukset', 'sotetie2021_asetukset', array($this, 'sotetie2021_perusarvo'));
        add_settings_section('sotetie2021_asetukset', 'Sotetie2021 Asetukset', array($this, 'sotetie2021_asetukset_teksti'), 'sotetie2021');
        add_settings_field('sotetie2021_api_rajapinta_osoite', 'API rajapinnan osoite ilman päättävää / päätettä', array($this, 'sotetie2021_api_rajapinta_osoite'), 'sotetie2021', 'sotetie2021_asetukset');
    }
    public function sotetie2021_perusarvo($input) {
        return $input;
    }   

    public function sotetie2021_api_rajapinta_osoite() {
        $asetukset = get_option('sotetie2021_asetukset');
        $rajapinta = "http://127.0.0.1/api";
        if(isset($asetukset['api_rajapinta_osoite'])) {
            $rajapinta = $asetukset['api_rajapinta_osoite'];
        }
        echo '<input type="text" id="sotetie2021_asetukset_api_rajapinta_osoite" name="sotetie2021_asetukset[api_rajapinta_osoite]" value="'.$rajapinta.'">';
    }
    public function sotetie2021_asetukset_teksti() {
        echo "Sivun nimi. Lyhytkoodina toimii [sotetie]";
    }
    public function sivun_sisalto() {
        echo '<div class="wrap"><form method="post" action="options.php">';
        settings_fields('sotetie2021_asetukset');
        do_settings_sections('sotetie2021');
        echo '<input name="submit" class="button button-primary" type="submit" value="Tallenna">';
        echo '</form></div>';
    }
    function sotetie() {
        $content = "";
        $asetukset = get_option('sotetie2021_asetukset');
        $sivun_nimi = "testi";
        $rajapinta = "http://127.0.0.1";
        $tyyli_tiedosto = "styles.css";
        wp_register_style('sotetie_haku', plugins_url($tyyli_tiedosto, __FILE__));
        wp_enqueue_style('sotetie_haku');
        wp_deregister_script('jquery');
        wp_enqueue_script('jquery', 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js');

        wp_register_script('sotetie_script', plugins_url("script.js", __FILE__));
        wp_enqueue_script('sotetie_script', true);

        if(isset($asetukset["sivun_nimi"])) {
            $sivun_nimi = $asetukset["sivun_nimi"];
        }
        if(isset($asetukset["api_rajapinta_osoite"])) {
            $rajapinta = $asetukset["api_rajapinta_osoite"];
        }
        if ( get_query_var('haku') ) {
            $content .= "
            <script>
            var valmisHaku = function(genOsaamiset) {
            if(\"".get_query_var('haku')."\" in genOsaamiset) {
                document.querySelector(\".aihe\").value = \"".get_query_var('haku')."\"
                }
            }
            </script>
            ";
        } else {
            $content .= "
            <script>
            var valmisHaku = undefined;
            </script>
            ";
        }

        $content .= "
        <script>
        var osoite = '".$rajapinta."';
        </script>
        ";
        $content .= file_get_contents(plugin_dir_path(__FILE__).'kayttoliittyma.html');
    
        
        return $content;
    }
    function haku_muuttuja( $vars ){
        $vars[] = "haku";
        return $vars;
      }
    
}
new Sotetie2021();

?>