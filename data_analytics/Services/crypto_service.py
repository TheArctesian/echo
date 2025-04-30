# services/crypto_service.py
from .base_service import BaseService
from web3 import Web3
import aiohttp
import asyncio
import os
from datetime import datetime

class CryptoService(BaseService):
    def __init__(self):
        super().__init__()
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL')))
        self.zapper_api_key = os.getenv('ZAPPER_API_KEY')
        self.moon_wallet_api_key = os.getenv('MOON_WALLET_API_KEY')

    async def get_zapper_portfolio(self, address):
        async with aiohttp.ClientSession() as session:
            url = f"https://api.zapper.fi/v2/portfolio"
            headers = {
                "Authorization": f"Basic {self.zapper_api_key}",
                "Accept": "application/json"
            }
            params = {
                "addresses[]": address,
                "network": "ethereum"
            }
            async with session.get(url, headers=headers, params=params) as response:
                return await response.json()

    async def get_moon_wallet_data(self, address):
        # Moon wallet API integration
        # This is a placeholder as Moon wallet's API specifics aren't public
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.moon_wallet_api_key}"}
            # Replace with actual Moon wallet API endpoint
            url = f"https://api.moonwallet.com/v1/wallet/{address}"
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def get_ethereum_balance(self, address):
        balance = self.web3.eth.get_balance(address)
        return self.web3.from_wei(balance, 'ether')

    async def fetch_data(self, start_date: str, end_date: str):
        addresses = os.getenv('ETHEREUM_ADDRESSES', '').split(',')
        
        all_data = {
            'zapper': {},
            'moon_wallet': {},
            'ethereum': {}
        }

        for address in addresses:
            tasks = [
                self.get_zapper_portfolio(address),
                self.get_moon_wallet_data(address),
                self.get_ethereum_balance(address)
            ]
            
            zapper_data, moon_data, eth_balance = await asyncio.gather(*tasks)
            
            all_data['zapper'][address] = zapper_data
            all_data['moon_wallet'][address] = moon_data
            all_data['ethereum'][address] = float(eth_balance)

        return all_data
