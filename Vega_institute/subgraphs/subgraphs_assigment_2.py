#!/usr/bin/env python
# coding: utf-8

# In[85]:


import requests


# In[86]:


import json
import datetime
import pandas as pd


# <strong>Information about UNI (DEX) and UNISWAP-V3</strong>

# In[87]:


url_V3 = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'


# In[88]:


query = f"""{{ 
    tokenDayDatas(
        where: {{token: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"}}, 
        orderBy: date, 
        orderDirection: asc
        ) {{ date
             token {{ symbol totalSupply }}
             volumeUSD
             priceUSD
        }}
    uniswapDayDatas(orderBy: date) {{
         date
         id
         tvlUSD
         volumeUSD
    }}
}}
"""

response = requests.post(url_V3, json={'query': query})
json_data = json.loads(response.text)
data_uni = json_data['data']


# In[89]:


data_token = []
data_uniswap = []
for unix_data in data_uni['tokenDayDatas']:

    date = datetime.datetime.fromtimestamp(unix_data['date'])
    token_symbol = unix_data['token']['symbol']
    token_totalSupply = unix_data['token']['totalSupply']
    token_volumeUSD = unix_data['volumeUSD']
    token_priceUSD = unix_data['priceUSD']
    
    w1 = [date, token_symbol, token_totalSupply, token_volumeUSD, token_priceUSD]
    data_token.append(w1)
    
for unix_data in data_uni['uniswapDayDatas']: 
    
    date = datetime.datetime.fromtimestamp(unix_data['date'])
    uniswap_volumeUSD = unix_data['volumeUSD']
    uniswap_tvlUSD = unix_data['tvlUSD']

    w2 = [date, uniswap_volumeUSD, uniswap_tvlUSD]
    data_uniswap.append(w2)


# In[90]:


import pandas as pd
df_token = pd.DataFrame(data_token)
df_uniswap = pd.DataFrame(data_uniswap)
df_token.columns = ['date', 'symbol', 'totalSupply', 'volumeUSD', 'priceUSD']
df_uniswap.columns = ['date', 'volumeUSD', 'tvlUSD']


# In[91]:


df_token


# In[92]:


df_uniswap


# In[93]:


import  plotly.express as px

df_token['volumeUSD'] = df_token['volumeUSD'].astype(float)
px.line(df_token.sort_values('date'), x = 'date', y = ['volumeUSD'], title="UNI token volume USD (DEX)")


# In[94]:


df_token['priceUSD'] = df_token['priceUSD'].astype(float)
px.line(df_token.sort_values('date'), x = 'date', y = ['priceUSD'], title="UNI token price USD")


# In[95]:


df_uniswap['volumeUSD'] = df_uniswap['volumeUSD'].astype(float)
px.line(df_uniswap.sort_values('date'), x = 'date', y = ['volumeUSD'], title="UNISWAP-V3 Volume USD")


# In[96]:


df_uniswap['tvlUSD'] = df_uniswap['tvlUSD'].astype(float)
px.line(df_uniswap.sort_values('date'), x = 'date', y = ['tvlUSD'], title="UNISWAP-V3 TVL USD")


# <strong>Information about UNISWAP-V2</strong>

# In[97]:


url_V2 = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'


# In[98]:


query_2 = f"""{{ 
    uniswapDayDatas(orderBy: date) {{
         dailyVolumeUSD
         date
         totalLiquidityUSD
    }}
}}
"""
response = requests.post(url_V2, json={'query': query_2})
json_data = json.loads(response.text)
data_uni = json_data['data']


# In[99]:


data_uniswap = []
for unix_data in data_uni['uniswapDayDatas']: 
    
    date = datetime.datetime.fromtimestamp(unix_data['date'])
    uniswap_volumeUSD = unix_data['dailyVolumeUSD']
    uniswap_tvlUSD = unix_data['totalLiquidityUSD']

    w2 = [date, uniswap_volumeUSD, uniswap_tvlUSD]
    data_uniswap.append(w2)


# In[100]:


df_uniswap = pd.DataFrame(data_uniswap)
df_uniswap.columns = ['date', 'volumeUSD', 'tvlUSD']


# In[101]:


df_uniswap


# In[102]:


df_uniswap['volumeUSD'] = df_uniswap['volumeUSD'].astype(float)
px.line(df_uniswap.sort_values('date'), x = 'date', y = ['volumeUSD'], title="UNISWAP-V2 Volume USD")


# In[103]:


df_uniswap['tvlUSD'] = df_uniswap['tvlUSD'].astype(float)
px.line(df_uniswap.sort_values('date'), x = 'date', y = ['tvlUSD'], title="UNISWAP-V2 TVL USD")


# <strong>Information about UNI (CEX) from Binance</strong>

# In[52]:


BASE = 'https://fapi.binance.com'
endpoint = '/fapi/v1/time' 
response = requests.get(BASE + endpoint)


# In[59]:


import pandas as pd
import json
import datetime
from datetime import datetime
class BinanceFuturesConnector:
    
    def __init__(self, api_key: str = '', secret_key: str = ''):
        self._api_key = api_key
        self._secret_key = secret_key
        self._API_URL = 'https://fapi.binance.com' # есть base url (the base inpoint) для доступа к дальнейшим инпоинтам
    def _make_request(self, method: str, endpoint: str, params: dict = None, sign: bool = False, api_url: str = None):
        if sign:
            header = {'X-MBX-APIKEY': self._API_KEY}
            if params is None:
                params = {}
            params['timestamp'] = int(time.time() * 1000 + 1000)
            params['signature'] = self._generate_signature(urlencode(params)) # подписываем при помощи секретного ключа
        else:
            header = None

        if api_url is None:
            api_url = self._API_URL

        if method == "GET":
            response = requests.get(api_url + endpoint, params, headers=header)
        elif method == "POST":
            response = requests.post(api_url + endpoint, params, headers=header)

        if response.status_code == 200:
            return response.json()
        if response.status_code in [404, 503]:
            msg = f'Binance error while requesting {method} {endpoint}: {response.status_code} - {response.reason}'
            raise ConnectionError(msg)

    def get_klines(self, ticker: str, interval: str, start_time: datetime = None, end_time: datetime = None, **kwargs) -> list:
        """
            [
                {
                    'openTime': datetime object,
                    'open': 0.01634790,
                    'high': 0.80000000,
                    'low': 0.01575800,
                    'close': 0.01577100,
                    'volume': 148976.11427815
                }
            ]
        """
        limit = 1500
        params = dict(symbol=ticker, interval=interval, limit=limit)
        if start_time is not None:
            start_time = override_timezone(start_time)
            params['startTime'] = int(start_time.timestamp() * 1000)
        if end_time is not None:
            end_time = override_timezone(end_time)
            params['endTime'] = int(end_time.timestamp() * 1000)

        params.update(kwargs)

        klines = []
        while True:
            response = self._make_request('GET', '/fapi/v1/klines', params)
            for item in response:
                klines.append(
                    dict(
                        openTime=datetime.utcfromtimestamp(item[0] / 1000),
                        open=float(item[1]),
                        high=float(item[2]),
                        low=float(item[3]),
                        close=float(item[4]),
                        volume=float(item[5])
                    )
                )
            if len(response) < limit:
                break

            if start_time is None:
                break

            # shift start time by 1s from the newest loaded datapoint time
            params['startTime'] = response[-1][0] + 1000
        return klines
    


# In[60]:


con = BinanceFuturesConnector()


# In[82]:


data = con.get_klines('UNIUSDT', interval='1d')
df_token = pd.DataFrame(data)


# In[83]:


df_token = df_token[228:328]
df_token 


# In[84]:


df_token['volume'] = df_token['volume'].astype(float)
px.line(df_token.sort_values('openTime'), x = 'openTime', y = ['volume'], title="UNI token volume USD (CEX) on Binance")


# <strong>Uniswap V3 connector</strong>

# In[48]:


import time

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Token:
    address: str
    decimals: str
    symbol: str
    chain: str #его сеть
        
#зададим функцию = по символу будем получать токен = структуру class Token
def symbol_to_token(symbol: str) -> Token:
    tokens = {
                'BUSD': Token('0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', 18, 'BUSD', 'bsc'),
                'USDT': Token('0x55d398326f99059fF775485246999027B3197955', 18, 'BUSD', 'bsc'),
             }
    return tokens[symbol]


# In[49]:



class DexConnector(ABC):
    def __init__(self, wallet_address: str, private_key: str, node: str, **kwargs):
        self.private_key = private_key
        self.wallet_address = wallet_address
    def _make_transaction(self, transaction, **kwargs):
        tx = transaction.buildTransaction({ 'nonce': self.w3.eth.getTransactionCount(self.wallet_address),
                                            'gas': kwargs.get('gas', 2000000),
                                            'gasPrice': int(5*kwargs.get('gasPrice', self.w3.eth.gasPrice + 1000000))
                                         })
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key=self.private_key)
        return self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    @abstractmethod
    def make_market_order(self, ticker: str, side: str, quantity: float, **kwargs) -> dict:
        raise NotImplementedError()
                                                        
    @abstractmethod
    def get_price(self, ticker: str, **kwargs) -> float:
        raise NotImplementedError()


# In[50]:


class UniswapV3Connector(DexConnector):
    # UniV3 ABI
    ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

    
    #self_in The mapping containing all user positions
    #owner The address of the position owner
    #tickLower The lower tick boundary of the position
    #tickUpper The upper tick boundary of the position
    def get_position(self,self_in: dict, owner: str, tickLower: int, tickUpper: int) -> struct Position.Info:
        position = self.contract.functions.get(self_in, owner, tickLower, tickUpper)
        return position
            


# In[ ]:





# In[ ]:





# In[ ]:




