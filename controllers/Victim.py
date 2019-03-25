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
        t = datetime.now()
        time = t.strftime("%d-%m-%Y %I:%M %p")
        data['time'] = time
        # post on dashboard
        db.collection('session').document(str(now) + data['name']).set(data)
        # TODO - get similar description
        with open("controllers/secrets/descriptions.json") as f:
            desc_list = json.load(f)
            scored_list = process.extract(data['description'], desc_list, scorer=fuzz.token_sort_ratio,limit=10)
        # TODO - get similar cases
        relevant_responses = []
        cases = []
        for desc in scored_list:
            if desc[1] < 47:
                break
            relevant_responses.append(desc[0])
            doc = db.collection('emergency_history').where('description', '==', desc[0]).get()
            doc = list(doc)[0].to_dict()
            cases.append(doc)
        self.write(json.dumps({"status": 200,
                               "message":"successful",
                               "relevant_responses": relevant_responses,
                               "cases": cases}))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()

