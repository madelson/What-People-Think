import os;

# gets template values to be populated across all pages
def get_template_values_common(answerer):
	values = {
		'answerer': answerer
	};
	return values;

# extracts a user id value for the request
def get_user_id(request):
	return str(request.remote_addr);
	
# finds a template for the given name
def template_path(name):
	path = os.path.join(os.path.dirname(__file__), name + '.html');
	return path;
	
def bad_request_error(handler, message):
	handler.error(404);
	handler.response.out.write(message);
	return None;