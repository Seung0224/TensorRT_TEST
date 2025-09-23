# TensorRT_TEST

1. Ultralytics Hub를 사용하여 DeepLearning Network Input size를 640x640으로 학습한 onnx 파일 필요
2. engine 파일로 변경시 아래와 같이 설정하고 engine 파일을 구성하면 640 이미지 전용으로만 사용
    profile.set_shape(name, min=(1, 3, 640, 640), opt=(1, 3, 640, 640), max=(1, 3, 640, 640))
   engine 파일로 변경시 아래와 같이 설정하면 다양한 입력이미지에대해서도 추론 가능
    profile.set_shape(name, min=(1, 3, 320, 320), opt=(1, 3, 640, 640), max=(1, 3, 1280, 1280))
3. 다양한 입력이미지로 사용하면 C++ Dll도 다시 소스를 작성해야함
