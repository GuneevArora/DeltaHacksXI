import streamlit as st
from pysafebrowsing import SafeBrowsing

def check_url_safety(url):
    s = SafeBrowsing(st.secrets["SAFE_BROWSING_API_KEY"], )
    r = s.lookup_urls([url])
    return r[url]


#check_url_safety("http://www.malware.testing.google.test/testing/malware/")  # test the function

#check_url_safety("http://testsafebrowsing.appspot.com/s/unwanted.html")  # test the function

#check_url_safety("www.google.com")  # test the function


