from controllers.modules import *

def set_token(user_data):
    """
    setting tokens and saving them on database
    :param user:
    :return:
    """
    now = datetime.now()
    time = now.strftime("%d-%m-%Y %I:%M %p")
    print(time)
    token = jwt.encode({"user_data": user_data, "time": time},
                       JWT_SECRET, JWT_ALGORITHM)
    db.collection('session').document(token.decode('utf-8')).set(user_data)

    return token.decode('utf-8')


def get_nearest_hospital(gps):
    k = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + gps + "&radius=5000&type=hospital&key=AIzaSyCXi_HCK6GfPiY2YiDH6KKUh979oBrcU54"
    req = requests.get(k).json()
    # print(req)
    nearest_hosp = req['results'][0]['geometry']['location']
    # print(nearest_hosp)
    return nearest_hosp

