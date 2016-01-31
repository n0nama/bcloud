/*global React*/
var Route = ReactRouter.Route;
var DefaultRoute = ReactRouter.DefaultRoute;
var RouteHandler = ReactRouter.RouteHandler;
var Link = ReactRouter.Link;
var IntlMixin     = ReactIntl.IntlMixin;
var FormattedDate = ReactIntl.FormattedDate;
var FormattedRelative = ReactIntl.FormattedRelative;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

var Gallery = React.createClass({
    render: function(){
        var images = this.props.images.map(function(img){
            return (
                <li key={img.id + 1}>
                    <img key={img.id} src={img.att} className="ui fluid image"></img>
                </li>
            );
        });
        return(
            <ul id="gallery">{images}</ul>
            );
    }
});

var Portfolio = React.createClass({
    showPreview: function(e) {
        var id = '#' + this.props.data.id;
	    $(id).modal({
	        onShow: function(){
	            $('#gallery').lightSlider({gallery: true});
	        }
	    }).modal('show');
  	},
    render: function(){
        return(
            <div key={this.props.data.id + 1} className="ui grid vertical segment">
              <div className="three wide column">
              { this.props.data.attach[0] ? (
                <img className="ui rounded image" src={this.props.data.attach[0].att} onClick={this.showPreview}></img>
                ) : (
                null
                )
              }
              </div>
              <div className="ten wide column">
                  <h3 className="ui header"><b>{this.props.data.title}</b></h3>
                  <p>{this.props.data.description}</p>
              </div>
              <div id={this.props.data.id} className="ui fullscreen modal">
                    <Gallery images={this.props.data.attach} />
              </div>
            </div>
        );
    }
});

var PortfolioForm = React.createClass({
    save: function(e){
        e.preventDefault();
        $('#pform').form({
            on: 'submit',
            inline: true,
            fields: {
                title: {
                    identifier: 'title',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                description: {
                    identifier: 'description',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
            }
        });
        if ( $('#pform').form('is valid') ) {
            var user = this.props.profile.user;
		    var title = React.findDOMNode(this.refs.title).value.trim();
		    var description = React.findDOMNode(this.refs.description).value.trim();
		    var link = React.findDOMNode(this.refs.link).value.trim();
		
		    var files  = this.refs.file.getDOMNode().files;
		    var data = new FormData();
		    data.append('user', user);
		    data.append('title', title);
		    data.append('description', description);
		    data.append('link', link);
		    if ( files.length != 0 )
		        for(var i=0;i<files.length;i++){
                    data.append("file" + i,files[i]); 
                    }
        
    	    this.props.portfolioSave(data);
    	    return;
        };
	},
    render: function(){
        return (
            <form id="pform" className="ui grid" onSubmit={this.save} encType="multipart/form-data">
                <div className="six wide center aligned column">
                    <div className="ui basic big icon button pfu">
                        <i className="upload icon">
                            <input ref="file" type="file" multiple></input>
                        </i>
                    </div>
                    <p><small>Файлы .jpg, .jpeg, .png</small></p>
                </div>
                <div className="seven wide column">
                    <div className="ui form">
                        <div className="required field">
                            <label>Заголовок:</label>
                            <input name="title" type="text" ref="title"></input>
                        </div>
                        <div className="required field">
                            <label>Описание:</label>
                            <textarea name="description" ref="description"></textarea>
                        </div>
                        <div className="field">
                            <label>Ссылка на сайт:</label>
                            <input type="text" ref="link"></input>
                        </div>
                        <button className="ui right floated blue button" type="submit">Сохранить</button>
                    </div>
                </div>
            </form>
            );
    }        
});

var ProfileInfo = React.createClass({
    edit: function(){
	    this.props.editStart();
	}, 
    render: function(){
        var age = calculateAge(this.props.profile.bd_month, this.props.profile.bd_day, this.props.profile.bd_year);
  	    var rate = this.props.profile.rate * 100;
  	    if (rate > 0) {
  	        $('#user_progress').progress({percent: rate});
  	    };
        var skills = this.props.skills.map(function (skills) {
  	        return(
  	            <a key={skills.id} className="ui label">
                    {skills.tags}
                </a>
  	            )
  	    });
        return (
                <div>
			     { !this.props.profile.filled ? 
			         (
			     <div>
			         <div className="row">
			            <h2 className="ui left floated header">
                           Ваш профиль совсем пустой!<br></br>Любая активность недоступна.<br></br>Пожалуйста, заполните его.
                        </h2>
                        <button className="mini ui black basic icon button right floated" onClick={this.edit}>
                            <i className="write icon"></i>
                        </button>
                      </div>
			     </div>
			         ):(
			     <div>
			         <div className="row">
			            <h2 className="ui left floated header">
                           {this.props.profile.f_name} {this.props.profile.l_name}
                           <a className="ui green empty circular label"></a>
                               <div className="sub header">{age}, {this.props.profile.spec}, {this.props.profile.city}</div>
                        </h2>
                        <button className="mini ui black basic icon button right floated" onClick={this.edit}>
                            <i className="write icon"></i>
                        </button>
                      </div>
                      <div className="ui green small labels">{skills}</div>
                          { this.props.profile.company ? (<div className="mrg"><b>Компания: </b>{this.props.profile.company}</div>):null}
			              { this.props.profile.website ? (<div className="mrg"><b>Сайт: </b><a href={this.props.profile.website} target="_blank">{this.props.profile.website}</a></div>):null}
                      <div className="row">
			             <div className="ui divider"></div>
                            <p>{this.props.profile.about}</p>
			          </div>
			     </div>
			          )}
			     </div>
            );
    }
    
});

var ProfileForm = React.createClass({
    validate : function(e){
        e.preventDefault();
        $('#proform').submit(function (e){
            e.preventDefault();
            return true;
        });
        if ( $('#proform').form('is valid') ) {
            this.save(e);
        }
    },
    save: function(e){
        e.preventDefault();
        if ( !this.props.profile.filled) {
            var filled = true
            var rate = 0.5
        }
        var user = this.props.profile.user.id;
		var f_name = React.findDOMNode(this.refs.f_name).value.trim();
		var l_name = React.findDOMNode(this.refs.l_name).value.trim();
		var bd_day = React.findDOMNode(this.refs.bd_day).value.trim();
		var bd_month= React.findDOMNode(this.refs.bd_month).value.trim();
		var bd_year = React.findDOMNode(this.refs.bd_year).value.trim();
		var spec = React.findDOMNode(this.refs.spec).value.trim();
		var sk = React.findDOMNode(this.refs.skills);
		var result = [];
		var options = sk && sk.options;
		var opt;
		for (var i=0, iLen=options.length; i<iLen; i++) {
            opt = options[i];

            if (opt.selected) {
                result.push(parseInt(opt.value.trim()));
                }
            };
        var skills = result;//.join('');
		var about = React.findDOMNode(this.refs.about).value.trim();
		var city = React.findDOMNode(this.refs.city).value.trim();
		var company = React.findDOMNode(this.refs.company).value.trim();
		var website = React.findDOMNode(this.refs.website).value.trim();
    	this.props.editSave(
    	    {
    	        user_id: user,
    	        f_name:f_name,
    	        l_name: l_name,
    	        bd_day: bd_day,
    	        bd_month: bd_month,
    	        bd_year: bd_year,
    	        skills: skills,
    	        spec: spec,
    	        about: about,
    	        city: city,
    	        company: company,
    	        website: website,
    	        filled: filled,
    	        rate: rate
    	    }
    	    );
    	    $('#profSave').toggleClass('loading');
    	return;
	},
	componentDidMount: function() {
	    $('#month_select').dropdown();
	    $('#sk_sel').dropdown('restore defaults');
	    $('#proform').form({
            on: 'submit',
            inline: true,
            fields: {
                f_name: {
                    identifier: 'f_name',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                l_name: {
                    identifier: 'l_name',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                bd_day: {
                    identifier: 'bd_day',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                bd_month: {
                    identifier: 'bd_month',
                    rules: [
                        {
                            type   : 'minCount[1]',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                bd_year: {
                    identifier: 'bd_year',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                spec: {
                    identifier: 'spec',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                city: {
                    identifier: 'city',
                    rules: [
                        {
                            type   : 'empty',
                            prompt : 'Это поле обязательно'
                        }
                    ]
                },
                skills: {
                    identifier: 'skills',
                    rules: [
                        {
                            type   : 'minCount[2]',
                            prompt : 'Пожалуйста, выберите не менее 2 и не более 5 навыков'
                        },
                        {
                            type   : 'maxCount[5]',
                            prompt : 'Пожалуйста, выберите не менее 2, но не более 5 навыков'
                        }
                    ]
                },
            }
        });
	},
    render: function(){
        var sid = [];
        var sids = "";
        var selected = this.props.profile.skills.map(function(s){
            sid.push(s.id);
        });
        
        var skills = this.props.all_skills.map(function(sk){
            return(<option key={sk.id} value={sk.id}>{sk.tags}</option>);
        });
        return (
            <div className="ui grid">
            <form id="proform" className="fourteen wide column ui form">
                <div className="required field">
                    <label>Имя:</label>
                    <div className="two fields">
                        <div className="field">
                            <input type="text" ref="f_name" name="f_name" placeholder="Имя" defaultValue={this.props.profile.f_name}></input>
                        </div>
                        <div className="field">
                            <input type="text" ref="l_name" name="l_name" placeholder="Фамилия" defaultValue={this.props.profile.l_name}></input>
                        </div>
                    </div>
                </div>
                <div className="required field">
                    <label>Дата рождения:</label>
                    <div className="three fields">
                        <div className="field">
                            <input type="text" ref="bd_day" name="bd_day" placeholder="День" defaultValue={this.props.profile.bd_day}></input>
                        </div>
                        <div className="field">
                            <select name="bd_month" ref="bd_month" id="month_select" className="ui fluid dropdown">
                                <option value={this.props.profile.bd_month}>Месяц</option>
                                <option value="01">Январь</option>
                                <option value="02">Февраль</option>
                                <option value="03">Март</option>
                                <option value="04">Апрель</option>
                                <option value="05">Май</option>
                                <option value="06">Июнь</option>
                                <option value="07">Июль</option>
                                <option value="08">Август</option>
                                <option value="09">Сентабрь</option>
                                <option value="10">Октябрь</option>
                                <option value="11">Ноябрь</option>
                                <option value="12">Декабрь</option>
                            </select>
                        </div>
                        <div className="field">
                            <input type="text" name="bd_year" ref="bd_year" placeholder="Год" defaultValue={this.props.profile.bd_year}></input>
                        </div>
                    </div>
                </div>
                <div className="two fields">
                    <div className="required field">
                        <label>Специализация:</label>
                        <input type="text" name="spec" ref="spec" placeholder="Например, Дизайнер..." defaultValue={this.props.profile.spec}></input>
                    </div>
                    <div className="required field">
                        <label>Город:</label>
                        <input type="text" name="city" ref="city" placeholder="" defaultValue={this.props.profile.city}></input>
                    </div>
                </div>
                <div className="required field">
                    <label>Навыки:</label>
                    <select id="sk_sel" name="skills" ref="skills" multiple={true} defaultValue={sid}>
                        {skills}
                    </select>
                </div>
                <div className="two fields">
                    <div className="field">
                        <label>Компания:</label>
                        <input type="text" ref="company" placeholder="" defaultValue={this.props.profile.company}></input>
                    </div>
                    <div className="field">
                        <label>Сайт:</label>
                        <input type="text" ref="website" placeholder="example.com" defaultValue={this.props.profile.website}></input>
                    </div>
                </div>
                <div className="field">
                    <label>О себе: </label>
                    <textarea defaultValue={this.props.profile.about} ref="about"></textarea>
                </div>
            </form>
            <div className="two wide column">
            <button id="profSave" className="mini ui green icon button right floated" onClick={this.validate}>
                <i className="check icon"></i>
            </button>
            </div>
            </div>
            )
    }
});

var AvatarForm = React.createClass({
    save:function(e){
        e.preventDefault;
        var avatar = React.findDOMNode(this.refs.avatar).value.trim();
        this.props.avatarSave({
              avatar : avatar
        });
        $('#avaSave').toggleClass('loading');
        return;
    },
    componentDidMount: function() {
        var curr_ava = this.props.avatar;
        console.log(curr_ava);
        $('#cropper_box').cropit({ imageState: { src: curr_ava} });
        $('#select_ava').click(function() {
            $('#cropped').click();
        });
        $('#avaSave').click(function() {
          var imageData = $('#cropper_box').cropit('export');
          $('#cro').val(imageData);
        });
    },
    render: function() {
    return (
        <div>
            <div id="cropper_box">
                <div id="crop_preview" className="cropit-image-preview"></div>
                <input id="zoom_range" type="range" className="cropit-image-zoom-input"/>
                <button id="select_ava" className="ui primary fluid button">Загрузить</button>
                <input id="cropped" type="file" className="cropit-image-input"/>
                <input id="cro" ref="avatar" type="hidden" className="cropit-image-input"/>
            </div>
			<button id="avaSave" className="mini ui green icon button rght" onClick={this.save}>
                <i className="check icon"></i>
            </button>
        </div>
    );
  },
});

var Profile = React.createClass({
	mixins: [IntlMixin],
	editStart: function(){
	    this.setState({profile_edit:true});
	},
	avatarEdit: function(){
	    this.setState({avatar_edit:true});
	},
	avatarSave: function(ava){
	    $.ajax({
      		url: '/profile',
      		type: 'PATCH',
      		dataType: 'json',
      		traditional: true,
      		data: ava,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
  			cache: false,
      		success: function(data) {
        		this.setState({profile: data, skills: data.skills, avatar_edit:false});
        		var a = $('#big_avatar').attr('src');
        		$('#mini_avatar').attr('src', a);
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/profile', status, err.toString());
      		}.bind(this)
   	 	});
	    //this.setState({avatar_edit:false});
	},
	editSave: function(profile){
	    $.ajax({
      		url: '/profile',
      		type: 'PUT',
      		dataType: 'json',
      		traditional: true,
      		data: profile,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
  			cache: false,
      		success: function(data) {
        		this.setState({profile: data, skills: data.skills, profile_edit:false});
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/profile', status, err.toString());
      		}.bind(this)
   	 	});
	    //this.setState({profile_edit:false});
	},
	portfolioSave: function(portfolio){
	    $.ajax({
      		url: '/portfolio',
      		type: 'POST',
      		//dataType: 'json',
      		data: portfolio,
      		processData: false,
            contentType: false,
      		file: portfolio.file,
			headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
  			cache: false,
      		success: function(data) {
        		this.setState({portfolio: data});
        		$("#pform").hide();
        		$('#port_new_add').show();
      		}.bind(this),
      		error: function(xhr, status, err) {
        		console.error('/profile', status, err.toString());
      		}.bind(this)
   	 	});
	},
	getInitialState: function() {
    	return {profile: [], skills:[], portfolio:[], all_skills:[], profile_edit:false, avatar_edit: false};
  	},
	componentDidMount: function() {
	$.ajax({
	  type: 'GET',
      url: '/profile',
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({profile: data.profile, skills: data.profile.skills, portfolio:data.portfolio, all_skills:data.all_skills});
        $('#pform').hide();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('/profile', status, err.toString());
      }.bind(this)
    });
    $('#port_new_add').click(function() {
        $('input[name="title"]').val('');
        $('textarea[name="description"]').val('');
        $('#emp_port').hide();
        $('#port_new_add').hide();
        $('#pform').show();
    });
  },
  	render: function() {
        if (this.state.portfolio.length > 0){
            var port = this.state.portfolio.map(function(p){
                return(
                    <Portfolio data={p} />
                );
            });
        } else {
                port = <h2 id="emp_port" className="ui center aligned grey header">Здесь пока пусто...</h2>
        };
		return (
			<div className="col-lg-12 mrg">
			    <div className="ui raised segment">
			        <div id="user_progress" className="ui top attached green progress">
                        <div className="bar"></div>
                    </div>
			        <div className="ui grid">
			                <div className="six wide column">
			                    <div className="row">
			                    { !this.state.avatar_edit ? (
			                        <div>
			                        <img id="big_avatar" className="ui medium rounded left floated image" src={this.state.profile.avatar}></img>
			                        <button className="mini ui black basic icon button rght" onClick={this.avatarEdit}>
                                        <i className="photo icon"></i>
                                    </button>
                                    </div>
                                    ) : (
                                        <AvatarForm avatar={this.state.profile.avatar} skills={this.state.skills} avatarSave={this.avatarSave} />
                                    ) }
                                </div>
			                </div>
			                <div className="ten wide column">
			                { !this.state.profile_edit ? (
			                    <ProfileInfo profile={this.state.profile} skills={this.state.skills} editStart={this.editStart} />
			                    ) : (
			                    <ProfileForm profile={this.state.profile} skills={this.state.skills} all_skills={this.state.all_skills} editSave={this.editSave}/>   
                            ) }
			                </div>
			            <div className="sixteen wide column">
			                <h2 className="ui horizontal divider header">
                                <b>ПОРТФОЛИО</b>
                            </h2>
                            {port}
                            <div className="ui grid">
                                <div className="sixteen wide center aligned column">
                                    <button id="port_new_add" className="ui primary button">Добавить</button>
                                </div>
                            </div>
                            <PortfolioForm profile={this.state.profile} portfolioSave={this.portfolioSave}/>
			            </div>
			        </div>
			    </div>
			</div>
		);
	}
});

var UserApp = React.createClass({
	render: function(){
	return(
		<div className="readiv">
			<RouteHandler locales={['ru-RU']}/>
		</div>
	);
	}
}); 

var routes = (
  <Route path="/profile" handler={UserApp}>
  	<DefaultRoute name="base" handler={Profile}/>

  </Route>
);

ReactRouter.run(routes, ReactRouter.HistoryLocation, function (Root) {
  React.render(<Root/>, document.getElementById('content'));
});