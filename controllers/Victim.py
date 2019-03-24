from controllers.modules import *

class VictimInfo(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        now = int(time.time())
        # post on dashboard
        db.collection('session').document(str(time)+name).set(data)
        # TODO - get similar description
        # TODO - get similar cases
        self.write("wassup")


