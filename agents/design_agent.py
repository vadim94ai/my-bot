import os
import json
import re
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class DesignAgent(BaseAgent):
    """
    Агент для генерации и обновления дизайна (HTML/CSS) на основе Tailwind и копирайтинга.
    Поддерживает полную программу из 7 модулей и монетизацию.
    """
    
    @property
    def stage_name(self) -> str:
        return 'design'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента дизайна.
        """
        self.log("Начало работы агента дизайна (Сборка 7 модулей и программы)")
        
        try:
            copywriting_data = self.load_previous_stage('copywriting') or {}
            marketing_data = self.load_previous_stage('marketing') or {}
            
            # Обновление landing/index.html реальным контентом
            self._update_landing_page(copywriting_data, marketing_data)
            
            output_data = {
                "status": "success",
                "modules_count": len(copywriting_data.get('mechanics', [])),
                "updated_files": ["landing/index.html", "build/index.html"],
                "palette": "cyberpunk-violet"
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
            self.log(f"Файл {landing_path} не найден, пропускаем.", level="WARNING")
            return
            
        with open(landing_path, 'r', encoding='utf-8') as f:
            html = f.read()

        h1 = copy_data.get('landing_h1', 'Освой профессию AI-Креатора: от видео до первых 50 000 ₽')
        h2 = copy_data.get('landing_h2', 'Полный практический курс по генерации видео, анимаций и заработку для новичков')
        hero_p = copy_data.get('hero_paragraph', 'Превратите нейросети в источник стабильного дохода без мощного ПК.')

        # 1. Title и Hero
        html = re.sub(r'<title>.*?</title>', f'<title>{h1}</title>', html, flags=re.DOTALL)
        
        html = re.sub(
            r'🚀\s*[^<]+',
            '🚀 Полный курс от настройки до заработка первых денег',
            html
        )
        
        html = re.sub(
            r'<h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold text-white leading-\[1\.1\] mb-6">.*?</h1>',
            f'<h1 class="text-4xl md:text-5xl lg:text-7xl font-extrabold text-white leading-[1.1] mb-6">{h1}</h1>',
            html,
            flags=re.DOTALL
        )
        
        html = re.sub(
            r'<h2 class="text-xl md:text-2xl text-slate-300 font-medium mb-8 leading-relaxed">.*?</h2>',
            f'<h2 class="text-xl md:text-2xl text-slate-300 font-medium mb-8 leading-relaxed">{h2}</h2>\n<p class="text-slate-400 mb-8 leading-relaxed">{hero_p}</p>',
            html,
            flags=re.DOTALL
        )

        # 2. Цены
        html = re.sub(r'2\s*990\s*₽', '3 000 ₽', html)
        html = re.sub(r'Получить доступ за [^<]+', 'Получить доступ за 3 000 ₽', html)

        # 3. Боли (Pain Points)
        pain_cards = copy_data.get('pain_cards', [])
        if len(pain_cards) >= 3:
            html = re.sub(
                r'Сколько денег вы теряете прямо сейчас\?',
                'С какими сложностями сталкивается каждый новичок?',
                html
            )
            html = re.sub(
                r'С какими сложностями сталкивается каждый новичок\?',
                'С какими барьерами сталкивается 90% новичков?',
                html
            )

        # 4. Генерация блока всех 7 модулей
        mechanics = copy_data.get('mechanics', [])
        if mechanics:
            modules_html = '<div class="space-y-12">\n'
            colors = [
                ("from-blue-600 to-indigo-600", "border-blue-500/30", "bg-blue-500/10", "text-blue-400"),
                ("from-purple-600 to-pink-600", "border-purple-500/30", "bg-purple-500/10", "text-purple-400"),
                ("from-cyan-600 to-blue-600", "border-cyan-500/30", "bg-cyan-500/10", "text-cyan-400"),
                ("from-emerald-600 to-teal-600", "border-emerald-500/30", "bg-emerald-500/10", "text-emerald-400"),
                ("from-amber-600 to-orange-600", "border-amber-500/30", "bg-amber-500/10", "text-amber-400"),
                ("from-rose-600 to-red-600", "border-rose-500/30", "bg-rose-500/10", "text-rose-400"),
                ("from-violet-600 to-purple-600", "border-violet-500/30", "bg-violet-500/10", "text-violet-400"),
            ]
            
            for i, m in enumerate(mechanics):
                num = m.get('module_num', i + 1)
                title = m.get('title', f'Модуль {num}')
                desc = m.get('description', '')
                bullets = m.get('bullets', [])
                
                c_grad, c_border, c_bg, c_text = colors[i % len(colors)]
                
                bullets_li = ""
                for b in bullets:
                    bullets_li += f'''
                    <li class="flex items-start">
                        <div class="w-6 h-6 rounded-full {c_bg} flex items-center justify-center mr-3 mt-1 flex-shrink-0">
                            <svg class="w-4 h-4 {c_text}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        </div>
                        <span class="text-slate-300 text-base">{b}</span>
                    </li>
                    '''
                    
                modules_html += f'''
                <div class="bg-white/5 backdrop-blur-xl rounded-3xl p-8 lg:p-10 border {c_border} hover:border-white/30 transition-all duration-300 shadow-xl" data-aos="fade-up">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                        <div class="inline-flex items-center px-4 py-1.5 rounded-full bg-gradient-to-r {c_grad} text-white font-bold text-sm tracking-wide shadow-md">
                            МОДУЛЬ #{num:02d}
                        </div>
                        <div class="text-sm font-semibold {c_text} tracking-wider uppercase">
                            Практический блок
                        </div>
                    </div>
                    <h3 class="text-2xl lg:text-3xl font-extrabold text-white mb-4 leading-snug">{title}</h3>
                    <p class="text-slate-300 text-lg mb-6 leading-relaxed">{desc}</p>
                    <div class="border-t border-white/10 pt-6">
                        <h4 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Чему вы научитесь:</h4>
                        <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {bullets_li}
                        </ul>
                    </div>
                </div>
                '''
            modules_html += '</div>\n'
            
            # Заменяем секцию механик на все модули
            pattern = r'<section id="features" class="py-24 relative border-t border-white/5">.*?<!-- SOCIAL PROOF SECTION -->'
            replacement = f'''<section id="features" class="py-24 relative border-t border-white/5">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-20" data-aos="fade-up">
                <div class="inline-block px-4 py-2 rounded-full bg-accent/20 border border-accent/30 text-accent font-semibold text-sm mb-4">
                    7 ПОЛНЫХ МОДУЛЕЙ • ОТ НАСТРОЙКИ ДО ЗАРАБОТКА
                </div>
                <h2 class="text-3xl md:text-5xl font-extrabold text-white mb-6">Программа практического курса</h2>
                <div class="w-24 h-1 bg-gradient-to-r from-secondary to-accent mx-auto rounded-full mb-6"></div>
                <p class="text-slate-400 text-lg max-w-2xl mx-auto">Каждый модуль содержит пошаговые видеоуроки, готовые промты, скрипты и файлы для практики.</p>
            </div>
            {modules_html}
        </div>
    </section>

    <!-- SOCIAL PROOF SECTION -->'''
            html = re.sub(pattern, replacement, html, flags=re.DOTALL)

        # 5. FAQ
        faq = copy_data.get('faq', [])
        if faq:
            faq_html = ""
            for item in faq:
                q = item.get('question', '')
                a = item.get('answer', '')
                faq_html += f'''
                <div class="faq-item border border-white/10 rounded-2xl overflow-hidden bg-white/5 backdrop-blur-md mb-4">
                    <button class="faq-button w-full px-6 py-5 text-left flex justify-between items-center focus:outline-none transition-colors hover:bg-white/10" aria-expanded="false">
                        <span class="font-bold text-white text-lg">{q}</span>
                        <svg class="w-6 h-6 text-secondary transform transition-transform duration-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                    </button>
                    <div class="faq-content px-6 pb-5 text-slate-300 max-h-0 overflow-hidden transition-all duration-300 opacity-0">
                        {a}
                    </div>
                </div>
                '''
            faq_pattern = r'<div class="space-y-4" data-aos="fade-up" data-aos-delay="100">.*?</div>\s*</div>\s*</section>'
            faq_replacement = f'<div class="space-y-4" data-aos="fade-up" data-aos-delay="100">\n{faq_html}\n</div>\n</div>\n</section>'
            html = re.sub(faq_pattern, faq_replacement, html, flags=re.DOTALL)

        with open(landing_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        os.makedirs('build', exist_ok=True)
        with open('build/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
            
        self.log(f"Лендинг успешно обновлен. Отрендерено {len(mechanics)} модулей программы!")
