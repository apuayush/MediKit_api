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
        db.collection('session').document(str(time) + data['name']).set(data)
        # TODO - get similar description
        with open("controllers/secrets/descriptions.json") as f:
            desc_list = json.load(f)
            scored_list = process.extract(data['description'], desc_list, scorer=fuzz.token_sort_ratio,limit=10)
            # TODO - get similar cases
            print(scored_list)
        self.write(json.dumps({"message": "wassup"}))


