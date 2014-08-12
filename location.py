#!/usr/bin/env python

import web
import json
import hashlib

urls = ('/location','Location')

app = web.application(urls,globals())

# json_file = 'shape.json'
json_file = 'locationResponse.json'

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

            # print data
            request = json.loads(data)

            decode_request = json.dumps(request, sort_keys=True, indent=4)
            # print decode_request

            hash_value = hashlib.new('md5', decode_request).hexdigest()
            # print hash_value

            return json.dumps(shapes[hash_value], sort_keys=True, indent=4)

            # serving_cell = request["serving cell"]["cell"]
            # ta = int(request["serving cell"]["ta"])
            #
            # print ta
            #
            # if ta > 30 :
            #     raise LookupError
            #
            # return json.dumps(shapes[str(ta % 10 + 1)], sort_keys=True)
            
        except LookupError:
            return web.notfound("Sorry, the location was not found.")
        except:
            return web.badrequest();
        
 
if __name__ == "__main__":
        app.run()
