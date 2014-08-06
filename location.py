#!/usr/bin/env python

import web
import json

urls = ('/location','Location')

app = web.application(urls,globals())

json_file = 'shape.json'
with open(json_file) as json_data:
    shapes = json.load(json_data)
    json_data.close()

class Location:
 
    def __init__(self):
        self.hello = "hello world"
 
    def GET(self):
        return self.hello

    def POST(self):
        try:
            data = web.data()
            # print data

            request = json.loads(data)

            # serving_cell = request["serving cell"]["cell"]
            ta = request["serving cell"]["ta"]

            print ta

            ta = int(ta);

            if ta > 30 :
                raise LookupError

            return json.dumps(shapes[str(ta % 10 + 1)], sort_keys=True)
            
        except LookupError:
            return web.notfound("Sorry, the location was not found.")
        except:
            return web.badrequest();
    
##        print json.dumps(request["serving cell"])
##        print json.dumps(request["serving cell"]["ta"])
##        ta = int(json.dumps(request["serving cell"]["ta"])
        
 
if __name__ == "__main__":
        app.run()
