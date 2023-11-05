import time

from advantech.Data import generateData
from advantech.Config import generateConfig
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions

def on_connected(edgeAgent, isConnected):
    print("connected !")

def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def edgeAgent_on_message(agent, messageReceivedEventArgs):
    print("edgeAgent_on_message !")

def generate_edgeAgent():
    dccsOptions = DCCSOptions(apiUrl = 'https://api-dccs-ensaas.sa.wise-paas.com/', 
                              credentialKey = 'e648181bbc03d2fef18014ef624fefe6')
    edgeAgentOptions = EdgeAgentOptions(nodeId = 'ed3a814a-53d0-4b48-97f8-7cbc9f393aac',
                                        connectType = constant.ConnectType['DCCS'],
                                        DCCS = dccsOptions)
    _edgeAgent = EdgeAgent(edgeAgentOptions)
    config = generateConfig()

    _edgeAgent.on_connected = on_connected
    _edgeAgent.on_disconnected = on_disconnected
    _edgeAgent.on_message = edgeAgent_on_message    

    _edgeAgent.connect()
    
    time.sleep(5)  # Waiting for connection to be established
    
    _edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)
    
    for i in range(1, 60):
        sendData(_edgeAgent)
        time.sleep(1)

def sendData(edgeAgent):
    data = generateData()
    edgeAgent.sendData(data)
