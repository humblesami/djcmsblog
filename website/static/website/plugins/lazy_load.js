(function(){
    (function(){
        let host_url = window.location.origin + '';
        let invalid_urls = ['/null', host_url + '/', host_url + '/wp-content', '/'];
        let supportsLazyLoad = ('loading' in document.createElement('img'));
    
        let image_sizes = {
            'full': [823, 503],
            'feature': [428, 240],
            'iphone': [382, 233],
            'regular': [283, 173],
            'min': [199, 121]
        };
    
        function get_size_name(el_width){
            let key_name = '';
            if(el_width > (image_sizes['full'][0] + image_sizes['feature'][0]) /2){
                key_name = 'full';
            }
            else if(el_width > (image_sizes['feature'][0] + image_sizes['iphone'][0]) /2){
                key_name = 'feature';
            }
            else if(el_width > (image_sizes['iphone'][0] + image_sizes['regular'][0]) /2){
                key_name = 'iphone';
            }
            else if(el_width > (image_sizes['regular'][0] + image_sizes['min'][0]) /2){
                key_name = 'regular';
            }
            else{
                key_name = 'min';
            }
            return key_name;
        }
    
        window.lazy_load_images = function() {
            // console.log($('.top-news-container').height(), $('#main-container').height(), 222);
            let images_to_load = $('img[src="/static/gui/images/waiting-image.svg"],img[src="/static/gui/images/waiting-image-square.svg"]');
            let pending_image_count = images_to_load.length;
            if (pending_image_count) {                
                // console.log("loading " + pending_image_count+' images');
                images_to_load.each(function (i, el) {
                    let jq_el = $(el);
                    let actual_src = jq_el.attr('data-src');
                    if (actual_src && invalid_urls.indexOf(actual_src) === -1) {
                        let variants = jq_el.attr('data-variants');
                        let el_width = jq_el.width();
                        if(window.is_localhost)
                        {
                            let size_name = get_size_name(el_width);
                            if(size_name !== 'min')
                            {
                                //console.log(size_name, el_width);
                            }
                        }
                        if(variants){
                            let size_name = get_size_name(el_width);
                            if(size_name !== 'full'){
                                actual_src = actual_src.substring(0, actual_src.length - 5);
                                actual_src += '__'+size_name+'.webp';
                            }
                        }
                        if(supportsLazyLoad)
                        {
                            // el.loading = 'lazy';
                            el.src = actual_src;
                            jq_el.removeClass('waiting-square').removeAttr('data-src');
    
                        }
                        else {
                            if(window.has_loaded)
                            {
                                el.src = actual_src;
                                jq_el.removeClass('waiting-square').removeAttr('data-src');
                            }
                        }
                    }
                });
            }
        }
    })();
    window.lazy_load_images();
    $(function(){
        window.lazy_load_images();
    });
})()