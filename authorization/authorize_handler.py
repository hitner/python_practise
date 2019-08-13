from tornado.web import RequestHandler
import http_base_handler
import json


class AuthLoginHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        try:
            content = json.loads(self.request.body)
            uid = content['uid']
            password = content['password']
            if password == '123456':
                token = 'THESE IS A FAKE TOKEN'
                self.set_secure_cookie(self.COOKIE_NAME, f'{uid}:{token}')
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1,"password is not right")
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')
        except KeyError:
            self.write_error_parameter(['uid','password']) 



class AuthLogoutHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        if self.current_user:
            self.clear_all_cookies()
            self.write_success_dict({})
        else:
            self.write_code_layer_error(403, 'Error: unvalue login')
