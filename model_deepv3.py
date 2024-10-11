from tensorflow.keras.models import load_model
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras import layers, models

def create_deeplabv3plus(input_shape=(256, 256, 3), num_classes=2):
    # Sử dụng ResNet50V2 làm backbone cho DeepLabV3+
    base_model = ResNet50V2(weights='imagenet', include_top=False, input_shape=input_shape)

    # Lấy các đặc trưng từ model backbone
    x = base_model.output

    # Áp dụng các lớp bổ sung cho DeepLabV3+
    x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((4, 4))(x)
    x = layers.Conv2D(num_classes, (1, 1), activation='softmax')(x)

    # Tạo mô hình
    model = models.Model(inputs=base_model.input, outputs=x)

    return model


