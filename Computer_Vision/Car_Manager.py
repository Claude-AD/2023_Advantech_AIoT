import cv2
import numpy as np
from collections import deque
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import joblib

data = {'alpha':[],
        'beta' :[],
        'gamma':[],
        'accident':[]}

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
    
    def avg_cordi(self):
        n = len(self.cordi_x)
        sum_x, sum_y = 0,0
        for i in range(n-1, 0, -1):
            sum_x += self.cordi_x[i]
            sum_y += self.cordi_y[i]
        return (sum_x/n, sum_y/n)
    

class Overlap():
    def __init__(self, car1, car2):
        self.car1 = car1
        self.car2 = car2
        self.a1 = []
        self.a2 = []
        self.is_on = True
        self.frame = 1
        self.alpha = 0
        self.angle1 = []
        self.angle2 = []
        self.gamma = []

    # Speed Algorithm
    def speed(self):
        if len(self.car1.cordi_x) < 3 or len(self.car2.cordi_x) < 3:
            self.is_on = False
        else:
            self.a1.append(self.car1.accel())
            self.a2.append(self.car2.accel())
            if len(self.a1) == 2:
                self.alpha = max(self.a1)/min(self.a1) + max(self.a2)/min(self.a2)
                print(f"id_{self.car1.id:02}: [{self.a1[0]:.3f} | {self.a1[1]:.3f}]")
                print(f"id_{self.car2.id:02}: [{self.a2[0]:.3f} | {self.a2[1]:.3f}]")

    # Angle Algorithm
    def angle(self):
        if self.is_on:
            self.angle1.append(self.car1.avg_cordi())
            self.angle2.append(self.car2.avg_cordi())
            if len(self.angle1) == 1:
                self.angle1.append((self.car1.cordi_x[-1], self.car1.cordi_y[-1]))
                self.angle2.append((self.car2.cordi_y[-1], self.car2.cordi_y[-1]))
            if len(self.angle1) == 3:
                a = tuple(elem[0]- elem[1] for elem in zip(self.angle1[0], self.angle1[1]))
                b = tuple(elem[0]- elem[1] for elem in zip(self.angle1[2], self.angle1[1]))
                angle1 = np.arccos(np.dot(a,b)/np.sqrt(a[0]**2+a[1]**2)/np.sqrt(b[0]**2+b[1]**2))*180/np.pi
                
                a = tuple(elem[0]- elem[1] for elem in zip(self.angle2[0], self.angle2[1]))
                b = tuple(elem[0]- elem[1] for elem in zip(self.angle2[2], self.angle2[1]))
                angle2 = np.arccos(np.dot(a,b)/np.sqrt(a[0]**2+a[1]**2)/np.sqrt(b[0]**2+b[1]**2))*180/np.pi
                print(f"{angle1:.3f}, {angle2:.3f}")
                print(f"******** alpha = {self.alpha:.3f} ********")
                print(f"******** beta  = {angle1 + angle2:.3f} ********")
                print(f"******** gamma = {min(self.gamma):.3f} ********")
                # data['alpha'].append(self.alpha)
                # data['beta'].append(angle1 + angle2)
                # data['gamma'].append(min(self.gamma))
                # if self.alpha > 10 and min(self.gamma) < 100:
                #     data['accident'].append(1)
                # else: data['accident'].append(0)

                model = joblib.load('./accident/test01.pkl')
                prediction = model.predict([[self.alpha, angle1 + angle2, min(self.gamma)]])
                print(f"{prediction.item()*100:.2f}%")
                if prediction.item()*100 > 50:
                    print('********ACCIDENT********')
                    print('********ACCIDENT********')
                    print('********ACCIDENT********')
                    
    # Estimate Trajectory
    def trace(self, white, threshold):
        ret = False
        if self.is_on:
            gamma = 1000000
            for car in [self.car1, self.car2]:
                X = np.array(car.cordi_x).reshape(-1, 1)
                y = car.cordi_y

                poly_features = PolynomialFeatures(degree=1)
                X_poly = poly_features.fit_transform(X)

                model = LinearRegression()
                model.fit(X_poly, y)

                dif = car.cordi_x[-1] - car.cordi_x[0]
                x = np.linspace(car.cordi_x[-1], car.cordi_x[-1] + dif*1.3, 10)

                X_plot = poly_features.transform(x.reshape(-1, 1))
                y_plot = model.predict(X_plot)

                points = [(int(i), int(j)) for i, j in zip(x, y_plot)]
                
                if car == self.car1: opponent = self.car2
                else: opponent = self.car1
                for p in points:
                    gamma = min(gamma, np.linalg.norm(np.array(p) - np.array((opponent.cordi_x[-1], opponent.cordi_y[-1]))))
                cv2.polylines(white, [np.array(points)], isClosed=False, color=(0, 255, 0), thickness=3)
        self.gamma.append(gamma)

        return ret, white