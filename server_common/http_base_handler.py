from tornado.web import RequestHandler, MissingArgumentError


class BaseHandler(RequestHandler):
    COOKIE_NAME = 'session'

    def get_current_user(self):
        session: str = self.get_secure_cookie(self.COOKIE_NAME)
        if session:
            sep = session.split('-', 1)
            return int(sep[0])

    def options(self, *args, **kwargs):
        if __debug__:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
            self.set_header('Access-Control-Allow-Methods', ', '.join(self.ALLOWED_METHODS))
            self.set_status(200)
            self.finish()
        else:
            self.reply405()

    def get(self, *args, **kwargs):
        self.reply405()

    def post(self, *args, **kwargs):
        self.reply405()

    def put(self, *args, **kwargs):
        self.reply405()

    def delete(self, *args, **kwargs):
        self.reply405()

    def patch(self, *args, **kwargs):
        self.reply405()

    def reply405(self):
        self.set_status(405)
        allow = ', '.join(self.ALLOWED_METHODS)
        self.add_header('Allow', allow)
        self.finish('Error: method not allowed, only for ' + allow)

    def write(self, chunk):
        if __debug__ and self.request.method != 'OPTIONS':
            origin = self.request.headers['Origin']
            if origin:
                self.add_header("Access-Control-Allow-Origin", origin)
        super(BaseHandler, self).write(chunk)

    def write_success_dict(self, data):

        self.write({'rcode': 0, 'data': data})

    def write_user_layer_error(self, rcode, describe):
        self.write({'rcode': rcode, 'describe': describe})

    def write_code_layer_error(self, rcode, describe):
        self.set_status(rcode)
        self.finish(describe)

    def write_bad_request(self, descibe):
        self.write_code_layer_error(400, descibe)

    def write_error_parameter(self, para):
        self.write_code_layer_error(400, 'Error: need para ' + ', '.join(para))

    def write_error_not_there(self):
        self.write_code_layer_error(430, "Error: not in room/env")

