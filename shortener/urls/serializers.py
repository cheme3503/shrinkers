from shortener.utils import url_count_changer
from django.contrib.auth.models import User
from shortener.models import Users, ShortenedUrls
from rest_framework import serializers                  #serializer는 요청한 모델을 API로 보여줄 때 사용하는 클래스임. 보통 GET
                                                        #방식으로 모델에 대한 데이터를 요청했을 때, Serializer를 활용해 데이터를 제공

class UserBaseSerializer(serializers.ModelSerializer):  #ModelSerializer를 상속받아 직렬화 클래스를 만듬

    class Meta:
        model = User
        exclude = ('password',)

class UserSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Users
        fields = ["id", "url_count", "organization", "user"]

class UrlListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = ShortenedUrls
        fields = "__all__"

class UrlCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    target_url = serializers.CharField(max_length=2000)
    category = serializers.IntegerField(required=False)
    def create(self, request, data, commit=True):
        instance = ShortenedUrls()
        instance.creator_id = request.user.id
        instance.category = data.get("category", None)
        instance.target_url = data.get("target_url").strip()
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)

        return instance
