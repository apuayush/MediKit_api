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
        global current_id
        now = int(time.time())
        data['id'] =  current_id
        current_id += 1
        t = datetime.now()
        ti = t.strftime("%d-%m-%Y %I:%M %p")
        data['time'] = ti
        data['doc_response'] = ""
        # post on dashboard
        db.collection('patient_data').document(str(now) + data['name']).set(data)
        # TODO - get similar description
        with open("controllers/secrets/descriptions.json") as f:
            desc_list = json.load(f)
            scored_list = process.extract(data['description'], desc_list, scorer=fuzz.token_sort_ratio,limit=10)
        # TODO - get similar cases
        relevant_responses = []
        cases = []
        for desc in scored_list:
            if desc[1] < 27:
                break
            relevant_responses.append(desc[0])
            doc = db.collection('emergency_history').where('description', '==', desc[0]).get()
            doc = list(doc)[0].to_dict()
            cases.append(doc)
        self.write(json.dumps({"status": 200,
                               "id": current_id-1,
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


class DoctorResponse(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        t = datetime.now()
        ti = t.strftime("%d-%m-%Y %I:%M %p")
        # post on dashboard
        doc = db.collection('patient_data').where('id', '==', data['id']).get()
        doc_1 = list(doc)[0]
        doc_data = doc_1.to_dict()
        doc_id = doc_1.id
        doc_data['doc_response'] = data['doc_response']
        doc_data['doc_response_time'] = ti

        db.collection('patient_data').document(doc_id).set(doc_data)

        self.write(json.dumps({"status": 200,
                               "message": "successful"}))

    def write_error(self, status_code, message="Internal Server Error", **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': message
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()

