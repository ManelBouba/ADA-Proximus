from serpapi import GoogleSearch
# pip install serpapi, google-search-results
import csv

def search_google(query, api_key, num_results=50):
    results = []
    search = GoogleSearch({"q": query, "api_key": api_key, "num": 10})  # Adjust `num` for the number of results per page
    page = search.get_dict()
    
    while len(results) < num_results and page:
        # organic results are the little cards that appear in the search
        if "organic_results" in page:
            results.extend(page["organic_results"])  # Collect all fields in each organic result

        # Check if there's a next page link
        next_page = page.get("serpapi_pagination", {}).get("next")
        if next_page:
            search.params_dict.update({"start": len(results)}) 
            page = search.get_dict()
        else:
            break  # Exit loop if no more pages

    return results[:num_results]

def save_csv(data, filename):
    keys = ["title", "link", "snippet"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys, extrasaction='ignore')  # Ignore missing fields dynamically
        writer.writeheader()
        for item in data:
            for item in data:
                writer.writerow(item)
            

if __name__ == "__main__":
    # That's my api key, i dont have any problem sharing it but requests are limited
    API_KEY = "6f29f95576e46f9583a2c167383938bcd2ef216bdde76e7ef2d8a4006251ae06"

    # this query should, its the example i took so i could get emails too
    QUERY = 'site:linkedin.com/in/ "proximus" "manager" @gmail.com'
    NUM_RESULTS = 50

    print(f"Searching for '{QUERY}'...")
    search_results = search_google(QUERY, API_KEY, NUM_RESULTS)

    if search_results:
        print(f"Found {len(search_results)} results. Saving to CSV...")
        save_csv(search_results, "linkedin_proximus.csv")
        print("Results saved to 'linkedin_proximus.csv'")
    else:
        print("No results found.")
