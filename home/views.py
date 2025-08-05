from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import logout
from user_auth.models import Celebrity

# 기본 뷰 함수들
def home(request):
    return render(request, 'home/home.html')

def main(request):
    
    celebrity_list = Celebrity.objects.all() # 변수명을 더 명확하게 변경 (선택 사항)
    context = {
        "celebrity_list": celebrity_list,
    }
    return render(request, 'home/main.html', context)


def user_logout(request):
    logout(request)
    return redirect('register:login') 

# users 테이블에 데이터 삽입 함수 (함수만 정의, 바로 실행하지 않음)
def insert_users_raw_sql():
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (user_name, email, password, nickname, phonenumber) VALUES
            ('user1', 'user1@gmail.com', '1234', 'JohnnyD', '010-1234-5678'),
            ('admin1', 'admin@gmail.com', '1234', 'JaneS', '010-9876-5432')
        """)

# users 테이블에서 데이터 조회 함수
def select_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
    return rows

