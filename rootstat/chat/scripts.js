var id;
var last = '';

$(document).ready(function(){
    $('.contact').click(function(){
        $('.contact').removeClass('contact-active');
        $(this).addClass('contact-active');
        $('#chat-history-list').empty();
        id = this.getAttribute('room_id');
        get_history(id);
    });

    $('#input').keypress(function(e) {
        if(e.which == 13) {
            send()
        }
    });
    $('#input').keyup(function(e){
       if(e.which == 13){
           $('#input').val('');
       }
    });
});

function receive_message(date, text, sender, name){
    if (sender == username){
        $('#chat-history-list').append('<div class=bubbledLeft><p class=sender>Вы</p>'+text+'<br><b class=date>'+date+'</b></div>');
    }
    else{
        $('#chat-history-list').append('<div class=bubbledRight><p class=sender>'+name+'</p>'+text+'<br><b class=date>'+date+'</b></div>');
    }
}

function close_socket(){
    try {
        sockjs.close();
    }
    catch (TypeError){
        console.log('No active connections')
    }
}