from werkzeug.security import safe_str_cmp  # For comparing strings in a safe manner
from user import User

# Takes in a username and a password and will authenticate
def authenticate(username, password):
	user = User.find_by_username(username)
	if user and safe_str_cmp(user.password, password):
		return user

def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)

print("Hello world")