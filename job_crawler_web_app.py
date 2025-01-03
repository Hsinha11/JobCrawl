# import requests
# from bs4 import BeautifulSoup
# import streamlit as st # type: ignore

# def fetch_job_links(query, num_pages=1):
#     links = []
#     for page in range(num_pages):
#         url = f"https://www.google.com/search?q={query}&start={page * 10}"
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers)
        
#         soup = BeautifulSoup(response.text, "html.parser")
#         for item in soup.select('h3'):
#             link = item.find_parent('a')['href']
#             # Check if link contains any of the desired ATS sites
#             if any(site in link for site in ats_sites) and link not in links:
#                 # Trim the link to get the clean URL
#                 clean_link = link.split('/url?q=')[-1].split('&')[0]
#                 links.append(clean_link)
    
#     return links

# # List of ATS sites to include in the search
# ats_sites = [
#     "jobs.lever.co",
#     "boards.greenhouse.io",
#     "hire.withgoogle.com",
#     "jobs.jobvite.com",
#     "workable.com",
#     "breezy.hr",
#     "applytojob.com"
# ]

# # Streamlit UI
# st.title("Job Link Fetcher")
# st.write("Enter your search query for job postings:")

# # Input box for search query
# query_input = st.text_input("Search Query", value="site:lever.co software engineer india")

# # Input box for number of pages
# num_pages_input = st.number_input("Number of Pages to Search", min_value=1, max_value=20, value=5)

# # Button to fetch job links
# if st.button("Fetch Job Links"):
#     if query_input:
#         with st.spinner("Fetching job links..."):
#             job_links = fetch_job_links(query_input, num_pages_input)
#             st.success(f"Fetched {len(job_links)} job links!")
            
#             # Display the links
#             for link in job_links:
#                 st.markdown(f"[{link}]({link})")
                
#             # # Save links to a file
#             # with open("job_link.txt", "w") as f:
#             #     for link in job_links:
#             #         f.write(link + "\n")
#             # st.success(f"Saved {len(job_links)} job links to job_link.txt")
#     else:
#         st.error("Please enter a valid search query.")


import requests
from bs4 import BeautifulSoup
import streamlit as st # type: ignore

def fetch_job_links(query, ats_sites, num_pages=1):
    links = []
    
    # Combine ATS sites into the query string
    ats_query = " OR ".join([f"site:{site}" for site in ats_sites])
    final_query = f"({ats_query}) {query}"
    
    for page in range(num_pages):
        url = f"https://www.google.com/search?q={final_query}&start={page * 10}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.select('a'):
            href = item.get('href')
            # Clean the Google search result URL
            if href and href.startswith('/url?q='):
                clean_link = href.split('/url?q=')[-1].split('&')[0]
                # Now, check if the cleaned link belongs to any ATS job boards
                if any(site in clean_link for site in ats_sites) and clean_link not in links:
                    # Filter out unwanted URLs (e.g., login or maps links)
                    if "accounts.google.com" not in clean_link and "maps.google.com" not in clean_link:
                        links.append(clean_link)
    
    return links

# List of ATS sites to include in the search
ats_sites = [
    "jobs.lever.co",
    "boards.greenhouse.io",
    "hire.withgoogle.com",
    "jobs.jobvite.com",
    "workable.com",
    "breezy.hr",
    "applytojob.com"
    "workdayjobs.com"
]

# Streamlit UI
st.title("Job Link Fetcher")
st.write("Enter your search query for job postings:")

# Input box for search query
query_input = st.text_input("Search Query", value="software engineer india")

# Input box for number of pages
num_pages_input = st.number_input("Number of Pages to Search", min_value=1, max_value=200, value=5)

# Button to fetch job links
if st.button("Fetch Job Links"):
    if query_input:
        with st.spinner("Fetching job links..."):
            job_links = fetch_job_links(query_input, ats_sites, num_pages_input)
            st.success(f"Fetched {len(job_links)} job links!")
            
            # Display the links
            for link in job_links:
                st.markdown(f"[{link}]({link})")
    else:
        st.error("Please enter a valid search query.")
