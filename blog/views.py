from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# 输入：HTTP请求
# 处理：将请求的文章全部存到 context（字典）内
# 输出：将数据填充回 HTML 中 返回一个字符串（网页源码）


class PostListView(ListView):
    model = Post                        # 处理的是 Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'       
    ordering = ['-date_posted']         # 按照时间倒序排列
    paginate_by = 5                     # 自动分页 每页五个

# 展示列表 ListView 相当于基类 这里继承了 ListView


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    # 类似于CPP中的虚函数重写 调整了 get_queryset 的逻辑 找到作者是这个用户的文章

# 查寻


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']                   # 用户只能填充内容和标题

    def form_valid(self, form):                     # 自动填充作者
        form.instance.author = self.request.user    # 手动指向当前登陆用户
        return super().form_valid(form)

# 创建 Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):                             # 权限测试
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# 以上三个函数属于增删改 
# LoginRequiredMixin 检查用户是否登陆 
# UserPassesTestMixin 检查用户是否为作者 
# CreateView / UpdateView：负责具体的业务（显示表单、保存数据）。


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
