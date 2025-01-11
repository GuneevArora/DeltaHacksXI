"""
Returns a list of ['Site', 'Date'] pairs of which the input email has been exposed in, using LeakCheck API.
* MAY NEED SOME WORK ON THE INPUT SYSTEM *
* NEEDS ERROR CHECKING FOR INCORRECT EMAILS & NO DATA LEAK EMAILS *
"""

from leakcheck import LeakCheckAPI_Public

def output_leaks(data):
    """Returns a list with [Leak Company, Date] pairs."""
    output = []
    for i in range (len(data['sources'])):
        output += [[data['sources'][i]['name'], data['sources'][i]['date']]]
    return output

def main():
    input_email = str(input("Email: "))  # input email for leaked data search

    public_api = LeakCheckAPI_Public()  # initialize without an API key
    api_data = public_api.lookup(query=input_email)  # perform a public lookup

    print(output_leaks(api_data))
    return output_leaks(api_data)

main()
