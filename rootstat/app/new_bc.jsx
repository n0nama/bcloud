var Route = ReactRouter.Route;
var DefaultRoute = ReactRouter.DefaultRoute;
var RouteHandler = ReactRouter.RouteHandler;
var Link = ReactRouter.Link;
var dta = [
  {id: 1, title: "Breaking News #1", text: "This is one test new", date: "12.05.2015"},
  {id: 5, title: "Breaking News #2", text: "This is *another* test new", date: "03.05.2015"}
  
];

var NewsList = React.createClass({
	getInitialState: function() {
    	return {data: []};
  	},
	componentDidMount: function() {
    $.ajax({
      url: '/api/news/?format=json',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  	},
  	render: function() {
		return (
			<div>
			{ this.state.data.map(function (news) {
					return (
					<div className="col-lg-12 mrg" key={news.id}>
						<h3 className="ui top attached header">
							<Link to="id" params={{id: news.id}}>{news.title}</Link>
							<p className="rght">
								{news.date}
							</p>
						</h3>
						<div className="ui green attached segment">
							{news.text.substr(0, 400)}... <a onClick={this.handleClick}>Read more &gt;&gt;</a>
						</div>
					</div>)
				})
				}
				12
			</div>
		);
	}
});


var Comments = React.createClass({
	render: function(){
	return(
		<div className="comment">
			<a className="avatar">
      			<img src="/media/avatars/nonama_avatar.jpg"></img>
    		</a>
    		<div className="content">
      			<a className="author">Matt</a>
      			<div className="metadata">
        			<span className="date">Today at 5:42PM</span>
      			</div>
      			<div className="text">
        			How artistic!
      			</div>
      			<div className="actions">
        			<a className="reply">Reply</a>
      			</div>
    		</div>
		</div>
		);
	}
});

var CommentList = React.createClass({
	render: function(){
	return(
	<div className="col-lg-12 mrg">
	<div className="ui comments">
		<h3 className="ui dividing header">Comments</h3>
		<Comments />
	</div>
	</div>
	);
	}
});

var CommentForm = React.createClass({
	render: function(){
		return(
		<div className="col-lg-12 mrg">
		<h3 className="ui dividing header">Add comment</h3>
			<form className="ui reply form">
    			<div className="field">
      				<textarea></textarea>
    			</div>
    			<div className="ui blue labeled submit icon button">
      				<i className="icon edit"></i> Add Reply
    			</div>
			</form>
		</div>
		);
	}
});

var CommentBox = React.createClass({
	render: function(){
	return(
	<div className="readiv">
		<CommentList />
		<CommentForm />
	</div>
	);
	}
});

var SinglePost = React.createClass({
	function() {console.log('A');},
	render: function(){
		return(
			<div>1
			</div>
		);
	}
});

var SinglePostBox = React.createClass({
	render: function(){
	return(
		<div className="readiv">
			<SinglePost />
			<CommentBox />
		</div>
	);
	}
});

var NewsApp = React.createClass({
	render: function(){
	return(
		<div className="readiv">
			<RouteHandler/>
		</div>
	);
	}
}); 

var routes = (
  <Route path="/" handler={NewsApp}>
  	<DefaultRoute name="base" handler={NewsList}/>
    <Route name="id" path=":id" handler={SinglePostBox}/>
  </Route>
);

ReactRouter.run(routes, ReactRouter.HashLocation, function (Root) {
  React.render(<Root/>, document.getElementById('content'));
});

