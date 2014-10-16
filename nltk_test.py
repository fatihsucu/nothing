import unirest



class Routes(object):
    data = None
    """docstring for Routes"""
    def __init__(self):
        super(Routes, self).__init__()        
        self.end = "yalova"
        self.start = "bursa"
        if not self.data:
            self.data = self.make_request(self.end, self.start)
    
    def make_request(self, end, start):
        response = unirest.get("https://montanaflynn-mapit.p.mashape.com/directions?ending={}&starting={}".format(self.end,self.start),
            headers={"X-Mashape-Key": "qD3iWvWhE6mshvyXTW5QGdvIGd8Kp1VFEUwjsnhuFeUCLoTvHm"}
            )
        return response.body

    def get_directions_data(self):        
        for d in self.data["directions"]:
            yield d


    def get_directions(self):
        for direction in self.data["directions"]:
            yield direction["direction"].encode('utf8')

    def get_distance(self):
        return self.data["distance"]

    def get_duration(self):
        return self.data["duration"]

    def alert_maneuver(self, direction):
        try:           
            if not direction["maneuver"]:
                return "Continue"
            else:
                return direction["maneuver"]

        except:
            return "Continue"
