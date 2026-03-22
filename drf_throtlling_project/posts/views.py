from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from .throttles import PostCreateThrottle


class PostListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'posts_list'

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [PostCreateThrottle, ScopedRateThrottle]
    throttle_scope = 'posts_create'

    def get(self, request):
        return Response({"message": "Use POST to create a post"})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
