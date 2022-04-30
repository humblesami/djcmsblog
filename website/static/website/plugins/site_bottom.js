function fit_scale_image(selector=''){
    if(!selector)
    {
        selector = '.blog-visual';
    }
    selector += ':not(.scaled)';
    $(selector).each(function(i, el){
        let width = $(el).width();
        // console.log(i, 111);
        let height = width * 0.588;
        $(el).addClass('scaled').height(height);
    });
}
fit_scale_image();