import json
from pathlib import Path

class SlidesGenerator:
    """Генератор HTML-презентаций для видео."""

    def __init__(self, design_tokens_path: str = 'configs/design_tokens.json') -> None:
        """Инициализирует генератор слайдов и загружает токены дизайна."""
        self.design_tokens_path = design_tokens_path
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> dict:
        """Загружает настройки стилей (цвета, шрифты) из JSON-файла."""
        try:
            with open(self.design_tokens_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Значения по умолчанию, если файл не найден
            return {
                "colors": {
                    "primary": "#1B2A4A",
                    "secondary": "#3B82F6",
                    "accent": "#F59E0B",
                    "text": "#1E293B",
                    "background": "#F8FAFC"
                },
                "typography": {
                    "font_family": "Inter, sans-serif"
                }
            }

    def generate_presentation(self, theses: list[str], title: str, subtitle: str) -> str:
        """
        Генерирует полный HTML-код презентации.
        
        Слайд 1: Титульный (название + подзаголовок)
        Слайды 2-N: По одному тезису на слайд
        Последний слайд: Призыв к действию (CTA)
        """
        slides = []
        slides.append(self._create_title_slide(title, subtitle))

        total = len(theses)
        for i, thesis in enumerate(theses, 1):
            slides.append(self._create_slide_html(thesis, i, total))

        slides.append(self._create_cta_slide("Переходи по ссылке ниже", "https://example.com"))

        slides_html = "\n".join(slides)
        
        font_family = self.tokens.get('typography', {}).get('font_family', 'Inter, sans-serif')
        bg_color = self.tokens.get('colors', {}).get('background', '#F8FAFC')
        text_color = self.tokens.get('colors', {}).get('text', '#1E293B')
        primary_color = self.tokens.get('colors', {}).get('primary', '#1B2A4A')
        secondary_color = self.tokens.get('colors', {}).get('secondary', '#3B82F6')
        accent_color = self.tokens.get('colors', {}).get('accent', '#F59E0B')

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        :root {{
            --primary: {primary_color};
            --secondary: {secondary_color};
            --accent: {accent_color};
            --bg: {bg_color};
            --text: {text_color};
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: {font_family};
            background-color: var(--bg);
            color: var(--text);
            overflow-x: hidden;
            scroll-behavior: smooth;
        }}
        
        .slides-container {{
            display: grid;
            grid-template-rows: auto;
            width: 100%;
        }}

        .slide {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
            box-sizing: border-box;
            border-bottom: 2px solid #E2E8F0;
            opacity: 0;
            animation: fadeIn 1s forwards;
        }}

        @keyframes fadeIn {{
            to {{ opacity: 1; }}
        }}

        .title {{ font-size: 4rem; font-weight: 700; color: var(--primary); margin-bottom: 1rem; }}
        .subtitle {{ font-size: 2.5rem; font-weight: 600; color: var(--secondary); max-width: 900px; }}
        .thesis {{ font-size: 3rem; font-weight: 600; max-width: 1000px; line-height: 1.4; }}
        .icon {{ font-size: 5rem; margin-bottom: 2rem; color: var(--secondary); }}
        .number {{ font-size: 1.5rem; color: #64748B; margin-top: 3rem; font-weight: 600; }}
        
        .cta-button {{
            display: inline-block;
            margin-top: 3rem;
            padding: 1.5rem 3rem;
            background-color: var(--accent);
            color: #fff;
            text-decoration: none;
            font-size: 2rem;
            border-radius: 12px;
            font-weight: 700;
            transition: transform 0.3s, background-color 0.3s;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .cta-button:hover {{ 
            background-color: #D97706; 
            transform: translateY(-5px);
        }}
    </style>
</head>
<body>
    <div class="slides-container">
        {slides_html}
    </div>
</body>
</html>"""

    def save_presentation(self, html: str, output_path: str = 'output/presentation.html') -> None:
        """Сохраняет сгенерированный HTML в файл."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    def _create_slide_html(self, content: str, slide_number: int, total: int) -> str:
        """Генерирует разметку для отдельного слайда с тезисом."""
        return f"""
        <div class="slide">
            <div class="icon">✨</div>
            <div class="thesis">{content}</div>
            <div class="number">Слайд {slide_number} из {total}</div>
        </div>"""

    def _create_title_slide(self, title: str, subtitle: str) -> str:
        """Генерирует разметку для заглавного слайда."""
        return f"""
        <div class="slide">
            <h1 class="title">{title}</h1>
            <h2 class="subtitle">{subtitle}</h2>
        </div>"""

    def _create_cta_slide(self, cta_text: str, url: str) -> str:
        """Генерирует разметку для финального слайда с призывом к действию."""
        return f"""
        <div class="slide">
            <h1 class="title">Готовы начать?</h1>
            <div class="subtitle">{cta_text}</div>
            <a href="{url}" class="cta-button">Узнать подробности</a>
        </div>"""
