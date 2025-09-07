# yourapp/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0   # 제일 중요한 페이지로 설정

    def items(self):
        # urls.py에서 name 으로 등록된 뷰 이름
        return ["customer_ai:chat_view","customer_ai:vision_view","customer_ai:novle_view" ]

    def location(self, item):
        return reverse(item)
