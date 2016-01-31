$(document).ready(function(){
    
    new Morris.Line({
        resize: true,
        element: 'userschart',
        data: [
            { year: '05.10', value: 20 },
            { year: '06.10', value: 10 },
            { year: '07.10', value: 5 },
            { year: '08.10', value: 3 },
            { year: '09.10', value: 17 },
            { year: '10.10', value: 56 },
            { year: '11.10', value: 2 }
            ],
        xkey: 'year',
        ykeys: ['value'],
        labels: ['Value']
        
    });
    
    $('#userstat').addClass('active');
    
    $('#userstat').click(function(){
        $('#bugstat').removeClass('active');
        $('#serverstat').removeClass('active');
        $('#userstat').addClass('active');
        
        $('#serverpref').hide();
        $('#errorlog').hide();
        $('#chartwrapper').show();
    });
    
    $('#bugstat').click(function(){
        $('#userstat').removeClass('active');
        $('#serverstat').removeClass('active');
        $('#bugstat').addClass('active');
        
        $('#serverpref').hide();
        $('#errorlog').show();
        $('#chartwrapper').hide();
    });
    
    $('#serverstat').click(function(){
        $('#userstat').removeClass('active');
        $('#bugstat').removeClass('active');
        $('#serverstat').addClass('active');
        
        $('#serverpref').show();
        $('#errorlog').hide();
        $('#chartwrapper').hide();
        
        $('#ramperc').progress();
        $('#cpuperc').progress();
        $('#sddperc').progress();
    });
    
    $('#newt').click(function(){
        $('#myt').removeClass('active');
        $('#ct').removeClass('active');
        $('#newt').addClass('active');
        
        $('#newtickets').show();
        $('#mytickets').hide();
        $('#ctickets').hide();
    });
    
    $('#myt').click(function(){
        $('#newt').removeClass('active');
        $('#ct').removeClass('active');
        $('#myt').addClass('active');
        
        $('#mytickets').show();
        $('#newtickets').hide();
        $('#ctickets').hide();
    });
    
    $('#ct').click(function(){
        $('#newt').removeClass('active');
        $('#myt').removeClass('active');
        $('#ct').addClass('active');
        
        $('#ctickets').show();
        $('#newtickets').hide();
        $('#mytickets').hide();
    });
});