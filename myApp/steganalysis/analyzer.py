import torch
from PIL import Image
import numpy as np
from torchvision import transforms
from .model import load_model
from django.conf import settings

class ImageAnalyzer:
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = load_model(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
    
    def analyze(self, image_path):
        """
        分析图像，返回特征和隐写检测结果
        """
        try:
            # 加载和预处理图像
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # 进行预测
            with torch.no_grad():
                features, stego_prob = self.model(image_tensor)
                
                # 获取特征值和隐写检测结果
                features = features[0].cpu().numpy()
                stego_prob = stego_prob.item()
                
                # 特征分析结果
                feature_names = ['颜色分布', '纹理特征', '频域特征', '统计特征', '空间特征']
                feature_values = features.tolist()
                
                # 算法识别结果（示例，实际应该基于特征进行判断）
                algorithm_probs = {
                    'LSB': max(0.1, min(0.9, feature_values[0])),
                    'DCT': max(0.1, min(0.9, feature_values[1])),
                    'DWT': max(0.1, min(0.9, feature_values[2])),
                    'PVD': max(0.1, min(0.9, feature_values[3]))
                }
                
                return {
                    'success': True,
                    'has_stego': stego_prob > 0.5,
                    'confidence': stego_prob if stego_prob > 0.5 else 1 - stego_prob,
                    'features': {
                        'names': feature_names,
                        'values': feature_values
                    },
                    'algorithms': [
                        {'name': k, 'probability': v * 100}
                        for k, v in algorithm_probs.items()
                    ]
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# 创建全局分析器实例
analyzer = ImageAnalyzer(settings.STEGANALYSIS_MODEL_PATH) 