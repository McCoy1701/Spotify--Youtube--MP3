import os
import json
from dotenv import load_dotenv
from googleapiclient import discovery


load_dotenv()


def main():
    results = searchYoutube('Coop Go Go')
    print(results)


def searchYoutube(query) -> list:
    apiKey = os.getenv("API_KEY") 
    youtube = discovery.build('youtube', 'v3', developerKey=apiKey)

    request = youtube.search().list(q=query, part='snippet', type='video')
    res = request.execute()

    searchList = []
    for i in res["items"]:
        searchList.append([i["snippet"]["title"] + ", " + i["snippet"]["channelTitle"] + ", " + i["id"]["videoId"]])
    
    return searchList
        

def saveToFile(list, filename):
    output= json.dumps(list, indent=4)
    with open(filename, "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()

