from react import jsx

# For multiple paths, use the JSXTransformer class.
#transformer = jsx.JSXTransformer()
#for jsx_path, js_path in my_paths:
#    transformer.transform(jsx_path, js_path=js_path)

# For a single file, you can use a shortcut method.
jsx.transform('/home/bcloud/preprod/bcloud/application/projects/projects.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/projects.js')
jsx.transform('/home/bcloud/preprod/bcloud/application/chat/chat.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/chat.js')
jsx.transform('/home/bcloud/preprod/bcloud/application/messages/messages.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/messages.js')
jsx.transform('/home/bcloud/preprod/bcloud/application/colleagues/colleagues.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/colleagues.js')
jsx.transform('/home/bcloud/preprod/bcloud/application/news/news.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/news.js')
jsx.transform('/home/bcloud/preprod/bcloud/application/user/user.jsx', js_path='/home/bcloud/preprod/bcloud/static/app/user.js')