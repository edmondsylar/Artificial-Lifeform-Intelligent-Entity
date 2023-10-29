import google.generativeai as palm
import os

# Initialize the Google Palm2 API
google_api_key = "AIzaSyDn2fvOXSrPnm7hxCYQKwClE93hWfk8ch0"
palm.configure(api_key=google_api_key)

# Define the agent
def search_agent(user_query):
    # Perform a web search using Google Palm2
    google_search_result = palm.generate_text(
        model='models/text-bison-001',
        prompt=f"Search the internet for '{user_query}'",
        temperature=0.1
    )
    
    # Perform a Wikipedia search using Google Palm2
    wikipedia_search_result = palm.generate_text(
        model='models/text-bison-001',
        prompt=f"Search Wikipedia for '{user_query}'",
        temperature=0.1
    )
    
    # Process and format the search results
    # You can extract relevant information from both search results
    
    return {
        "Google Search Result": google_search_result.result,
        "Wikipedia Search Result": wikipedia_search_result.result
    }

# User input
user_query = "Artificial Intelligence"

# Call the agent with the user's query
results = search_agent(user_query)

# Print or display the results
print("Search Results:")
print("Google Search:")
print(results["Google Search Result"])
print("\nWikipedia Search:")
print(results["Wikipedia Search Result"])
