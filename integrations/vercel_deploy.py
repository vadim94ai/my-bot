"""
Модуль для деплоя файлов на Vercel.
"""
import os
import base64
import logging
import httpx
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class VercelDeployer:
    """Класс для работы с Vercel API."""

    def __init__(self, token: str, project_id: str = '', org_id: str = '') -> None:
        """
        Инициализация деплоера Vercel.
        
        :param token: Vercel Access Token
        :param project_id: ID проекта Vercel
        :param org_id: ID организации или команды Vercel
        """
        self.token = token
        self.project_id = project_id
        self.org_id = org_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _read_directory_files(self, directory: str) -> List[Dict[str, str]]:
        """
        Рекурсивное чтение файлов из директории и их кодирование в base64.
        
        :param directory: Путь к директории
        :return: Список файлов в нужном для Vercel API формате
        """
        files_data = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory).replace("\\", "/")
                
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
                encoded_content = base64.b64encode(content).decode('utf-8')
                
                files_data.append({
                    "file": rel_path,
                    "data": encoded_content,
                    "encoding": "base64"
                })
        return files_data

    async def deploy(self, directory: str = 'landing', project_name: str = 'infoproduct-landing') -> Dict[str, Any]:
        """
        Создание деплоя через Vercel API v13.
        
        :param directory: Директория с файлами для деплоя
        :param project_name: Название проекта
        :return: Информация о деплое (URL, статус, ID)
        """
        files = self._read_directory_files(directory)
        
        payload = {
            "name": project_name,
            "files": files,
            "target": "production"
        }
        
        url = "https://api.vercel.com/v13/deployments"
        params = {}
        if self.org_id:
            params['teamId'] = self.org_id

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                "url": data.get("url"),
                "deployment_id": data.get("id"),
                "status": data.get("readyState"),
                "created_at": data.get("createdAt")
            }

    async def get_deployment_status(self, deployment_id: str) -> str:
        """
        Получение статуса конкретного деплоя.
        
        :param deployment_id: ID деплоя
        :return: Статус деплоя в виде строки
        """
        url = f"https://api.vercel.com/v13/deployments/{deployment_id}"
        params = {}
        if self.org_id:
            params['teamId'] = self.org_id
            
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("readyState", "UNKNOWN")

    async def list_deployments(self) -> List[Dict[str, Any]]:
        """
        Список всех деплоев в проекте.
        
        :return: Список деплоев
        """
        url = "https://api.vercel.com/v6/deployments"
        params = {}
        if self.project_id:
            params['projectId'] = self.project_id
        if self.org_id:
            params['teamId'] = self.org_id
            
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("deployments", [])
