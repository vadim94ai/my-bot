import asyncio
import os
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class VideoAgent(BaseAgent):
    """
    Агент для создания видеоматериалов, субтитров и презентаций.
    """
    
    @property
    def stage_name(self) -> str:
        return 'video'

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента для генерации видео-ассетов.
        """
        self.log("Начало работы видео-агента")
        
        try:
            marketing_data = self.load_previous_stage('marketing')
            copywriting_data = self.load_previous_stage('copywriting')
            
            key_theses = marketing_data.get('key_messages', [])
            reels_script = copywriting_data.get('reels_script', {})
            
            slides = self._generate_slides(key_theses)
            vtt_content = self._generate_subtitles_vtt(reels_script)
            reels_data = self._prepare_reels_data(reels_script)
            
            os.makedirs('build/assets', exist_ok=True)
            with open('build/assets/presentation.html', 'w', encoding='utf-8') as f:
                f.write(slides)
                
            with open('build/assets/subtitles.vtt', 'w', encoding='utf-8') as f:
                f.write(vtt_content)
                
            self.save_output(reels_data, 'reels_script.json')
            
            output_data = {
                "slides_generated": True,
                "subtitles_generated": True,
                "reels_prepared": True,
                "files": [
                    "build/assets/presentation.html",
                    "build/assets/subtitles.vtt",
                    "output/reels_script.json"
                ]
            }
            
            self.save_output(output_data, f"{self.stage_name}_output.json")
            self.log("Работа видео-агента успешно завершена")
            return output_data
            
        except Exception as e:
            self.log(f"Произошла ошибка при создании видеоматериалов: {e}", level="ERROR")
            return {}
            
    def _generate_slides(self, theses: list) -> str:
        """
        Генерирует HTML-презентацию на основе тезисов.
        """
        slides_html = "<html><body>"
        for i, thesis in enumerate(theses[:5]): # Берем первые 5 для примера
            slides_html += f"<div class='slide'><h2>Слайд {i+1}</h2><p>{thesis}</p></div>"
        slides_html += "</body></html>"
        return slides_html
        
    def _generate_subtitles_vtt(self, reels_script: dict) -> str:
        """
        Генерирует VTT файл субтитров.
        """
        vtt = "WEBVTT\n\n"
        vtt += "00:00:00.000 --> 00:00:20.000\n"
        vtt += f"{reels_script.get('0-20s', '')}\n\n"
        vtt += "00:00:20.000 --> 00:00:50.000\n"
        vtt += f"{reels_script.get('20-50s', '')}\n\n"
        vtt += "00:00:50.000 --> 00:01:00.000\n"
        vtt += f"{reels_script.get('50-60s', '')}\n"
        return vtt
        
    def _prepare_reels_data(self, reels_script: dict) -> dict:
        """
        Подготавливает данные для рилс.
        """
        return {
            "title": "Сценарий для Reels",
            "duration": "60s",
            "segments": reels_script
        }
