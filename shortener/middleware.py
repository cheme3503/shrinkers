from shortener.models import BackOfficeLogs,Users, JobInfo
from urllib.parse import unquote
import json

class ShrinkersMiddleware:                     #Middleware is a callable that takes a request and returns a response
    def __init__(self, get_response):          #"callable"은 호출 가능한 클래스 인스턴스, 함수, 메서드 등 객체를 의미함.
                                               # __call__ 메서드가 있으면 클래스 인스턴스를 호출 가능함.
                                               #get_response callable might be the actual view or next middleware in the chain.
        self.get_response = get_response

    def __call__(self, request):
        request.users_id = None
        if request.user.is_authenticated:
            get_user = Users.objects.filter(user=request.user).first()
            if get_user:
                request.users_id = get_user.id
        response =self.get_response(request)
        if request.method not in ['GET','OPTIONS']:
            try:
                body = json.loads(request.body) if request.body else None
            except json.decoder.JSONDecodeError:
                body = self.form_data_to_dict(request.body)
                #form data로 넘어온 경우 json type이 아니므로, dictionary로 변환 필요-이를 위해 아래에 함수 method 정의
            endpoint = request.get_full_path_info()
            ip = (
                request.header['X-Forwarded-For'].split(',')[0]
                if 'x-Forwarded-for' in request.headers.keys()
                else request.META.get('REMOTE_ADDR', None)
            )

           # X-Forwarded-For: <supplied-value>, <client-ip>, <load-balancer-ip>
          # request.META 속성( attribute) - Contains HTTP headers added by
          # browsers or a web server as part of the request.Parameters are
          # enclosed in a standrd python dictionary where keys are the
         # HTTP header names -in uppercase and unserscore
         # request.META.get('REMOTE_ADDR')은 user의  remote IP address 값을 얻음

            ip = ip.split(',')[0] if ',' in ip else ip

            BackOfficeLogs.objects.create(
                endpoint = endpoint,
                body=body,
                ip=ip,
                user_id=request.user.id,
                status_code=response.status_code,
                method = request.method,
            )

            if response.status_code >= 500:
                ADMIN_EMAIL = "rocklay.info@gmail.com"
                content = f"{response.status_code} 에러 발생 \n" \
                          f"엔드포인드 : ({str(request.method).upper()}) {endpoint}\n" \
                          f"IP : {ip} \n" \
                          f"User ID : {request.users_id} \n"
                JobInfo.objects.create(
                    job_id=f"u-0-send_email",
                    user_id=request.users_id,
                    additional_info={"recipient": ["admin", ADMIN_EMAIL], "content": content},
                )
        return response


        #다음 middleware로 response 값을 넘겨줌

    @staticmethod
    def form_data_to_dict(body:bytes):
        UNLOGGABLES =['csrfmiddlewaretoken', 'password']
        body = body.decode('utf-8')
        body = unquote(body).split('&')
        rtn = {}
        for b in body:
            body_list = b.split('=')
            if body_list[0] not in UNLOGGABLES:
                rtn[body_list[0]] = body_list[1]
            else:
                rtn[body_list[0]] = 'hidden'
        return rtn


