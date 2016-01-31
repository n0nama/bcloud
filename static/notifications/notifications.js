function messages_handler(message){
    var id = JSON.parse(message).id;
    get_notification(id);
}

function show_notification(a){
    if (box.children()[0].tagName == 'P') {
        box.empty();
        $('.notification-activator').css('color','#31708f');
    }
    var notif;
    if ('link' in a){
        notif = "<div class='notification' id='message'><i class='fa fa-times notification-close' id=" +a.id+ "></i><a class='notif_link' href='"+ a.link +"'><h5>"+ a.body +"</p></a></div>";
    }
    else{
        notif = "<div class='notification' id='message'><i class='fa fa-times notification-close' id=" +a.id+ "></i><h5>"+ a.body +"</p></div>";
    }
    box.append(notif);
    $('.notification-close').click(function(event){delete_notification(event)});
}

$(document).ready(function(){
    box = $('.notification-box');
    $('.notification-activator').click(function(){
        box.toggle();
    });
    get_unread_notifications();
});

function delete_notification(notif){
    var id = notif.target.id;
    read_notification(id);
    notif.target.parentElement.remove();
    if (box.html() == ''){
        box.html('<p>Нет оповещений</p>');
        $('.notification-activator').css('color','#777');
    }
};

function get_unread_notifications(){
    $.post(
        get_last_url,
        function(data){
            var notf = JSON.parse(data);
            for (var i in notf){
                show_notification(notf[i]);
            }
        }
    )
}

function read_notification(id){
   $.post(
        read_notification_url,
        {'id': id}
    );
};

function get_notification(id){
    $.post(
        get_notification_url,
        {'id': id},
        function(data){
            if (data != 'Error'){
                var a = JSON.parse(data);
                show_notification(a);
            }
        }
    );
};