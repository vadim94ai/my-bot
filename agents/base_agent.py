import json
import os
import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """
    Базовый класс для всех агентов.
    """
    def __init__(self, config_path: str = 'configs/project_config.json'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Загружает конфигурацию проекта.
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            self.log(f"Конфигурационный файл {self.config_path} не найден. Используется пустая конфигурация.", level="WARNING")
            return {}
        except Exception as e:
            self.log(f"Ошибка при загрузке конфигурации: {e}", level="ERROR")
            return {}

    @property
    @abstractmethod
    def stage_name(self) -> str:
        """
        Имя стадии пайплайна (например, 'marketing', 'copywriting').
        """
        pass

    @abstractmethod
    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Запускает агента.
        """
        pass

    def save_output(self, data: Dict[str, Any], filename: str) -> None:
        """
        Сохраняет данные в формате JSON в директорию output/.
        """
        try:
            os.makedirs('output', exist_ok=True)
            filepath = os.path.join('output', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.log(f"Данные успешно сохранены в {filepath}")
        except Exception as e:
            self.log(f"Ошибка при сохранении файла {filename}: {e}", level="ERROR")

    def load_previous_stage(self, stage_name: str) -> Dict[str, Any]:
        """
        Загружает результаты предыдущей стадии.
        """
        try:
            filepath = os.path.join('output', f"{stage_name}_output.json")
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            self.log(f"Файл {filepath} не найден.", level="WARNING")
            return {}
        except Exception as e:
            self.log(f"Ошибка при загрузке данных стадии {stage_name}: {e}", level="ERROR")
            return {}

    def log(self, message: str, level: str = 'INFO') -> None:
        """
        Выводит лог с отметкой времени и именем стадии.
        """
        timestamp = datetime.datetime.now().isoformat()
        print(f"[{timestamp}] [{level}] [{self.stage_name.upper()}]: {message}")
