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

var SearchInput = React.createClass({
	mixins: [IntlMixin],
	render: function() {
		return (
		<div className="col-lg-12 mrg">
			<div className="ui fluid action input">
  				<input type="text" placeholder="Поиск..."></input>
  				<select className="ui dropdown">
    				<option value="all">По заголовку</option>
    				<option value="articles">По тексту</option>
    				<option value="products">По дате</option>
  				</select>
  			<div type="submit" className="ui blue button">Поиск</div>
			</div>
		</div>
		)}
});

var Marked = React.createClass({
	mixins: [IntlMixin],
	render: function() {
		var post = this.props.data.map(function (post) {
		if (post.marked){
				return (
					<div className="col-lg-12 mrg" key={post.id}>
						<div className="ui raised segment marked">
							<h3 className="ui dividing header">
								<Link to="id" params={{id: post.id}}>{post.title}</Link>
								<p className="rght">
									<small><FormattedDate value={post.pub_date} day="numeric" month="numeric" year="numeric"/></small>
								</p>
							</h3>
							{post.text}<br></br>
							<p className="rght"><Link to="id" params={{id: post.id}}><small>Читать далее</small><i className="arrow right small icon"></i></Link></p>
						</div>
					</div>
					)
					}
				});
		return (
			<div>
				{post}
			</div>
		);
	}
});

var NewsList = React.createClass({
	mixins: [IntlMixin],
	getInitialState: function() {
    	return {data: []};
  	},
	componentDidMount: function() {
	$.ajax({
	  type: 'GET',
      url: '/news/',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('/news/', status, err.toString());
      }.bind(this)
    });
  },
  	render: function() {
		var news = this.state.data.map(function (news) {
			var classes = React.addons.classSet({
        			'ui red raised segment': ( news.status === 'II' ),
					'ui blue raised segment': ( news.status === 'IN' ),
					'ui yellow raised segment': ( news.status === 'BU' ),
					'ui green raised segment': ( news.status === 'UP' ),
    		});
			if (!news.marked){
			return (
				<div className="col-lg-12 mrg" key={news.id}>
					<div className={classes}>
					<h3 className="ui dividing header">
						<Link to="id" params={{id: news.id}}>{news.title}</Link>
						<p className="rght">
							<small><FormattedDate value={news.pub_date} day="numeric" month="numeric" year="numeric"/></small>
						</p>
					</h3>
						{news.text.substr(0, 400)}...<br></br>
						<p className="rght"><Link to="id" params={{id: news.id}}><small>Читать далее</small><i className="arrow right small icon"></i></Link></p>
					</div>
				</div>
				)
				}
			});
		return (
			<div>
			<SearchInput />
			<Marked data={this.state.data}/>
				{news}
			</div>
		);
	}
});

var Replies = React.createClass({
	render: function(){
	var rep = this.props.replies.map(function(rep){
		return(
			<div className="comments" key={rep.id}>
				<div className="comment">
					<a className="avatar">
						<img src={rep.staff.profile.avatar}></img>
					</a>
					<div className="content">
						<a className="author" href={'/users/' + rep.staff.username}>{rep.staff.profile.f_name} {rep.staff.profile.l_name}</a>
							<div className="metadata">
								<span className="date"><FormattedDate value={rep.pub_date} day="numeric" month="long" year="numeric"/></span>
							</div>
							<div className="text">
								{rep.text}
							</div>
					</div>
    			</div>
			</div>
		);
	})
	return(
		<div>
			{rep}
		</div>
	);
	}
});

var Comments = React.createClass({
	getInitialState: function() {
    	return {edit: false};
  	},
	editClick: function(e) {
	    this.setState({ edit: true });
  	},
	handleDelete: function(e) {
	    e.preventDefault();
		var pk = this.props.comment.id;
    	this.props.onCommentDelete({pk});
    	return;
  	},
	handleEdit: function(e) {
	    e.preventDefault();
		var pk = this.props.comment.id;
		var text = React.findDOMNode(this.refs.editText).value.trim();
    	this.props.onCommentUpdate({pk:pk, text: text});
		this.setState({ edit: false });
    	return;
  	},
	render: function(){
	var user = this.props.user;
		return (
			<div className="comment" key={this.props.comment.id}>
				<a className="avatar">
      				<img src={this.props.comment.author.profile.avatar}></img>
    			</a>
    			<div className="content">
      				<a className="author" href={"/users/" + this.props.comment.author.username}>{this.props.comment.author.profile.f_name} {this.props.comment.author.profile.l_name}</a>
      				<div className="metadata">
        				<span className="date"><FormattedDate value={this.props.comment.pub_date} day="numeric" month="long" year="numeric"/></span>
						{this.props.comment.author.username == user ? 
							(
								<div>
									{!this.state.edit ?
									(<button className="ui compact black basic icon mini button" onClick={this.editClick}><i className="write icon"></i></button>):
									(<button className="ui compact black basic icon mini button" onClick={this.handleEdit}><i className="checkmark icon"></i></button>)}
									<button className="ui compact red basic icon mini button" onClick={this.handleDelete}><i className="remove icon"></i></button>
								</div>
							):null
						}
      				</div>
					{!this.state.edit ?
						(
						<div className="text">
        					{this.props.comment.text}
						</div>
						):
						(
						<div className="text">
						<div className="ui form">
							<textarea rows="1" ref="editText">
        						{this.props.comment.text}
							</textarea>
						</div>
						</div>
						)
					}
    			</div>
				<Replies replies={this.props.comment.replies}/>
			</div>
	);
}
});

var CommentForm = React.createClass({
	handleSubmit: function(e) {
	    e.preventDefault();
		var new_id = this.props.id;
    	var author = this.props.author;
    	var text = React.findDOMNode(this.refs.text).value.trim();
    	if (!text || !author) {
      		return;
    	}
    this.props.onCommentSubmit({new: new_id, author: author, text: text});
    React.findDOMNode(this.refs.text).value = '';
    return;
  },
	render: function(){
		return(
		<div className="col-lg-12 mrg">
			<h3 className="ui dividing header">Добавить комментарий</h3>
			<form method="POST" role="form" className="ui reply form" onSubmit={this.handleSubmit}>
    			<div className="field">
      				<textarea ref="text"></textarea>
    			</div>
				<button className="ui blue labeled submit icon button" type="submit" value="SUBMIT" name="submit"><i className="icon edit"></i> Отправить</button>
			</form>
		</div>
		);
	}
});

var SinglePost = React.createClass({
	mixins: [IntlMixin],
	render: function() {
		var post = this.props.data.map(function (post) {
		var classes = React.addons.classSet({
        			'ui red raised segment mrg': ( post.status === 'II' ),
					'ui blue raised segment mrg': ( post.status === 'IN' ),
					'ui yellow raised segment mrg': ( post.status === 'BU' ),
					'ui green raised segment mrg': ( post.status === 'UP' ),
    		});
				return (
				<div>
					<div className="col-lg-12 mrg" key={0}><Link to="base"><i className="arrow left small icon"></i><small className="grey">Назад</small></Link></div>
					<div className="col-lg-12 mrg" key={post.id}>
						<div className={classes}>
						<h3 className="ui dividing header">
							<Link to="id" params={{id: post.id}}>{post.title}</Link>
							<p className="rght">
								<small><FormattedDate value={post.pub_date}/></small>
							</p>
						</h3>
							{post.text}
							
						</div>
					</div>
				</div>
					)
				});
		return (
			<div>
				{post}
			</div>
		);
	}
});

var SinglePostBox = React.createClass({
	mixins: [IntlMixin],
	handleCommentSubmit: function(comment) {
		var id = this.props.params.id;
    	$.ajax({
      		url: '/news/' + id,
      		dataType: 'json',
      		type: 'POST',
      		data: comment,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
      		success: function(data) {
        		this.setState({comments: data});
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/news/' + this.props.id, status, err.toString());
      		}.bind(this)
   	 	});
  	},
	handleCommentUpdate: function(comment) {
		var id = this.props.params.id;
    	$.ajax({
      		url: '/news/' + id,
      		dataType: 'json',
      		type: 'UPDATE',
      		data: comment,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
      		success: function(data) {
        		this.setState({comments: data});
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/news/' + id, status, err.toString());
      		}.bind(this)
   	 	});
  	},
	handleCommentDelete: function(pk) {
		var id = this.props.params.id;
    	$.ajax({
      		url: '/news/' + id,
      		dataType: 'json',
      		type: 'DELETE',
      		data: pk,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
      		success: function(data) {
        		this.setState({comments: data});
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/news/' + id, status, err.toString());
      		}.bind(this)
   	 	});
  	},
	getInitialState: function() {
    	return {post: [], comments: [], user: [], id: [], uid: []};
  	},
    componentDidMount: function () {
		var id = this.props.params.id;
    	$.ajax({
	  		type: 'GET',
      		url: '/news/' + id,
      		dataType: 'json',
      		cache: false,
      		success: function(data) {
        		this.setState({post: data.post, user: data.user, comments: data.comments, id: id, uid: data.uid});
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/news/' + id, status, err.toString());
      		}.bind(this)
    		});
  		},
	render: function(){
	var user=this.state.user;
	var comments = this.state.comments.map(function (comment) {
		return(
			<Comments comment={comment} user={user} onCommentDelete={this.handleCommentDelete} onCommentUpdate={this.handleCommentUpdate}/>
			);
		}.bind(this));
	return(
		<div>
			<SinglePost data={this.state.post}/>
			{this.state.comments.length > 0 ? 
			(
			<div className="col-lg-12 mrg">
				<div id="newscomments" className="ui threaded comments">
					<h3 className="ui dividing header">Комментарии</h3>
					{comments}
				</div>
			</div>
			):null}
			<CommentForm onCommentSubmit={this.handleCommentSubmit} author={this.state.uid} id={this.state.id}/>
		</div>
	);
	}
});

var NewsApp = React.createClass({
	render: function(){
	return(
		<div className="readiv">
			<RouteHandler locales={['ru-RU']}/>
		</div>
	);
	}
}); 

var routes = (
  <Route path="/news/" handler={NewsApp}>
  	<DefaultRoute name="base" handler={NewsList}/>
    <Route name="id" path="/news/:id" handler={SinglePostBox}/>
  </Route>
);

ReactRouter.run(routes, ReactRouter.HistoryLocation, function (Root) {
  React.render(<Root/>, document.getElementById('content'));
});

