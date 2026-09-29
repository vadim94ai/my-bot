import math
from pathlib import Path

class SubtitlesGenerator:
    """Генератор субтитров в формате WebVTT."""

    def generate_vtt(self, text: str, words_per_minute: int = 150) -> str:
        """
        Разбивает текст на сегменты и генерирует WebVTT субтитры
        с рассчитанными таймингами на основе скорости речи.
        """
        words = text.split()
        words_per_second = words_per_minute / 60.0
        
        # Около 10 слов на один сегмент субтитров
        segment_size = 10
        segments = []
        
        current_time = 0.0
        for i in range(0, len(words), segment_size):
            chunk = words[i:i+segment_size]
            chunk_duration = len(chunk) / words_per_second
            
            start_time = current_time
            end_time = current_time + chunk_duration
            
            segments.append({
                'start': start_time,
                'end': end_time,
                'text': ' '.join(chunk)
            })
            
            # Небольшая пауза между сегментами
            current_time = end_time + 0.1 
            
        vtt_lines = ["WEBVTT\n"]
        for i, seg in enumerate(segments, 1):
            start_str = self._format_timestamp(seg['start'])
            end_str = self._format_timestamp(seg['end'])
            
            vtt_lines.append(f"{i}")
            vtt_lines.append(f"{start_str} --> {end_str}")
            vtt_lines.append(f"{seg['text']}\n")
            
        return "\n".join(vtt_lines)

    def save_vtt(self, vtt_content: str, output_path: str = 'output/subtitles.vtt') -> None:
        """Сохраняет сгенерированные субтитры в файл .vtt."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(vtt_content)

    def _format_timestamp(self, seconds: float) -> str:
        """Конвертирует время в секундах в формат WebVTT HH:MM:SS.mmm."""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int(round((seconds - int(seconds)) * 1000))
        
        if ms >= 1000:
            ms -= 1000
            s += 1
            if s >= 60:
                s -= 60
                m += 1
                if m >= 60:
                    m -= 60
                    h += 1

        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
