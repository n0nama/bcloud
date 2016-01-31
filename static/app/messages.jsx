var IntlMixin = ReactIntl.IntlMixin;
var FormattedDate = ReactIntl.FormattedDate;

var Messages = React.createClass({
    getInitialState: function(){
        return ({data: []})
    },
    componentWillMount: function(){
        $.ajax({
            type: "POST",
            url: this.props.urls[this.props.section],
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            context: this,
            success: function(data) {
                this.setState({data: data})
            }
        })
    },

    render: function(){
        return(
            <div className="col-lg-12 mrg">
                <NavBar active={this.props.section} urls={this.props.urls}/>
                <MessagesBox messages={this.state.data} urls={this.props.urls} section={this.props.section}/>
            </div>
        )
    }
});

var NavBar = React.createClass({
    render: function(){
        return(
            <div className="ui large secondary menu">
                <div className="item"><a className="ui primary button" href={this.props.urls.compose}>Написать</a></div>
                <a href={this.props.urls.inbox} className={this.props.active=="inbox"? "active item": "item"}>
                    Входящие
                </a>
                <a href={this.props.urls.outbox} className={this.props.active=='outbox'? 'active item': 'item'}>
                    Отправленные
                </a>
                <a href={this.props.urls.favorite} className={this.props.active=='favorite'? 'active item': 'item'}>
                    Избранное
                </a>
                <a href={this.props.urls.draft} className={this.props.active=='draft'? 'active item': 'item'}>
                    Черновики
                </a>
                <a href={this.props.urls.trash} className={this.props.active=='trash'? 'active item': 'item'}>
                    Корзина
                </a>
            </div>
        )
    }
});

var MessagesBox = React.createClass({
    render: function(){
        var MessageNodes = this.props.messages.map(function(data){
            return(
                <Message message_data={data} urls={this.props.urls} section={this.props.section}/>
            )
        }.bind(this));

        return(
            <div className="ui segment">
    			<table className="ui very basic table">
            		<tbody>
                        {MessageNodes}
                    </tbody>
                </table>
            </div>
        )
    }
});

var Message = React.createClass({
    mixins: [IntlMixin],

    send_request: function(url){
        $.ajax({
            type: "POST",
            url: url+this.props.message_data.id.toString()+'/',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            context: this,
            success: function(data) {
                var node = this.getDOMNode();
                React.unmountComponentAtNode(node);
                $(node).remove();
            }
        });
    },

    delete: function(){
        this.send_request(this.props.urls.delete)
    },

    add_favorite: function(){
        this.send_request(this.props.urls.add_favorite)
    },

    remove_favorite: function(){
        this.send_request(this.props.urls.remove_favorite)
    },

    restore: function(){
        this.send_request(this.props.urls.restore)
    },

    render: function(){
        var view_url=this.props.urls.view+this.props.message_data.id.toString()+'/';
        var date = new Date(this.props.message_data.date);
        var buttons;
        if (this.props.section == 'favorite'){
            buttons = <td className="right aligned collapsing">
                        <a onClick={this.remove_favorite}><i className="small bordered star half empty yellow icon mbless"></i></a>
                        <a onClick={this.delete}><i className="small bordered red remove icon mbless"></i></a>
                      </td>
        }
        else if (this.props.section == 'trash'){
            buttons = <td className="right aligned collapsing">
                        <a onClick={this.restore}><i className="small bordered red checkmark icon mbless"></i></a>
                      </td>
        }
        else {
            buttons = <td className="right aligned collapsing">
                        <a onClick={this.add_favorite}><i className="small bordered star yellow icon mbless"></i></a>
                        <a onClick={this.delete}><i className="small bordered red remove icon mbless"></i></a>
                      </td>
        }
        return(
            <tr>
                <td className="collapsing">
                    <div className="ui checkbox">
                        <input type="checkbox" id="mess_check"/>
                        <label htmlFor="mess_check"></label>
                    </div>
                </td>
                <td>
                    <a href={view_url}>{this.props.message_data.subject}</a>
                </td>
                <td className="right aligned collapsing">
                    <img className="ui avatar image" src={this.props.message_data.avatar}/>{this.props.message_data.sender}
                </td>
                <td className="right aligned collapsing"><small>
                    <FormattedDate
                        value={date}
                        day = 'numeric'
                        month="long"
                    />
                </small></td>
                {buttons}
            </tr>
        )
    }
});

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

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        !(/^(\/\/|http:|https:).*/.test(url));
}