import torch
import torch.nn as nn
import torchvision.models as models

class SteganNet(nn.Module):
    def __init__(self):
        super(SteganNet, self).__init__()
        # 使用预训练的ResNet18作为特征提取器
        resnet = models.resnet18(pretrained=True)
        self.features = nn.Sequential(*list(resnet.children())[:-2])
        
        # 特征提取层
        self.feature_layer = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 5)  # 5个主要特征
        )
        
        # 隐写检测层
        self.stego_layer = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        # 提取基础特征
        x = self.features(x)
        
        # 获取特征向量
        features = self.feature_layer(x)
        
        # 隐写检测
        x_flat = nn.AdaptiveAvgPool2d((1, 1))(x)
        x_flat = x_flat.view(x_flat.size(0), -1)
        stego_prob = self.stego_layer(x_flat)
        
        return features, stego_prob

def load_model(model_path=None):
    """
    加载预训练模型或创建新模型
    """
    model = SteganNet()
    if model_path and torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path))
    elif model_path:
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    return model 