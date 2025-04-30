# services/financial_service.py
from .base_service import BaseService
import plaid
from plaid.api import plaid_api
import iblib
from datetime import datetime
import os
import aiohttp
import asyncio

class FinancialService(BaseService):
    def __init__(self):
        super().__init__()
        self.plaid_client = None
        self.ibkr_client = None
        self.acorns_session = None

    async def initialize_plaid(self):
        if not self.plaid_client:
            configuration = plaid.Configuration(
                host=plaid.Environment.Development,
                api_key={
                    'clientId': os.getenv('PLAID_CLIENT_ID'),
                    'secret': os.getenv('PLAID_SECRET'),
                }
            )
            self.plaid_client = plaid_api.PlaidApi(plaid.ApiClient(configuration))

    async def initialize_ibkr(self):
        if not self.ibkr_client:
            self.ibkr_client = iblib.Connection(
                os.getenv('IBKR_API_KEY'),
                os.getenv('IBKR_ACCOUNT_ID')
            )

    async def get_boa_data(self):
        await self.initialize_plaid()
        try:
            response = await self.plaid_client.accounts_get({
                'access_token': os.getenv('BOA_ACCESS_TOKEN')
            })
            transactions = await self.plaid_client.transactions_get({
                'access_token': os.getenv('BOA_ACCESS_TOKEN'),
                'start_date': datetime.now() - timedelta(days=30),
                'end_date': datetime.now()
            })
            return {
                'accounts': response.accounts,
                'transactions': transactions.transactions
            }
        except Exception as e:
            self.logger.error(f"BOA data fetch error: {str(e)}")
            return {}

    async def get_hsbc_data(self):
        await self.initialize_plaid()
        try:
            response = await self.plaid_client.accounts_get({
                'access_token': os.getenv('HSBC_ACCESS_TOKEN')
            })
            transactions = await self.plaid_client.transactions_get({
                'access_token': os.getenv('HSBC_ACCESS_TOKEN'),
                'start_date': datetime.now() - timedelta(days=30),
                'end_date': datetime.now()
            })
            return {
                'accounts': response.accounts,
                'transactions': transactions.transactions
            }
        except Exception as e:
            self.logger.error(f"HSBC data fetch error: {str(e)}")
            return {}

    async def get_ibkr_data(self):
        await self.initialize_ibkr()
        try:
            portfolio = await self.ibkr_client.portfolio_summary()
            positions = await self.ibkr_client.positions()
            trades = await self.ibkr_client.trades()
            return {
                'portfolio': portfolio,
                'positions': positions,
                'trades': trades
            }
        except Exception as e:
            self.logger.error(f"IBKR data fetch error: {str(e)}")
            return {}

    async def get_acorns_data(self):
        # Note: Acorns doesn't provide an official API
        # This is a placeholder for when/if they do
        return {}

    async def fetch_data(self, start_date: str, end_date: str):
        tasks = [
            self.get_boa_data(),
            self.get_hsbc_data(),
            self.get_ibkr_data(),
            self.get_acorns_data()
        ]
        
        boa, hsbc, ibkr, acorns = await asyncio.gather(*tasks)
        
        return {
            "bank_of_america": boa,
            "hsbc": hsbc,
            "interactive_brokers": ibkr,
            "acorns": acorns
        }
