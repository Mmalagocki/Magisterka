from client import RestClient
import json
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("216832@edu.p.lodz.pl", "d6d724224f05d4bf")
post_data = dict()
# You can set only one task at a time
post_data[len(post_data)] = dict(
    target="itoscop.com"
)
# POST /v3/traffic_analytics/similarweb/live
response = client.post("/v3/traffic_analytics/similarweb/live", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    with open('phishing_example_data.json', 'w') as f:
        json.dump(response, f)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
