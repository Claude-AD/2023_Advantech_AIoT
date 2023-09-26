# Development Log
---
### 2023.09.25

YOLOv8을 이용해 객체 간 overlap 구현 시작

pre-trained된 YOLO 모델이 부서진 차에 대해서는 인식률이 떨어짐

부서진 차에 대해서 train이 필요할 듯

---

### 2023.09.26

overlap 구현 성공

overlap된 각 객체의 overlap 전후 15 프레임에서 평균 가속도와 최대 가속도의 차이를 계산하는 Speed 기능 구현 시작
