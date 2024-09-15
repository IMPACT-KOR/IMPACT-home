
from django.shortcuts import render, redirect
import random
import json
from django.http import JsonResponse
from datetime import datetime

# 홈 화면
def home(request):
    return render(request, 'home.html')

# 초기 재화 설정 함수
def initialize_coins(request):
    if 'coins' not in request.session:
        request.session['coins'] = 0  # 기본 재화는 0으로 설정
    request.session.modified = True  # 세션이 변경되었음을 명시적으로 알림
    return request


# Sybill Trelawney: Professor of divination
def trelawney_conversation(request):
    request = initialize_coins(request)
    coins = request.session['coins']
    message = "안녕하세요, 저는 Trelawney입니다. 당신의 운세를 점쳐드릴 수 있습니다."
    
    if request.method == 'POST':
        use_coins = request.POST.get('use_coins')
        if use_coins == "1" and coins > 0:  # 재화가 있고 사용하기를 선택한 경우
            return redirect('luck_today')  # 운세 결과 페이지로 이동
        elif use_coins == "1" and coins == 0:  # 재화가 없을 경우
            message = "재화가 부족하여 기본 운세만 확인할 수 있습니다."
            return render(request, 'trelawney.html', {'message': message, 'coins': coins})
        elif use_coins == "0":  # 재화를 사용하지 않기 선택
            return redirect('luck_today')  # 운세 결과 페이지로 이동

    return render(request, 'trelawney.html', {'message': message, 'coins': coins})

# Sybill Trelawney_luck_today 
def luck_today(request):
    request = initialize_coins(request)
    coins = request.session['coins']  # 세션에서 재화 가져오기
    fortune = None
    require_birthdate = False  # 생년월일 입력 여부

    if request.method == 'POST':
        birthdate_str = request.POST.get('birthdate')  # 생년월일

        if coins > 0:  # 재화를 사용할 경우
            fortunes = {
                'love': random.choice(["연애운이 아주 좋습니다!", "연애에 주의가 필요합니다."]),
                'money': random.choice(["금전운이 상승 중입니다!", "지출을 조심해야 합니다."]),
                'business': random.choice(["사업운이 좋아질 것입니다.", "사업에 조심해야 합니다."])
            }
            request.session['coins'] -= 1  # 재화 차감
            request.session.modified = True  # 세션 변경 반영
            fortune = random.choice(list(fortunes.values()))  # 다양한 운세 제공

        else:  # 재화가 부족하거나 사용하지 않기를 선택한 경우
            require_birthdate = True  # 기본 운세 확인을 위해 생년월일 입력 요구
            if birthdate_str:  # 생년월일이 입력되면
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
                fortune = generate_fortune_based_on_birthdate(birthdate)  # 기본 운세 제공

    return render(request, 'luck.html', {
        'fortune': fortune,
        'coins': coins,
        'require_birthdate': require_birthdate
    })

# 생년월일에 따른 운세 생성 함수
def generate_fortune_based_on_birthdate(birthdate):
    fortunes = [
        "오늘은 평온한 하루가 될 것입니다.",
        "뜻밖의 행운이 당신을 기다리고 있습니다.",
        "약간의 어려움이 있을 수 있으나 금방 해결될 것입니다.",
        "새로운 인연이 생길 가능성이 있습니다.",
        "재정적으로 좋은 소식이 있을 것입니다."
    ]
    random.seed(birthdate.toordinal())  # 생년월일을 시드로 사용하여 랜덤 운세 제공
    return random.choice(fortunes)




# Rolanda Hooch: Flying instructor, Quidditch referee, and coach
def hooch_conversation(request):
    request = initialize_coins(request)  # 세션에 재화 정보 초기화 또는 불러오기
    coins = request.session['coins']  # 현재 재화 정보 가져오기

    # Hooch의 인사말
    message = "안녕하세요! 저는 Hooch입니다. 게임을 통해 재화를 얻을 수 있습니다."

    return render(request, 'hooch.html', {'message': message, 'coins': coins})


# Rolanda Hooch_galaga (게임 클리어 시 재화 추가)
def galaga_game(request):
    if request.method == 'POST':
        request = initialize_coins(request)  # 세션에 재화 정보 초기화
        coins = request.session['coins']
        
        try:
            # 클라이언트에서 보내온 재화를 세션에 추가
            data = json.loads(request.body)
            request.session['coins'] += data.get('coins', 0)
            request.session.modified = True  # 세션이 변경되었음을 명시적으로 알림

            # 세션에 재화가 제대로 저장되는지 확인
            print(f"현재 세션 내 재화: {request.session['coins']}")  # 세션 로그

            return JsonResponse({"status": "success", "coins": request.session['coins']})
        
        except Exception as e:
            print(f"재화 업데이트 중 오류 발생: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return render(request, 'galaga.html')