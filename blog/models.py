from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField  # 1. 引入新字段类型
from markdownx.utils import markdownify

class Post(models.Model):
    title = models.CharField(max_length=100)                    # 标题
    # content = models.TextField() 原先的文本编辑器
    content = MarkdownxField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 级联删除 随作者一同删除

    def __str__(self):
        return self.title 
    # 重构运算符 让其返回文章标题 而不是地址

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    # 返回网页路径 pk：主键 即ID

    # 3. 新增一个“属性”方法，把 Markdown 文本转成 HTML
    # 这样在模板里直接调用 post.formatted_markdown 就能拿到 HTML
    @property
    def formatted_markdown(self):
        return markdownify(self.content)