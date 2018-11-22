from tornado.web import RequestHandler
import http_base_handler


class AuthLoginHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        uid = self.get_argument('uid', '')
        if uid:
            token = 'THESE IS A FAKE TOKEN'
            self.set_secure_cookie(self.COOKIE_NAME, uid + ':' + token)
            self.write_success_dict({})
        else:
            self.write_error_parameter(['uid'])


class AuthLogoutHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST']

    def post(self, *args, **kwargs):
        if self.current_user:
            self.clear_all_cookies()
            self.write_success_dict({})
        else:
            self.write_code_layer_error(403, 'Error: unvalue login')
