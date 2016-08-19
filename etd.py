import requests
import lxml.html
import pprint

def parse_pos(str):
    # input data should look like:
    # 78°,NE
    s = str.split(',')
    # remove the degree symbol
    s[0] = s[0][:-1]
    return s

url = "http://var2.astro.cz/ETD/predictions.php"
lat = 39.002792 #delka
long = 283.043959 #sirka

form_data = {
    'delka': lat,
    'sirka': long,
    'midnight': 2457616.5,
}

#response = requests.post(url, data=form_data)

# testing only
f = open("example.html", 'r')
response = f.read()
#############

tree = lxml.html.fromstring(response)

targetlist = []

for table in tree.xpath('//table//table')[1:2]:
    for row in table.xpath('.//tr')[1:]:
        if row.__len__() == 1:
            continue
        elements = row.xpath('.//td//text()')

        # By now we should have the row from ETD, which consists of the following columns
        # 0: Name of target star
        # 1: Constellation
        # 2: Time of transit beginning
        # 3: Position of transit beginning (alt in degrees, az in rough compass heading)
        # 4: Timestamp of center of transit (date, month, time)
        # 5: Position of transit center
        # 6: Time of transit end
        # 7: Position of transit end
        # 8: Duration of transit in minutes
        # 9: Magnitude of star
        # 10: Depth of transit (chagne in magnitude)
        # 11: Elements
        # 12: RA
        # 13: Declination

        entry = dict()
        entry['name'] = elements[0]
        entry['const'] = elements[1]
        entry['time_begin'] = elements[2]
        
        tmp = parse_pos(elements[3])
        entry['alt_begin'] = tmp[0]
        entry['az_begin'] = tmp[1]

        # TODO: parse this better
        entry['ts_center'] = elements[4]
        
        tmp = parse_pos(elements[5])
        entry['alt_center'] = tmp[0]
        entry['az_center'] = tmp[1]

        entry['time_end'] = elements[6]

        tmp = parse_pos(elements[7])
        entry['alt_end'] = tmp[0]
        entry['az_end'] = tmp[1]

        entry['duration'] = elements[8]
        entry['mag'] = elements[9]
        entry['depth'] = elements[10]
        entry['elements'] = elements[11]
        entry['ra'] = elements[12][4:]
        entry['dec'] = elements[13][4:]

        targetlist.append(entry)

pp = pprint.PrettyPrinter()
for i in targetlist:
    pp.pprint(i)
    print('\n')

