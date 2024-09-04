import requests

## Functions
def getProcessId(reactorNumber, url):
    auth = ("Lexi", "Lexi")
    response = requests.get(url+'processes?running=true&reactorIds='+str(reactorNumber), auth=auth)
    r = response.json()
    return r['data'][0]['id']

def set_setpoint(reactorNumber, controlLoopNumber, flowRateSpt):
    # base url
    url = 'http://192.168.15.85:8080/lpims/rest/v1/'
    # username and password
    auth = ("Lexi", "Lexi")

    # get process id of running process on specific bioreactor
    processID = getProcessId(reactorNumber, url)

    # creat dict for different control loop setpoints
    cl_dict = {
        1: 'CL1_Flow_Cont',
        2: 'CL2_Flow_Cont',
        3: 'CL3_Flow_Cont',
        4: 'CL4_Flow_Cont'
    }

    # get signal ID
    response = requests.get(url+'signals?processId='+str(processID), auth=auth)
    r = response.json()
    r2 = r['data']
    for r3 in r2:
        # find the signal that is a flow rate setpoint and is in the correct control loop
        if r3['port']['name'] == 'FlowRateSpt' and r3['device']['name'] == cl_dict[controlLoopNumber]:
            signalId = r3['id']

    # write new setpoint
    signalUrl = url + 'signals/' + str(signalId)
    response = requests.put(signalUrl, json={"currentValue": flowRateSpt}, auth=auth)
    if response.status_code == 200:
        print('Control Loop Setpoint ' + str(controlLoopNumber) + ' set to ' + str(flowRateSpt))