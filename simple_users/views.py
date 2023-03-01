from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SimpleUser
from .serializers import SimpleUserSerializer


class SimpleUserCreateAPIView(generics.CreateAPIView):
    queryset = SimpleUser.objects.all()
    serializer_class = SimpleUserSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(["POST"])
def login_simulation(request):
    try:
        user = request.POST["username"]

        if SimpleUser.objects.filter(username=user).exists():
            response = Response({"message": f"Welcome {user}"})
            response.set_cookie(key="sessionid", value=user)
            return response

        else:
            return Response({"error": f"Username {user} does not exist"})
    except:
        return Response({"error": "You must provide a username"})
