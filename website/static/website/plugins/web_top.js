window.on_dom_shown_functions=[];
window.dom_styled=0;
function show_dom(el)
{
    el.rel = 'stylesheet';window.dom_styled +=1;el.onload=null;
    el.onload=null;if(window.dom_styled != 2) return ;
    for(let fun of window.on_dom_shown_functions){fun();}
    window.dom_shown = 1;
    //console.log('Page loaded after all on dom shown functions');
}

function disable_ads(){
    window.adsbygoogle = {
        enabled: true,
        loaded: true,
        push: function () {
            return;
        },
        google_ad_client: "",
        enable_page_level_ads: true
    }
}
let host = window.location.hostname;
if (host === "localhost" || host === '127.0.0.1') {
    window.is_localhost = 1;
    disable_ads();
}

(function (){
    let user_active = 0;
    let activation_waiters = [];
    function on_user_active(new_function){
        // console.log('user active', new_function, 11);
        if(user_active){
            if(new_function)
            {
                activation_waiters.push(new_function)
            }
            for (const fun of activation_waiters){
                fun.ref(fun.args);
            }
            activation_waiters = [];
        }
        else{
            if(new_function)
            {
                activation_waiters.push(new_function)
            }
        }
    }
    window.on_user_active = on_user_active;

    function add_listeners(events, lister){
        for(const ev of events){
            window.addEventListener(ev, lister);
        }
    }
    function remove_listeners(events, lister){
        for(const ev of events){
            window.removeEventListener(ev, lister);
        }
    }
    function on_mousedown_touch_scroll(){
        if(user_active){
            remove_listeners(['mousedown', 'touchstart', 'scroll'], on_mousedown_touch_scroll);
        }
        else{
            user_active = 1;
            on_user_active();
            remove_listeners(['mousedown', 'touchstart', 'scroll'], on_mousedown_touch_scroll);
        }
    }
    add_listeners(['mousedown', 'touchstart', 'scroll'], on_mousedown_touch_scroll);

    let mouse_moved = 0;
    function on_mouse_move(){
        mouse_moved += 1;
        if(user_active){
            remove_listeners(['mousemove'], on_mouse_move);
        }
        else if(mouse_moved >= 3){
            user_active = 1;
            on_user_active();
            remove_listeners(['mousemove'], on_mouse_move);
        }
    }
    add_listeners(['mousemove'], on_mouse_move);
})();
var top_utils = {
    set_image_container_height: function(selector){
        let el1 = $(selector).first();
        if(el1.length){
            let width = el1.width();
            let height = width * 0.588;
            $(selector).height(height);
        }
    },
}
