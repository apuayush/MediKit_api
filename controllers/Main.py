from controllers.modules import *
from controllers import utility


class LoginHandler(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def post(self):

        data = json.loads(self.request.body.decode('utf-8'))
        docs = db.collection('user_data').where('uname', '==', data['uname']).get()
        docs = list(docs)[0].to_dict()
        if docs is None:
            self.write(json.dumps(dict(
                status='403',
                message='user not registered'
            ))
            )
        elif docs['password'] == data['password']:
            jwt_token = utility.set_token(docs)

            self.write(json.dumps(dict(
                status="200",
                message="login succesful",
                session_key=jwt_token
            )
            ))
        else:
            self.write(json.dumps(dict(
                status="403",
                message="invalid password"
            )
            ))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()


class LogoutHandler(RequestHandler):
    """
    method = POST
    route : /logout
    parameter : token
    """
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', ' POST, OPTIONS')

    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        # remove token
        try:
            db.collection('session').document(data['session_key']).delete()
        except:
            self.write_error(205, "Unsuccessful logout")
        self.write({"status": 200, "msg": "successful"})

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
