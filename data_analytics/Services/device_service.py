# services/device_service.py
from .base_service import BaseService
import asyncio
import aiohttp
import os
import subprocess
import json
from datetime import datetime

class DeviceService(BaseService):
    def __init__(self):
        super().__init__()
        self.heatbit_api_key = os.getenv('HEATBIT_API_KEY')
        self.samsung_tv_ip = os.getenv('SAMSUNG_TV_IP')
        self.samsung_tv_token = os.getenv('SAMSUNG_TV_TOKEN')

    async def get_heatbit_data(self):
        async with aiohttp.ClientSession() as session:
            url = "https://api.heatbit.com/v1/metrics"
            headers = {"Authorization": f"Bearer {self.heatbit_api_key}"}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return {
                    'mining_stats': data.get('mining_stats', {}),
                    'heating_stats': data.get('heating_stats', {}),
                    'power_consumption': data.get('power_consumption', {}),
                    'temperature': data.get('temperature', {})
                }

    async def get_samsung_tv_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self.samsung_tv_ip}:8001/api/v2/"
                headers = {"Authorization": f"Bearer {self.samsung_tv_token}"}
                
                async with session.get(f"{url}applications", headers=headers) as response:
                    apps_data = await response.json()
                
                async with session.get(f"{url}usage", headers=headers) as response:
                    usage_data = await response.json()
                
                return {
                    'applications': apps_data,
                    'usage_stats': usage_data
                }
        except Exception as e:
            self.logger.error(f"Samsung TV data fetch error: {str(e)}")
            return {}

    async def get_linux_system_data(self):
        try:
            systems = ['pop-os', 'zorin', 'arch']
            system_data = {}

            for system in systems:
                # This assumes SSH access is configured for each system
                # Replace with actual hostnames/IPs
                hostname = os.getenv(f'{system.upper()}_HOSTNAME')
                if not hostname:
                    continue

                # Execute commands remotely
                commands = [
                    "uptime",
                    "free -m",
                    "df -h",
                    "top -bn1",
                    "journalctl --since '1 hour ago' -n 100",
                    "gnome-shell --version",
                    "ps aux | grep gnome"
                ]

                system_data[system] = {}
                
                for cmd in commands:
                    try:
                        result = await asyncio.create_subprocess_shell(
                            f"ssh {hostname} {cmd}",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        stdout, stderr = await result.communicate()
                        
                        cmd_name = cmd.split()[0]
                        system_data[system][cmd_name] = stdout.decode()
                    except Exception as e:
                        self.logger.error(f"Error executing {cmd} on {system}: {str(e)}")

            return system_data

        except Exception as e:
            self.logger.error(f"Linux system data fetch error: {str(e)}")
            return {}

    async def fetch_data(self, start_date: str, end_date: str):
        tasks = [
            self.get_heatbit_data(),
            self.get_samsung_tv_data(),
            self.get_linux_system_data()
        ]
        
        heatbit, samsung_tv, linux = await asyncio.gather(*tasks)
        
        return {
            "heatbit": heatbit,
            "samsung_tv": samsung_tv,
            "linux_systems": linux
        }
