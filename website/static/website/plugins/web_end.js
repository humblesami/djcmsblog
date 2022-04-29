$(function (){
    window.has_loaded = 1;
    function hide_click_away_elements(e){
        if(!$(e.target).closest('.hide_on_click_away').length)
        {
            let elm = $(e.target);
            let data_target = null;
            while (!elm.is('body'))
            {
                data_target = elm.attr('data-target');
                if(data_target)
                {
                    break;
                }
                elm = elm.parent();
            }
            $('.hide_on_click_away:visible').each(function (i, el){
                let qel = $(this);
                if(qel.is(data_target))
                {
                    return false;
                }
                if(qel.is('.collapse, .show')){
                    qel.removeClass('show');
                }
                else{
                    qel.hide();
                }
            })
        }
    }
    function add_loading() {
        let all_ad_containers = $('.google-adcontainer');
        //console.log('Ads loader active')
        if (!all_ad_containers.length) {
            // console.log('No ads requested');
            return;
        }
        let is_local = web_utils.is_local_host();
        if (is_local) {
            all_ad_containers.remove();
            return;
        }

        let cnt = 0;
        let add_waiter = setInterval(function () {
            cnt += 1;
            all_ad_containers.each(function (i, el) {
                if (!$('.google-adcontainer:not(.loaded)').length) {
                    clearInterval(add_waiter);
                    //console.log('All ' + all_ad_containers.length + ' ads loaded');
                    return;
                }
                if (!$(el).parent().hasClass('loaded')) {
                    let iframe = $(el).find('iframe:first');
                    if (iframe.length) {
                        if (iframe[0].contentWindow.length) {
                            $(el).parent().addClass('loaded').show();
                        } else {
                            el.last_state = 'no content';
                        }
                    } else {
                        el.last_state = 'no iframe';
                    }
                } else if (el.last_state !== 'loaded') {
                    el.last_state = 'loaded';
                    $(el).addClass('loaded');
                }
            });
            if (cnt >= 20) {
                clearInterval(add_waiter);
                let not_loaded = $('.google-adcontainer:not(.loaded)');
                let loaded = $('.google-adcontainer.loaded');
                if (not_loaded.length) {
                    // not_loaded.each(function (i, el) {
                    //     console.warn('Add # ' + (i + 1) + ' not loaded because ', el.last_state);
                    // });
                    not_loaded.hide();
                }
                if (loaded.length) {
                    loaded.css('display', 'block !important');
                    //console.log(loaded.length + ' ads loaded');
                }
            }
        }, 200);
    }
    function top_links(){
        let is_mobile = navigator.userAgent.match(/(iPhone|iPod|iPad)/) ? 'IOS' : false;
        if(!is_mobile)
        {
            is_mobile = navigator.userAgent.match(/Android/) ? 'Android': false;
        }
        let desktop_chrome = false;
        if(!!window.chrome){
            if(!is_mobile)
            {
                desktop_chrome = true;
            }
        }
        if(!desktop_chrome){
            $('.demand_menu:first .date_r').attr('title', 'Click date box to change date').find('input').css('cursor', 'pointer');
        }
        else{
            $('.demand_menu:first .date_r').attr('title', 'Click calendar sign in date box box to change date');
        }
        $('.demand_menu:first .news-by-date-input').change(function (){
            let val  = this.value;
            if(val && val.length === 10){
                window.location = '/news-by-date/'+this.value;
            }
            else{

            }
        })
    }
    $(document).on('touchstart mousedown', 'body', function (e){
        hide_click_away_elements(e);
    });
    add_loading();
    top_links();
});