import cv2
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class car:
    def __init__(self, x, y):
        self.cordi_x = [x]
        self.cordi_y = [y]

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