import random

from wisepaasdatahubedgesdk.Model.Edge import EdgeData, EdgeTag, EdgeStatus

def __generateBatchData():    # send data in batch for high frequency data
  array = []
  for n in range(1, 10):
    edgeData = EdgeData()
    for i in range(1, 1 + 1):
      for j in range(1, 1 + 1):
        deviceId = 'Device' + str(i)
        tagName = 'ATag' + str(j)
        value = random.uniform(0, 100)
        tag = EdgeTag(deviceId, tagName, value)
        edgeData.tagList.append(tag)
      for j in range(1, 1 + 1):
        deviceId = 'Device' + str(i)
        tagName = 'DTag' + str(j)
        value = random.randint(0,99)
        value = value % 2
        tag = EdgeTag(deviceId, tagName, value)
        edgeData.tagList.append(tag)
      for j in range(1, 1 + 1):
        deviceId = 'Device' + str(i)
        tagName = 'TTag' + str(j)
        value = random.uniform(0, 100)
        value = 'TEST ' + str(value)
        tag = EdgeTag(deviceId, tagName, value)
        edgeData.tagList.append(tag)
    array.append(edgeData)
  return array


def generateData():
  edgeData = EdgeData()
  for i in range(1, 1 + 1 + 1):
    for j in range(1, 1 + 1):
      deviceId = 'Device' + str(i)
      tagName = 'ATag' + str(j)

      value = random.uniform(0, 100)
      tag = EdgeTag(deviceId, tagName, value)
      
      edgeData.tagList.append(tag)
    for j in range(1, 1 + 1):
      deviceId = 'Device' + str(i)
      tagName = 'DTag' + str(j)
      value = random.randint(0,99)
      value = value % 2
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
    for j in range(1, 1 + 1):
      deviceId = 'Device' + str(i)
      tagName = 'TTag' + str(j)
      value = random.uniform(0, 100)
      value = 'TEST ' + str(value)
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
  return edgeData

