import cv2
import numpy as np
from collections import deque
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class Car:
    def __init__(self, id):
        self.cordi_x = deque()
        self.cordi_y = deque()
        self.id = id

    # Manage cordinate
    def add(self, x, y):
        if len(self.cordi_x) > 10:
            self.cordi_x.popleft()
        if len(self.cordi_y) > 10:
            self.cordi_y.popleft()
        self.cordi_x.append(x)
        self.cordi_y.append(y)
        return

    # calculate acceleration
    def accel(self):
        n = len(self.cordi_x)
        half = int(n/2)
        vx = [self.cordi_x[half] - self.cordi_x[0],
              self.cordi_x[-1] - self.cordi_x[half]]
        vy = [self.cordi_y[half] - self.cordi_y[0],
              self.cordi_y[-1] - self.cordi_y[half]]
        ax = (vx[1] - vx[0]) / 2
        ay = (vy[1] - vy[0]) / 2
        a = (ax**2+ay**2)**(1/2)
        if a == 0:
            return 1
        return a

    # Angle Algorithm
    def angle(self):
        pass

    # Estimate Trajectory
    def trace(self, x, y, white, threshold, opponent):
        if 0.95< self.cordi_x[-1]/x <1.05 and 0.95< self.cordi_y[-1]/y <1.05:
            pass
        else:
            self.cordi_x.append(x)
            self.cordi_y.append(y)

        ret = False
        if len(self.cordi_x) < 5:
            return ret, white
        else:
            X = np.array(self.cordi_x).reshape(-1, 1)
            y = self.cordi_y

            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)

            model = LinearRegression()
            model.fit(X_poly, y)

            diff = 0
            for i in range(4):
                diff += self.cordi_x[-1-i] - self.cordi_x[-1-i-1]
            diff /= 4
            if diff > 0:
                x = np.linspace(self.cordi_x[-1], self.cordi_x[-1] + diff*10, 10)
            else:
                x = np.linspace(self.cordi_x[-1] + diff*10, self.cordi_x[-1], 10)
            X_plot = poly_features.transform(x.reshape(-1, 1))
            y_plot = model.predict(X_plot)

            points = [(int(i), int(j)) for i, j in zip(x, y_plot)
                      if np.linalg.norm(np.array((self.cordi_x[-1], self.cordi_y[-1])) - np.array((i, j))) <= threshold*1.5]
            
            for p in points:
                if np.linalg.norm(np.array(p) - np.array(opponent)) < threshold/4:
                    ret = True
            cv2.polylines(white, [np.array(points)], isClosed=False, color=(0, 255, 0), thickness=3)    

        return ret, white
    

class Overlap():
    def __init__(self, car1, car2):
        self.car1 = car1
        self.car2 = car2
        self.a1 = []
        self.a2 = []
        self.is_on = True
        self.frame = 1
        self.alpha = 0
    
    # Speed Algorithm
    def speed(self):
        if len(self.car1.cordi_x) < 3:
            self.is_on = False
        elif len(self.car2.cordi_x) < 3:
            self.is_on = False
        else:
            self.a1.append(self.car1.accel())
            self.a2.append(self.car2.accel())
            if len(self.a1) == 2:
                self.alpha = max(self.a1)/min(self.a1) + max(self.a2)/min(self.a2)
                print(f"id_{self.car1.id:02}: [{self.a1[0]:.3f} | {self.a1[1]:.3f}]")
                print(f"id_{self.car2.id:02}: [{self.a2[0]:.3f} | {self.a2[1]:.3f}]")
                print(f"******** alpha = {self.alpha:.3f} ********")
