# TensorRT_TEST

1. Ultralytics Hub를 사용하여 DeepLearning Network Input size를 640x640으로 학습한 onnx 파일 필요
2. engine 파일로 변경시 아래와 같이 설정하고 engine 파일을 구성하면 640 이미지 전용으로만 사용
    profile.set_shape(name, min=(1, 3, 640, 640), opt=(1, 3, 640, 640), max=(1, 3, 640, 640))
   engine 파일로 변경시 아래와 같이 설정하면 다양한 입력이미지에대해서도 추론 가능
    profile.set_shape(name, min=(1, 3, 320, 320), opt=(1, 3, 640, 640), max=(1, 3, 1280, 1280))
3. 다양한 입력이미지로 사용하면 C++ Dll도 다시 소스를 작성해야함
4. 다만들엇으면 아래 이미지와 같이 나와있는 파일들을 실제로 내가 실행하는 .exe와 같은 경로에 넣고 동작시켜야함
   <img width="636" height="141" alt="image" src="https://github.com/user-attachments/assets/66c07fb1-ddcb-4ae0-ac8b-33293d1206c3" />

# onnx 실행 시 inferencetime
<img width="503" height="203" alt="onnx" src="https://github.com/user-attachments/assets/c7a9fd7f-aebe-4ad5-993e-e87b5272844e" />

# engine 실행 시 inferencetime
<img width="475" height="189" alt="engine" src="https://github.com/user-attachments/assets/4ae29c4b-4ec0-4d3d-8bd3-dd27f80af949" />
