# services/knowledge_service.py
from .base_service import BaseService
import os
import aiohttp
import asyncio
from datetime import datetime
import json
from pathlib import Path
import pyinotify

class KnowledgeService(BaseService):
    def __init__(self):
        super().__init__()
        self.obsidian_path = os.getenv('OBSIDIAN_SYNC_DIR')
        self.berkeley_api_key = os.getenv('BERKELEY_API_KEY')
        self.calcentral_token = os.getenv('CALCENTRAL_ACCESS_TOKEN')

    async def analyze_obsidian_vault(self):
        vault_data = {
            'notes': [],
            'tags': set(),
            'links': [],
            'daily_notes': [],
            'metadata': {}
        }

        try:
            vault_path = Path(self.obsidian_path)
            for file_path in vault_path.rglob('*.md'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Basic file metadata
                    stats = file_path.stat()
                    file_data = {
                        'name': file_path.name,
                        'path': str(file_path.relative_to(vault_path)),
                        'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        'size': stats.st_size,
                        'tags': self._extract_tags(content),
                        'links': self._extract_links(content),
                        'word_count': len(content.split())
                    }
                    
                    vault_data['notes'].append(file_data)
                    vault_data['tags'].update(file_data['tags'])
                    vault_data['links'].extend(file_data['links'])

            vault_data['tags'] = list(vault_data['tags'])
            vault_data['metadata'] = {
                'total_notes': len(vault_data['notes']),
                'total_tags': len(vault_data['tags']),
                'total_links': len(vault_data['links'])
            }

        except Exception as e:
            self.logger.error(f"Error analyzing Obsidian vault: {str(e)}")

        return vault_data

    def _extract_tags(self, content):
        import re
        tags = re.findall(r'#[\w/\-]+', content)
        return [tag.strip('#') for tag in tags]

    def _extract_links(self, content):
        import re
        links = re.findall(r'\[\[(.*?)\]\]', content)
        return links

    async def get_berkeley_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._get_course_schedule(session),
                self._get_library_usage(session),
                self._get_campus_access(session)
            ]
            schedule, library, access = await asyncio.gather(*tasks)
            
            return {
                'course_schedule': schedule,
                'library_usage': library,
                'campus_access': access
            }

    async def _get_course_schedule(self, session):
        url = "https://api.berkeley.edu/calcentral/v1/academics/schedule"
        headers = {"Authorization": f"Bearer {self.calcentral_token}"}
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def _get_library_usage(self, session):
        url = "https://api.berkeley.edu/library/v1/usage"
        headers = {"Authorization": f"Bearer {self.berkeley_api_key}"}
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def _get_campus_access(self, session):
        url = "https://api.berkeley.edu/access/v1/logs"
        headers = {"Authorization": f"Bearer {self.berkeley_api_key}"}
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def fetch_data(self, start_date: str, end_date: str):
        tasks = [
            self.analyze_obsidian_vault(),
            self.get_berkeley_data()
        ]
        
        obsidian_data, berkeley_data = await asyncio.gather(*tasks)
        
        return {
            "obsidian": obsidian_data,
            "berkeley": berkeley_data
        }
