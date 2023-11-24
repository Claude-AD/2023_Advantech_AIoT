import time
from wisepaasdatahubedgesdk.Model.Edge import EdgeData, EdgeTag

def create_edge_data_from_plag(plag, device_id, tag_name):
    edge_data = EdgeData()
    edge_tag = EdgeTag(deviceId=device_id, tagName=tag_name, value=str(plag))
    edge_data.tagList.append(edge_tag)
    return edge_data

def receive_plag_data(plag, device_id):
    tag_name = "ATag1"  # 태그는 Analog타입의 ATag1
    edge_data = create_edge_data_from_plag(plag, device_id, tag_name)
    return edge_data
