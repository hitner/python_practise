from qiniu import Auth


class QiniuTokenHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET']

    def get(self, *args, **kwargs):
        token = self.get_query_argument('session', '')
        if token:
            session = session_manager.session_from(token)
            if session:
                qiniu = create_qiniu_token(token)
                self.write_success_dict({'qiniuToken':qiniu})
            else:
                self.write_user_layer_error(1, 'session 失效')

        else:
            self.write_error_parameter(['session'])



qiniu_secret = ''

def create_qiniu_token(session):
    if not qiniu_secret:
        return ''
    access_key = 'dJlvugwyyPkue5JTTj02LBwTQrNphcrTRS9DToiP'
    bucket_name = 'importmusic'
    q = Auth(access_key, qiniu_secret)
    polic = {
        'fsizeLimit':20*1024*1024,
        'saveKey':session+'_$(fname)'
    }
    return q.upload_token(bucket_name, None, 7200, polic)