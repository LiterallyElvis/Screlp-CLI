import sys
import connect
import files

items = []


class Business:
    """
    Business object to store desired data.

    Ultimately collected into a list of like objects for later comprehension.
    """
    def __init__(self):
        self.result_position = 0
        self.id = None
        self.name = None
        self.address = None
        self.city = None
        self.state = None
        self.zip = 00000
        self.rating = 0
        self.review_count = 0
        self.category = None
        self.query_performed = None


def parse_results(api_result, items, url, args):
    """
    Takes JSON result from Yelp query and uses each individual result to
    populate a Business object. Appends business object to list of business
    objects for later manipulation.
    """
    for x in range(0, api_result["total"]):
        biz = Business()
        try:
            source = api_result["businesses"][x]
            biz.result_position = x+1
            biz.id = source["id"]
            biz.name = source["name"]
            if len(source["location"]["address"]) > 1:
                biz.address = source["location"]["address"][0]
                biz.address += ", " + source["location"]["address"][1]
            else:
                biz.address = source["location"]["display_address"][0]
            biz.city = source["location"]["city"]
            biz.state = source["location"]["state_code"]
            biz.zip = source["location"]["postal_code"]
            biz.rating = str(source["rating"])
            biz.review_count = str(source["review_count"])
            biz.category = source["categories"][0][0]
            url = url.replace("http://api.yelp.com/v2/search?", "")
            biz.query_performed = url
            item = [biz.result_position, biz.id, biz.name, biz.address,
                    biz.city, biz.state, biz.zip, biz.rating,
                    biz.review_count, biz.category, biz.query_performed]
            items.append(item)
        except IndexError:
            break
        except KeyError:
            try:
                if api_result["error"]:
                    print("Error(s) encountered, please see raw_output.txt!")
                    files.write_raw_result(api_result, args)
                    sys.exit(1)
            except:
                files.write_raw_result(api_result, args)
    return items


def scrape_yelp(args, coords):
    """
    Uses list of generated coordinates to:

        1) Generate an API query URL
        2) Visit that URL and retrieve results
        3) Parse the JSON received

    Then returns the parsed results as a list.
    """
    items = []
    for coord in coords:
        url = connect.make_url(args, coord)
        result = connect.make_api_call(url)
        items = parse_results(result, items, url, args)
    return items


def eliminate_duplicate_results(results):
    """
    Takes a list of results and removes entries which share
    a Yelp API business ID attribute with something already
    in the results list.
    """
    old = results
    results = []
    for item in old:
        if item in results:
            pass
        else:
            results.append(item)

    return results
