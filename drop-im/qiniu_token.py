from qiniu import Auth

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