import sys
import io
import json
import hashlib

class LocationRequest(object):
    def __init__(self, msr):
        self.msr = msr

    def __repr__(self):
        serving_cell = '"serving cell" : { "cell" : "%s" , "ta" : "%s", "signal strength" : "%s" }' \
                       % (self.msr[0], self.msr[1], self.msr[2])
        # print serving_cell

        neighbor_cell_list = '"neighbor cell list" : ['
        for index in range(3, len(self.msr)):

            if index % 2 != 0:
                if 3 < index:
                    neighbor_cell_list += ','

                neighbor_cell_list += '{ "cell" : "%s"' % self.msr[index]
            else:
                neighbor_cell_list += ', "signal strength" : "%s"}' % self.msr[index]

        neighbor_cell_list += ']'

        # print neighbor_cell_list

        return '{' + serving_cell + ',' + neighbor_cell_list + '}'

class LocationResponse(object):
    def __init__(self, hash_string, shape):
        self.hash_string = hash_string
        self.shape = shape

    def __repr__(self):
        response = '"%s" : ' % self.hash_string
        response += '{"location" : {"latitude" : "%s", "longitude" : "%s", "uncertainty radius" : "%s"}}' \
        % (self.shape[0], self.shape[1], self.shape[2])
        return response

pFile = 'p.dat'
shapeFile = 'shape.dat'

requestFile = 'locationRequest.json'
responseFile = 'locationResponse.json'

# p_list = []
request_file = open(requestFile, 'w')

shape_list = []
with io.open(shapeFile) as shape_file:
    for line in shape_file:
        shape_data = []
        shape = line.split()

        latitude, longitude, radius  = '%f' % float(shape[0]), '%f' % float(shape[1]), '%f' % float(shape[2])
        shape_data.append(latitude)
        shape_data.append(longitude)
        shape_data.append(radius)
        # print shape_data
        shape_list.append(shape_data)
        # break

# sys.exit(0)

response_string = ''
index = 0
with io.open(pFile) as p_file:
    for line in p_file:
        p_data = []

        # print line
        p = line.split()
        # print p
        lac_ci = long(float(p[1]))
        lac = lac_ci // 65536
        ci = lac_ci % 65536
        # print lac_ci, lac, ci, lac*65536+ci

        # serving cell (cell, ta)
        # cell = lac-ci
        cell = '%d-%d' % (lac, ci)
        p_data.append(cell)
        # ta, signal strength
        ta, sig = '%d' % int(float(p[2])), '%d' % int(float(p[3]))
        p_data.append(ta)
        p_data.append(sig)

        # serving_cell = {"serving cell:"}
        for i in range(4, 16):
            data = long(float(p[i]))

            if data == -1:
                continue

            if i % 2 == 0:
                lac_ci = data
                lac = lac_ci // 65536
                ci = lac_ci % 65536
                cell = '%d-%d' % (lac, ci)
                p_data.append(cell)
            else:
                sig = str(data)
                p_data.append(sig)
        # print p_data
        # print cell
        # print p[1]
        # print p[2]
        # print p_data

        locationRequest = LocationRequest(p_data)
        # print repr(locationRequest)

        # construct the json object

        json_lr = json.loads(repr(locationRequest))

        location_request = json.dumps(json_lr, sort_keys=True, indent=4)

        # print location_request

        # print hashlib.new('md5', location_request).hexdigest()

        # assert isinstance(location_request, object)
        # print hash(location_request)
        request_file.write(location_request)
        request_file.write('\n\n\n')

        # response handle
        locationResponse = LocationResponse(hashlib.new('md5', location_request).hexdigest(), shape_list[index])
        # print locationResponse
        if len(response_string) > 0 :
            response_string += ','

        response_string += repr(locationResponse)

        index = index + 1
        # request_file.write(hashlib.new('md5', location_request).hexdigest())
        # request_file.write('\n\n\n')
        # break
        # p_list.append(p_data)
        # print p_list

    p_file.close()

    request_file.close()

    # print response_string

    response_file = open(responseFile, 'w')

    json_response = json.loads('{' + response_string + '}')

    response_file.write(json.dumps(json_response, sort_keys=True, indent=4))
    response_file.close()