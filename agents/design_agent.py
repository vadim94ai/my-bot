import os
import asyncio
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class DesignAgent(BaseAgent):
    """
    Агент для генерации дизайна (HTML/CSS) на основе Jinja2 и Tailwind.
    """
    
    @property
    def stage_name(self) -> str:
        return 'design'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента-дизайнера.
        """
        self.log("Начало работы агента дизайна")
        
        try:
            copywriting_data = self.load_previous_stage('copywriting')
            design_tokens = self._load_design_tokens()
            
            # В реальном проекте здесь будет интеграция с Jinja2
            # Для тестового задания сгенерируем HTML напрямую (имитация рендера)
            
            index_html = self._render_template('landing_template.html', copywriting_data, design_tokens)
            success_html = self._render_template('success.html', {}, design_tokens)
            fail_html = self._render_template('fail.html', {}, design_tokens)
            
            # Сохранение сгенерированных файлов
            os.makedirs('build', exist_ok=True)
            with open('build/index.html', 'w', encoding='utf-8') as f:
                f.write(index_html)
            with open('build/success.html', 'w', encoding='utf-8') as f:
                f.write(success_html)
            with open('build/fail.html', 'w', encoding='utf-8') as f:
                f.write(fail_html)
                
            output_data = {
                "design_tokens": design_tokens,
                "responsive_breakpoints": {
                    "sm": "320px",
                    "md": "768px",
                    "lg": "1024px"
                },
                "generated_files": ["build/index.html", "build/success.html", "build/fail.html"]
            }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа агента дизайна успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка при генерации дизайна: {e}", level="ERROR")
            return {}
            
    def _load_design_tokens(self) -> Dict[str, Any]:
        """
        Загружает дизайн-токены.
        """
        # Цветовая палитра "Modern Navy" из промпта
        return {
            "colors": {
                "primary": "#1B2A4A",
                "secondary": "#3B82F6",
                "accent": "#F59E0B",
                "success": "#10B981",
                "danger": "#EF4444",
                "neutral_light": "#F8FAFC",
                "neutral_dark": "#0F172A",
                "text_primary": "#1E293B",
                "text_secondary": "#64748B",
                "border": "#E2E8F0"
            },
            "typography": {
                "headings": "Inter",
                "body": "Inter"
            }
        }
        
    def _render_template(self, template_name: str, copy_data: Dict[str, Any], design_tokens: Dict[str, Any]) -> str:
        """
        Имитация рендеринга шаблона Jinja2.
        """
        # Упрощенная генерация HTML для примера
        if template_name == 'landing_template.html':
            h1 = copy_data.get('landing_h1', 'Заголовок по умолчанию')
            return f"<!DOCTYPE html><html><head><title>{h1}</title><script src='https://cdn.tailwindcss.com'></script></head><body><h1>{h1}</h1></body></html>"
        return f"<!DOCTYPE html><html><head><title>{template_name}</title><script src='https://cdn.tailwindcss.com'></script></head><body><h1>{template_name}</h1></body></html>"
