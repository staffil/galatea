# customer_ai/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from customer_ai.models import LLM
class LLMSitemapAllModes(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # 각 LLM 객체에 대해 세 모드 URL 생성
        items = []
        for llm in LLM.objects.all():
            items.append(('chat', llm.id))
            items.append(('vision', llm.id))
            items.append(('novel', llm.id))
        return items

    def location(self, item):
        mode, llm_id = item
        if mode == 'chat':
            return reverse('customer_ai:chat_view', args=[llm_id])
        elif mode == 'vision':
            return reverse('customer_ai:vision_view', args=[llm_id])
        elif mode == 'novel':
            return reverse('customer_ai:novel_view', args=[llm_id])
