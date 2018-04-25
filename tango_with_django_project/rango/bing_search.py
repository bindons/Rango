import requests
from IPython.display import HTML

def read_bing_key():
    subscription_key = None
    try:
        with open('bing.key','r') as f:
            subscription_key = f.readline()
    except:
        raise IOError('bing.key file not found')
    return subscription_key

def run_query(search_terms):
    subscription_key = read_bing_key()
    if not subscription_key:
        raise KeyError('Bing Key Not Found')

    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'

    #results_per_page = 10
    #offset = 0

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_terms, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    rows = "\n".join(["""<tr>
                       <td><a href=\"{0}\">{1}</a></td>
                       <td>{2}</td>
                     </tr>""".format(v["url"],v["name"],v["snippet"]) \
                  for v in search_results["webPages"]["value"]])

    HTML("<table>{0}</table>".format(rows))

    return rows

def main():
    print("Enter a query ")
    query = input()
    results = run_query(query)
    for result in results:
        print(result['title'])
        print('-'*len(result['title']))
        print(result['summary'])
        print(result['link'])
        print()

if __name__ == '__main__':
    main()