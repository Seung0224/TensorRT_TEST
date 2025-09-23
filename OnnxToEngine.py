import os
import tensorrt as trt

# ==== [사용자 설정] ====
DEFAULT_MODEL_PATH = r"D:\SLA_Model"
ONNX_FILE = DEFAULT_MODEL_PATH + r"\SEG.onnx"      # 변환할 ONNX 파일 경로
ENGINE_FILE = DEFAULT_MODEL_PATH + r"\SEG.engine"  # 저장할 엔진 파일 경로
USE_FP16 = True                                # FP16 최적화 사용 여부
WORKSPACE_SIZE = 4096                          # 워크스페이스 (MB)
# ======================

def build_engine(onnx_file, engine_file, fp16=True, workspace=4096):
    logger = trt.Logger(trt.Logger.INFO)
    builder = trt.Builder(logger)
    network_flags = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    network = builder.create_network(network_flags)
    parser = trt.OnnxParser(network, logger)

    print(f"[INFO] Loading ONNX file: {onnx_file}")
    with open(onnx_file, "rb") as f:
        if not parser.parse(f.read()):
            print("[ERROR] Failed to parse the ONNX file.")
            for i in range(parser.num_errors):
                print(parser.get_error(i))
            return None

    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace * (1 << 20))

    if fp16 and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
        print("[INFO] FP16 mode enabled")
    else:
        print("[INFO] FP16 mode disabled")

    # 🔽 Optimization Profile 추가
    profile = builder.create_optimization_profile()
    input_tensor = network.get_input(0)  # 첫 번째 입력 (예: "images")
    name = input_tensor.name

    # ONNX 모델 입력 shape 가져오기 (예: [-1,3,-1,-1])
    input_shape = input_tensor.shape
    print(f"[INFO] Input tensor: {name}, shape={input_shape}")

    # min/opt/max shape 정의
    # → YOLO는 보통 (1,3,H,W), 여기서는 640x640 기준으로
    profile.set_shape(name,
                      min=(1, 3, 640, 640),   # 최소
                      opt=(1, 3, 640, 640),   # 최적
                      max=(1, 3, 640, 640)) # 최대
    config.add_optimization_profile(profile)

    print("[INFO] Building serialized TensorRT engine...")
    serialized_engine = builder.build_serialized_network(network, config)
    if serialized_engine is None:
        print("[ERROR] Failed to build serialized network")
        return None

    runtime = trt.Runtime(logger)
    engine = runtime.deserialize_cuda_engine(serialized_engine)

    with open(engine_file, "wb") as f:
        f.write(serialized_engine)
    print(f"[INFO] Engine saved at: {engine_file}")

    return engine


if __name__ == "__main__":
    if not os.path.exists(ONNX_FILE):
        print(f"[ERROR] ONNX file not found: {ONNX_FILE}")
    else:
        build_engine(ONNX_FILE, ENGINE_FILE, USE_FP16, WORKSPACE_SIZE)