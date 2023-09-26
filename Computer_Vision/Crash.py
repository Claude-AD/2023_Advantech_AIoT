import numpy as np
from itertools import combinations

from Car_Manager import Car

cars = []
def crash(boxes, shape):
  cordi = boxes.xywh
  ids = boxes.id
  white = np.zeros(shape, dtype=np.uint8)

  n = len(cordi)
  if n <= 1 or ids == None:
    return white
  
  # Generate Car object
  global cars
  if len(cars) < int(ids.max().item()):
    for i in range(len(cars)+1, int(ids.max().item())+1):
      cars.append(Car())


  # Crash checking
  arr = [i for i in range(n)]
  arr = list(combinations(arr, 2))

  for n1, n2 in arr:
    p1 = (int(cordi[n1][0].item()), int(cordi[n1][1].item()))
    p2 = (int(cordi[n2][0].item()), int(cordi[n2][1].item()))
    
    # Add cordinate
    id1 = int(ids[n1].item())-1
    id2 = int(ids[n2].item())-1
    cars[id1].add(p1[0], p1[1])
    cars[id2].add(p2[0], p2[1])

    # Overlap checking
    th_w = cordi[n1][2]/2 + cordi[n2][2]/2
    th_h = cordi[n1][3]/2 + cordi[n2][3]/2

    if np.abs(p1[0]-p2[0]) < th_w and np.abs(p1[1]-p2[1]) < th_h:
      print(f"\nid:{ids[n1]}, id:{ids[n2]} OVERLAP")
      cars[id1].print_cordi()
      
  return white