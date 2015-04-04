$(function() {


    // Submit post on submit
    $('#showbox').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post();
    });

    // AJAX for posting
    function create_post() {
        console.log("create post is working!") 
         var x=$('#post-text').val()
             console.log(x)// sanity check
        $.ajax({
            url : "create_post/", // the endpoint
            type : "POST", // http method
            data : { the_post : $('#post-text').val() },
             // data sent with the post request
            
            // JSON.stringify(data);
            //handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                // $(".list-group").append("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+
                //     "</span> - <a id='delete-post-"+json.postpk+"'>delete me</a></li>");
                $(".list-group").append("<li class='list-group-item'>"+"<div class='row'>"+"<div class='col-xs-2 col-md-1'>"+
                    "<img src="+ json.pic_path+" class='img-circle img-responsive' style='width: 50%; height:50%;' alt='' /></div>" +
                    "<div class='col-xs-6 col-md-6'><div><div class='mic-info'>" + "<div class='mic-info'>By: <a href=''>"+
                    json.author+ "</a> "+json.created +"</div></div>"+"<div class='comment-text'>"+ json.text+"</div>"+
                    "<div class='action'><button type='button' class='btn btn-success btn-xs' title='Approved' id='upvote' onclick='upvotethis("+json.postpk+","+json.thread_id+")' >"+
                    "<span class='glyphicon glyphicon-arrow-up' id='upvotecount"+json.postpk+"'></span></button>"+
                                   "<button type='button' class='btn btn-danger btn-xs' title='Delete' onclick='downvotethis("+json.postpk+","+json.thread_id+")'>"+
                                        "<span class='glyphicon glyphicon-arrow-down' id='downvotecount"+json.postpk+"'></span>"+
                                    "</button></div>");
                
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});