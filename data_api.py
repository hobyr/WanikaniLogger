import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

class WanikaniAPIData():
    """
    Stores Wanikani API data and methods to retrieve various data from API.
    """
    def __init__(self, api_token):
        self.url = 'https://api.wanikani.com/v2/'
        self.api_token = api_token
        self.headers = {'Authorization': 'Bearer ' + self.api_token}

    def retrieve_data(self, api_endpoint_path):
        """
        Get data from the WaniKani V2 API.

        api_endpoint_path: Endpoint path that specifies data to retrieve (e.g. level progressions, user)
        """
        # The JSON response from the WaniKani API
        response = []
        res = requests.get(self.url + api_endpoint_path, headers=self.headers).json()
        next_url = res['pages']['next_url']
        response.append(res)
        while next_url:
            res = requests.get(next_url, headers=self.headers).json()
            response.append(res)
            next_url = res['pages']['next_url']
        # Save data into JSON file
        filename = api_endpoint_path + '.json'
        with open(filename, 'w') as file:
            json.dump(response, file)
        # Return data
        return response

    def import_data(self, api_endpoint):
        """
        Import the data from the filename acc. to the api_endpoint into a variable.
        """
        # Get the filename
        filename = api_endpoint + '.json'
        # Ensure filename exists in the folder

        # Load contents from filename
        with open(filename, 'r') as file:
            data = json.load(file)
        return data


def calculate_diff(start, end):
    start_iso = datetime.fromisoformat(start[:-1])
    if end == None:
        end_iso = datetime.now()
    else:
        end_iso = datetime.fromisoformat(end[:-1])
        
    # Calculate the difference
    diff_iso = end_iso - start_iso
    # Return difference (type float) in an object attribute
    return diff_iso.days + diff_iso.seconds/86400


def mean(arr):
    return sum(arr)/len(arr)


if __name__ == "__main__":
    # Get data either from API or from file
    api_token = '<your_API_key>'
    wkd = WanikaniAPIData(api_token)
    data = wkd.import_data('level_progressions')
    
    levels = []
    differences = []
    for level_data in data[0]['data']:
    
        # Store important level info in vars
        level = level_data['data']['level']
        start = level_data['data']['started_at']
        end = level_data['data']['passed_at']
        diff = calculate_diff(start, end)

        # Store values into arrays
        levels.append(level)
        differences.append(diff)
    

    avg = mean(differences)

    # Making the graph
    fig, ax = plt.subplots(figsize=(17,8))
    
    ax.bar(levels, differences)
    ax.plot([0, len(levels)+1], [avg, avg], color='#F96D6D')
    ax.set_title("Duration in days from start to completion of a WaniKani level")
    ax.set_xlabel("Level")
    ax.set_ylabel("Duration (days)")
    ax.set_xlim([0, len(levels)+1])
    ax.set_xticks(list(range(1, len(levels)+1)))
    ax.set_ylim([0, 50])
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    ax.legend([f"Average ({avg:.2f} days)", "Duration"])
    plt.show()
