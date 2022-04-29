(function (){
    function search_bar(){
        (function (){
            if( window.location.pathname.startsWith('/search-news'))
            {
                $('#search_container').show();
            }
            let formatted_date = '';
            function format_date(given_date){
                let month = given_date.getMonth()+1;
                if(month<10){
                    month = '0'+month;
                }
                let date = given_date.getDate();
                if(date<10){
                    date = '0'+date;
                }
                formatted_date = given_date.getFullYear()+'-'+month+'-'+date;
                return formatted_date;
            }

            $(function (){
                function open_search(){
                    $('#search_container').show();
                }
                $('.menu-btn.search.opener:first').show().click(function (){
                    open_search();
                })
                function close_search(){
                    $('#search_container').hide();
                }
                $('#search_container .closer').click(function (){
                    close_search();
                });

                let loc = window.location.toString().replace(window.location.origin, '');
                if(loc.startsWith('/search-news'))
                {
                    let qs = loc.split('?');
                    if(qs.length < 2){
                        return;
                    }
                    qs = qs[1];
                    let params = qs.split('&');
                    let arr = [];
                    let search_form = $('#search_container form');
                    for(let p of params)
                    {
                        arr = p.split('=')[0];
                        let name = arr[0];
                        let val = arr[1];
                        search_form.find('.input[name="'+name+'"]').val(val);
                    }
                    open_search();
                }
            })
        })()
    }
    search_bar();
})()
let dt_util = {
    format_now: function(format)
    {
        let now = new Date();
        return this.format_time(now, format);
    },
    get_date_str: function(dt){
        if(typeof dt == 'string'){
            dt = new Date(dt);
        }
        return this.format_time(dt, 'Y-mm-dd');
    },
    today_str: function(){
        return this.get_date_str(new Date());
    },
    add_interval: function (interval_type, amount, dt, format){
        if(!dt || dt === 'now')
        {
            dt = new Date();
        }
        if(typeof dt === 'string')
        {
            dt = new Date(dt);
        }
        let new_dt = dt.getTime();

        let milliseconds_to_add = 0;
        switch (interval_type)
        {
            case 's':
                milliseconds_to_add = amount * 1000;
                break;
            case 'i':
                milliseconds_to_add = amount * 60 * 1000;
                break;
            case 'h':
                milliseconds_to_add = amount * 60 * 60 * 1000;
                break;
            case 'd':
                milliseconds_to_add = amount * 24 * 60 * 60 * 1000;
                break;
        }
        new_dt += milliseconds_to_add;
        new_dt = new Date(new_dt);
        // console.log(new_dt, milliseconds_to_add, interval_type, dt);
        if(format)
        {
            new_dt = dt_util.format_time(new_dt, format);
        }
        // console.log(new_dt);
        return new_dt;
    },
    is_same_date: function (dt1, dt2=new Date()) {
        if(typeof dt1 ===  'string' || !isNaN(dt1)){
            dt1 = new Date(dt1);
        }
        if(typeof dt2 ===  'string' || !isNaN(dt2)){
            dt2 = new Date(dt2);
        }
        dt1 = this.format_time(dt1, 'Y-m-d');
        dt2 = this.format_time(dt2, 'Y-m-d');
        return dt1 === dt2;
    },
    format_time: function (dt, format){
        if(!dt || dt === 'now')
        {
            dt = new Date();
        }
        if(typeof dt === 'string')
        {
            dt = new Date(dt);
        }
        if(!format)
        {
            format = 'DS MS d, Y h:mm A'
        }
        const month_names_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ];
        let day_names_short = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

        const month_names_full = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];
        let day_names_full = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

        let result = '';
        let year, month, monthName,  dayName, date_of_month, hour, minute, second;
        let actual_hour = dt.getHours();

        format = format.split('');

        let index = 0;
        let next_char = '';
        let skip_next = false;
        for(ch of format){
            index += 1;
            if(skip_next)
            {
                skip_next = false;
                continue;
            }
            if(index < format.length)
            {
                next_char = format[index];
            }

            switch(ch)
            {
                case 'Y':
                    year = dt.getFullYear();
                    result += year;
                    break;
                case 'y':
                    year = dt.getYear();
                    result += year;
                    break;
                case 'M':
                    monthName = 'M';
                    if(next_char === 'F'){
                        monthName = month_names_full[dt.getMonth()];
                        skip_next = true;
                    }
                    if(next_char === 'S')
                    {
                        monthName = month_names_short[dt.getMonth()];
                        skip_next = true;
                    }
                    result += monthName;
                    break;
                case 'm':
                    month = dt.getMonth() + 1;
                    if(next_char === 'm')
                    {
                        if(month<10)
                        {
                            month ='0'+month;
                        }
                        skip_next = true;
                    }
                    result += month;
                    break;

                case 'D':
                    dayName = 'D';
                    if(next_char === 'F')
                    {
                        dayName = day_names_full[dt.getDay()];
                        skip_next = true;
                    }
                    if(next_char === 'S')
                    {
                        dayName = day_names_short[dt.getDay()];
                        skip_next = true;
                    }
                    result += dayName;
                    break;
                case 'd':
                    date_of_month = dt.getDate();
                    if(next_char === 'd')
                    {
                        date_of_month = dt.getDate();
                        if(date_of_month < 10){
                            date_of_month = '0'+date_of_month;
                        }
                        skip_next = true;
                    }
                    result += date_of_month;
                    break;

                case 'h':
                    hour = actual_hour % 12;
                    if(actual_hour === 12)
                    {
                        hour = actual_hour;
                    }
                    result += hour;
                    break;
                case 'H':
                    hour = actual_hour;
                    if(hour < 10){
                        hour = '0'+hour;
                    }
                    result += hour;
                    break;
                case 'i':
                    minute = dt.getMinutes();
                    if(minute<10){
                        minute = '0'+minute;
                    }
                    result += minute;
                    break;
                case 's':
                    second = dt.getSeconds();
                    if(second<10){
                        second = '0'+second;
                    }
                    result += second;
                    break;
                case 'a':
                    if(actual_hour>11)
                    {
                        result += 'p.m.';
                    }
                    else{
                        result += 'a.m.';
                    }
                    break;
                case 'A':
                    if(actual_hour>11)
                    {
                        result += 'PM';
                    }
                    else{
                        result += 'AM';
                    }
                    break;
                default:
                    result += ch;
            }
        }
        return result;
    },
    to_publish_time: function(published_at){
        published_at = published_at.replace('T',' ');
        published_at = published_at.replace('Z','');
        published_at = new Date(published_at);
        published_at = this.format_time(published_at, 'DS MS d, Y h:i A');
        return published_at;
    },
    make_ago_str: function(time_span_minutes, span, span_name, next_span, next_span_name){
        let res = '';
        let num = 0;
        let rem =  0;
        if(time_span_minutes >= span)
        {
            num = Math.floor (time_span_minutes / span);
            if(num > 1){
                span_name += 's';
            }
            res =  num + ' ' + span_name;
            rem = time_span_minutes % span;
            if(rem >= next_span)
            {
                num = Math.floor (rem / next_span);
                if(num > 1){
                    next_span_name += 's';
                }
                res += ', ' + Math.floor(num) + ' ' + next_span_name;
            }
            res += ' ago';
        }
        return res;
    },
    time_ago_str: function(prev_dt, next_dt = Date()){
        if(typeof prev_dt == 'string')
        {
            prev_dt = new Date(prev_dt);
        }
        if(typeof next_dt == 'string')
        {
            next_dt = new Date(next_dt);
        }
        let time_span = next_dt - prev_dt;
        let time_span_minutes = Math.floor(time_span / (60 * 1000));

        let year =  60 * 24 * 365;
        let month = 60 * 24 * 30;
        let week = 60 * 24 * 7;
        let day = 60 * 24;
        let hour = 60;
        let minute = 1;

        let res = this.make_ago_str(time_span_minutes, year, 'year', month, 'month');
        if(!res){
            res = this.make_ago_str(time_span_minutes, year, 'year', month, 'month');
        }
        if(!res){
            res = this.make_ago_str(time_span_minutes, month, 'month', week, 'week');
        }
        if(!res){
            res = this.make_ago_str(time_span_minutes, week, 'week', day, 'day');
        }
        if(!res){
            res = this.make_ago_str(time_span_minutes, day, 'day', hour, 'hour');
        }
        if(!res){
            res = this.make_ago_str(time_span_minutes, hour, 'hour', minute, 'minute');
        }
        if(!res){
            res = time_span_minutes+' minutes '+ ' ago';
        }
        return res;
    }
}
let web_utils = {
    get_current_url: function(){
        let url = window.location;
        try{
            url = decodeURIComponent(url);
        }
        catch (er){

        }
        return url+'';
    },
    fit_image: function(selector){
        let el1 = $(selector).last();
        if(el1.length){
            let width = el1.width();
            let height = width * 0.588;
            console.log(selector, width, height);
            $(selector).height(height);
        }
    },
    getLocalItemValue: function (key) {
        let item = this.getLocalItemWithExpiry(key);
        if(item && item.value)
        {
            return item.value;
        }
        else{
            return null;
        }
    },

    getLocalItemWithExpiry: function(key) {
        let itemStr = localStorage.getItem(key);
        if (!itemStr) {
            return null
        }
        let item = null;
        try{
            item = JSON.parse(itemStr);
            if(item.expiry)
            {
                return item;
            }
            else{
                item = this.setLocalItem(key, item);
                return item;
            }
        }
        catch (er){
            console.log(key + ' updating with expiry and value ', itemStr);
            item = this.setLocalItem(key, itemStr);
            return item;
        }
    },

    getLocalItemExpiry: function(key) {
        let itemStr = localStorage.getItem(key);
        if (!itemStr) {
            return null
        }
        let item = null;
        try{
            item = JSON.parse(itemStr);
            if(item.expiry)
            {
                return item.expiry;
            }
            else{
                item = this.setLocalItem(key, item);
                return item.expiry;
            }
        }
        catch (er){
            console.log(key + ' updating with expiry and value ', itemStr);
            item = this.setLocalItem(key, itemStr);
            return item.expiry;
        }
    },

    setLocalItem: function (key, value, duration={type: 'M', amount:1}) {
        const now = new Date().getTime();
        switch (duration.type){
            case 'M':
                duration = 1000 * 3600 * 24 * 30 * duration.amount;
                break;
            case 'd':
                duration = 1000 * 3600 * 24 * duration.amount;
                break;
            case 'h':
                duration = 1000 * 3600 * duration.amount;
                break;
            case 'm':
                duration = 1000 * 60 * duration.amount;
                break;
            case 's':
                duration = 1000 * duration.amount;
                break;
        }
        duration = now + duration;
        const item = {
            value: value,
            expiry: duration,
        }
        localStorage.setItem(key, JSON.stringify(item));
        return item;
    },

    isMobile : {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (this.Android() || this.BlackBerry() || this.iOS() || this.Opera() || this.Windows());
        }
    },

    searchParams: function (p_name) {
        let params = (new URL(document.location)).searchParams;
        let val = params.get(p_name); // is the string "Jonathan Smith".
        return val;
    },

    is_mobile_device: function (){
        return this.isMobile.any();
    },

    is_local_host: function (){
        let host_name = window.location.hostname;
        // console.log('Host is ' + host);
        if(host_name.indexOf('localhost') > -1 || host_name.indexOf('127.0.0.1') > -1){
            return true;
        }
    },
    set_image_heights: function (selector){
        if(1 === 1){
            return;
        }
        let article_container = $(selector);
        let c_width = article_container.children().first().width();
        c_width *= 0.66;
        let images = article_container.children().find('a img');
        //compromising cls
        images.css('height', c_width + 'px');
    },
    what_browser :function(){
        if((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1 )
        {
            return ('Opera');
        }
        else if(navigator.userAgent.indexOf("Chrome") != -1 || navigator.userAgent.indexOf("Chromium") != -1)
        {
            return ('Chrome');
        }
        else if(navigator.userAgent.indexOf("Safari") != -1)
        {
            return ('Safari');
        }
        else if(navigator.userAgent.indexOf("Firefox") != -1 )
        {
            return ('Firefox');
        }
        else if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
        {
            return ('IE');
        }
        else
        {
            return ('unknown');
        }
    },
}
