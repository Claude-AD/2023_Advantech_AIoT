import numpy as np
from itertools import combinations

from Car_Manager import Car

cars = []
def crash(boxes, shape):
  cordi = boxes.xywh
  ids = boxes.id
  white = np.zeros(shape, dtype=np.uint8)
  n = len(cordi)
  
  if ids == None:
    return white
  
  # Generate Car object
  global cars
  if len(cars) < int(ids.max().item()):
    for _ in range(len(cars)+1, int(ids.max().item())+1):
      cars.append(Car())

  # Add cordinate & update self.frame
  for i in range(n):
    id = int(ids[i].item())-1
    cars[id].add(int(cordi[i][0].item()), int(cordi[i][1].item()))
    if len(cars[id].a) > 0:
      cars[id].frame += 1
      if cars[id].frame == 10:
        print(f"\nid: {id+1}")
        cars[id].accel()
        cars[id].speed()
      elif cars[id].frame > 10:
        cars[id].frame = 0
        cars[id].a.clear()

  if n <= 1:
    return white

  # Crash checking
  arr = [i for i in range(n)]
  arr = list(combinations(arr, 2))
  for n1, n2 in arr:
    p1 = (int(cordi[n1][0].item()), int(cordi[n1][1].item()))
    p2 = (int(cordi[n2][0].item()), int(cordi[n2][1].item()))
    
    id1 = int(ids[n1].item())-1
    id2 = int(ids[n2].item())-1

    # Overlap checking
    th_w = cordi[n1][2]/2 + cordi[n2][2]/2
    th_h = cordi[n1][3]/2 + cordi[n2][3]/2

    if np.abs(p1[0]-p2[0]) < th_w and np.abs(p1[1]-p2[1]) < th_h:
      print(f"\nid:{ids[n1]}, id:{ids[n2]} OVERLAP")
      if len(cars[id1].a) > 0 or len(cars[id1].cordi_x) < 3:
        pass
      else:
        cars[id1].accel()

      if len(cars[id2].a) > 0 or len(cars[id2].cordi_x) < 3:
        pass
      else:
        cars[id2].accel()

      
  return white