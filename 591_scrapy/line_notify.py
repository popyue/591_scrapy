import requests

class LineNotify():
    link = "https://notify-api.line.me/api/"
    def __init__(self,token):
        self.token = token

    def notify(self,message):
        headers = {"Authorization": "Bearer %s" % self.token}
        data = {"message":message}
        r = requests.post(self.link+"notify",headers=headers,data=data)
    def stickernotify(self,package_id,stickerId):
        headers = {"Authorization": "Bearer %s" % self.token}
        data = {"stickerPackageId": package_id,"stickerId": stickerId}
        r = requests.post(self.link+"notify",headers=headers,data=data)

    def checkIsWork(self):
        headers = {"Authorization": "Bearer %s" % self.token}
        r = requests.get(self.link+"status",headers=headers)
        if r.json()["message"] == "ok":
            return r.json()
        return False
