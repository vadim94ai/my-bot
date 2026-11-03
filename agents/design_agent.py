import os
import json
import re
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class DesignAgent(BaseAgent):
    """
    Агент для генерации и обновления дизайна (HTML/CSS) на основе Tailwind и копирайтинга.
    """
    
    @property
    def stage_name(self) -> str:
        return 'design'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента дизайна.
        """
        self.log("Начало работы агента дизайна")
        
        try:
            copywriting_data = self.load_previous_stage('copywriting') or {}
            marketing_data = self.load_previous_stage('marketing') or {}
            
            # Обновление landing/index.html реальным контентом
            self._update_landing_page(copywriting_data, marketing_data)
            
            output_data = {
                "status": "success",
                "updated_files": ["landing/index.html", "build/index.html"],
                "palette": "violet/cyberpunk"
            }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа агента дизайна успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка при генерации дизайна: {e}", level="ERROR")
            return {}

    def _update_landing_page(self, copy_data: Dict[str, Any], marketing_data: Dict[str, Any]) -> None:
        """
        Обновляет landing/index.html текстами из копирайтинга.
        """
        landing_path = 'landing/index.html'
        if not os.path.exists(landing_path):
            self.log(f"Файл {landing_path} не найден, пропускаем точечное обновление.", level="WARNING")
            return
            
        with open(landing_path, 'r', encoding='utf-8') as f:
            html = f.read()

        h1 = copy_data.get('landing_h1', 'Создавай вирусные AI-видео, мультфильмы и 3D с нуля')
        h2 = copy_data.get('landing_h2', 'Полный практический курс по нейросетям для новичков')
        
        # Заголовок страницы
        html = re.sub(r'<title>.*?</title>', f'<title>{h1}</title>', html, flags=re.DOTALL)
        
        # Бейдж над h1
        html = re.sub(
            r'🚀\s*Новый курс для экспертов и продюсеров',
            '🚀 Практический курс по AI-видео для новичков',
            html
        )
        
        # Главный заголовок H1
        html = re.sub(
            r'<h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold text-white leading-\[1\.1\] mb-6">.*?</h1>',
            f'<h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold text-white leading-[1.1] mb-6">{h1}</h1>',
            html,
            flags=re.DOTALL
        )
        
        # Подзаголовок H2
        html = re.sub(
            r'<h2 class="text-xl md:text-2xl text-slate-300 font-medium mb-8 leading-relaxed">.*?</h2>',
            f'<h2 class="text-xl md:text-2xl text-slate-300 font-medium mb-8 leading-relaxed">{h2}</h2>',
            html,
            flags=re.DOTALL
        )
        
        # Цены
        html = re.sub(r'2\s*990\s*₽', '3 000 ₽', html)
        html = re.sub(r'Получить доступ за 2 990 ₽', 'Получить доступ за 3 000 ₽', html)
        
        # Боли (Pain points)
        pain_cards = copy_data.get('pain_cards', [])
        if len(pain_cards) >= 3:
            html = re.sub(
                r'Сколько денег вы теряете прямо сейчас\?',
                'С какими сложностями сталкивается каждый новичок?',
                html
            )
            # Замена названий болей
            html = re.sub(r'<h3 class="text-2xl font-bold text-white mb-4">Брошенные платежи</h3>\s*<p class="text-slate-400 leading-relaxed">.*?</p>',
                          f'<h3 class="text-2xl font-bold text-white mb-4">{pain_cards[0].get("title", "Оплата зарубежных сервисов")}</h3>\n<p class="text-slate-400 leading-relaxed">{pain_cards[0].get("description", "")}</p>',
                          html, flags=re.DOTALL)
            html = re.sub(r'<h3 class="text-2xl font-bold text-white mb-4">Утечка лидов</h3>\s*<p class="text-slate-400 leading-relaxed">.*?</p>',
                          f'<h3 class="text-2xl font-bold text-white mb-4">{pain_cards[1].get("title", "Непостоянные персонажи")}</h3>\n<p class="text-slate-400 leading-relaxed">{pain_cards[1].get("description", "")}</p>',
                          html, flags=re.DOTALL)
            html = re.sub(r'<h3 class="text-2xl font-bold text-white mb-4">Низкий средний чек</h3>\s*<p class="text-slate-400 leading-relaxed">.*?</p>',
                          f'<h3 class="text-2xl font-bold text-white mb-4">{pain_cards[2].get("title", "Сложный монтаж и софт")}</h3>\n<p class="text-slate-400 leading-relaxed">{pain_cards[2].get("description", "")}</p>',
                          html, flags=re.DOTALL)

        # Модули обучения (Механики)
        mechanics = copy_data.get('mechanics', [])
        if len(mechanics) >= 3:
            html = re.sub(r'3 механики роста дохода', 'Программа практического обучения', html)
            
            # Модуль 1
            html = re.sub(r'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">Верни брошенные платежи</h3>\s*<p class="text-lg text-slate-400 mb-8 leading-relaxed">.*?</p>',
                          f'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">{mechanics[0].get("title", "Модуль 1")}</h3>\n<p class="text-lg text-slate-400 mb-8 leading-relaxed">{mechanics[0].get("description", "")}</p>',
                          html, flags=re.DOTALL)
            # Модуль 2
            html = re.sub(r'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">Увеличь средний чек</h3>\s*<p class="text-lg text-slate-400 mb-8 leading-relaxed">.*?</p>',
                          f'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">{mechanics[1].get("title", "Модуль 2")}</h3>\n<p class="text-lg text-slate-400 mb-8 leading-relaxed">{mechanics[1].get("description", "")}</p>',
                          html, flags=re.DOTALL)
            # Модуль 3
            html = re.sub(r'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">Собери базу контактов</h3>\s*<p class="text-lg text-slate-400 mb-8 leading-relaxed">.*?</p>',
                          f'<h3 class="text-3xl md:text-4xl font-bold text-white mb-6">{mechanics[2].get("title", "Модуль 3")}</h3>\n<p class="text-lg text-slate-400 mb-8 leading-relaxed">{mechanics[2].get("description", "")}</p>',
                          html, flags=re.DOTALL)

        # FAQ
        faq = copy_data.get('faq', [])
        if len(faq) >= 3:
            html = re.sub(
                r'Сколько денег я верну с помощью этих механик\?',
                faq[0].get('question', 'Нужен ли мощный ПК?'),
                html
            )
            html = re.sub(
                r'В среднем наши клиенты возвращают от 20% до 35% брошенных корзин.*?первую неделю\.',
                faq[0].get('answer', 'Нет, достаточно обычного компьютера или смартфона.'),
                html,
                flags=re.DOTALL
            )
            html = re.sub(
                r'За какое время будут первые результаты\?',
                faq[1].get('question', 'Справлюсь ли я без опыта?'),
                html
            )
            html = re.sub(
                r'Внедрение всех трех механик занимает около 2-3 дней.*?на текущем трафике\.',
                faq[1].get('answer', 'Да! Обучение создано специально с нуля по шагам.'),
                html,
                flags=re.DOTALL
            )
            html = re.sub(
                r'Нужны ли технические навыки\?',
                faq[2].get('question', 'Как оплачивать зарубежные нейросети?'),
                html
            )
            html = re.sub(
                r'Сложные навыки программирования не требуются.*?делегировать задачу помощнику\.',
                faq[2].get('answer', 'Мы покажем проверенные и простые способы оплаты зарубежных сервисов из РФ.'),
                html,
                flags=re.DOTALL
            )

        with open(landing_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        os.makedirs('build', exist_ok=True)
        with open('build/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
            
        self.log("Файл landing/index.html успешно обновлен новыми текстами")
