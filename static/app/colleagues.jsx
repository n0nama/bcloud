var Route = ReactRouter.Route;
var DefaultRoute = ReactRouter.DefaultRoute;
var RouteHandler = ReactRouter.RouteHandler;
var Link = ReactRouter.Link;
var IntlMixin     = ReactIntl.IntlMixin;
var FormattedDate = ReactIntl.FormattedDate;

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

var age = '';
function calculateAge(birthMonth, birthDay, birthYear) {
   var currentDate = new Date();
   var currentYear = currentDate.getFullYear();
   var currentMonth = currentDate.getMonth();
   var currentDay = currentDate.getDate();  
   age = currentYear - birthYear;

   if (currentMonth < birthMonth - 1) {
      age--;
   }
   if (birthMonth - 1 == currentMonth && currentDay < birthDay) {
      age--;
   }
   if (age % 10 == 1){
        return (age + " год")
  	} else if(age % 10 == 2 || age % 10 == 3 || age % 10 == 4){
  	    return (age + " года")
  	} else {
  	    return (age + " лет")
  	}
}

var SearchInput = React.createClass({
	mixins: [IntlMixin],
	render: function() {
		return (
		<div className="sixteen wide column mrg">
			<div className="ui fluid action input">
  				<input type="text" placeholder="Поиск..."></input>
  				<select id="search_filter" className="ui dropdown">
    				<option value="all">По заголовку</option>
    				<option value="articles">По тексту</option>
    				<option value="products">По дате</option>
  				</select>
  			<div type="submit" className="ui blue button">Поиск</div>
			</div>
		</div>
		)}
});

var UsersList = React.createClass({
	mixins: [IntlMixin],
	getInitialState: function() {
    	return {data: []};
  	},
	componentDidMount: function() {
	$.ajax({
	  type: 'GET',
      url: '/users',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data.users});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('/users', status, err.toString());
      }.bind(this)
    });
    $('#search_filter').dropdown();
    $('.blurring.dimmable.image').dimmer({
        on: 'click'
    });
    
  },
    render: function() {
		var users= this.state.data.map(function (user) {
		    var age = calculateAge(user.profile.bd_month, user.profile.bd_day, user.profile.bd_year);
		    var skills = user.profile.skills.map(function (s){
		        return (
		                <a className="ui small grey label card_labels">{s.tags}</a>
		            )
		    });
			return (
				    <div className="card" key={user.id}>
                        <div className="blurring dimmable image">
                            <div className="ui dimmer">
                                <div className="content">
                                    <div className="center">
                                        <div className="ui inverted button">Add Friend</div>
                                    </div>
                                </div>
                            </div>
                            <img src={user.profile.avatar}></img>
                        </div>
                        <div className="content">
                            <div className="header">{user.profile.f_name} {user.profile.l_name}</div>
                            <div className="meta">
                                <a>{age}, {user.profile.spec}, {user.profile.city}</a>
                            </div>
                            <div className="description">
                                {skills}
                            </div>
                        </div>
                        <div className="extra content">
                            <span className="right floated">
                                Joined in 2013
                            </span>
                            <span>
                                <i className="user icon"></i>
                                75 Friends
                            </span>
                            <button className="ui basic green button mrg">Предложить сотрудничество</button>
                        </div>
                    </div>
				)
			});
		return (
			<div className="ui grid">
			    <SearchInput />
			    <div className="ui special cards">
			        {users}
			    </div>
			</div>
		);
	}
});

var SocialApp = React.createClass({
	render: function(){
	return(
		<div className="readiv">
			<RouteHandler locales={['ru-RU']}/>
		</div>
	);
	}
}); 

var routes = (
  <Route path="/users" handler={SocialApp}>
  	<DefaultRoute name="base" handler={UsersList}/>
  </Route>
);

ReactRouter.run(routes, ReactRouter.HistoryLocation, function (Root) {
  React.render(<Root/>, document.getElementById('content'));
});

