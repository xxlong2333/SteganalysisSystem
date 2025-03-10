from django.db import models
import os

# Create your models here.
class User(models.Model):
    id = models.AutoField(id, primary_key=True)
    username = models.CharField("username", max_length=255, default='')
    password = models.CharField("password", max_length=255, default='')
    createTime = models.DateTimeField("创建时间", auto_now_add=True)
    class Meta:
        db_table = "user"

class History(models.Model):
    id = models.AutoField("id", primary_key=True)
    jobId = models.IntegerField("职位ID", max_length=255, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField("收藏次数", default=1)

    class Meta:
        db_table = "history"
#
# class SteganalysisResult(models.Model):
#     image = models.ImageField(upload_to='steganalysis_images/')
#     filename = models.CharField(max_length=255)
#     file_size = models.CharField(max_length=50)
#     upload_time = models.DateTimeField(auto_now_add=True)
#     analysis_time = models.DateTimeField(auto_now=True)
#     has_stego = models.BooleanField(default=False)
#     confidence = models.FloatField()
#
#     # 存储特征分析结果（JSON格式）
#     feature_analysis = models.JSONField()
#     # 存储算法识别结果（JSON格式）
#     algorithm_analysis = models.JSONField()
#
#     def __str__(self):
#         return f"{self.filename} - {'隐写' if self.has_stego else '无隐写'}"
#
#     def get_file_size_display(self):
#         size = os.path.getsize(self.image.path)
#         for unit in ['B', 'KB', 'MB', 'GB']:
#             if size < 1024:
#                 return f"{size:.2f} {unit}"
#             size /= 1024
#         return f"{size:.2f} TB"
#
