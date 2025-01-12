"""
Check whether user's IP is likely from a VPN or not. (True/False)
Call using_vpn() to get this output.
Any incorrect IP data or errors simply return False.
"""

import requests

def get_user_ip():
    """
    Retrieve the user's public IP address using an external service.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            data = response.json()
            return data["ip"]  # return the public IP address
        else:
            print(f"Failed to get IP address. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None

def using_vpn():
    ip_address = get_user_ip()
    api_key = '67661z-4k9c06-2302d7-017030'
    url = f'https://proxycheck.io/v2/{ip_address}?key={api_key}&vpn=1'
    response = requests.get(url)
    if response.status_code == 200:  # if response was successful (code 200)
        data = response.json()
        # ProxyCheck.io returns a "proxy" field "yes" or "no"
        is_vpn = data.get(ip_address, {}).get('proxy', 'no') == 'yes'
        return is_vpn
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
