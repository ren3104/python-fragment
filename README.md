# python-fragment
<p align="center">
  <a href="https://github.com/ren3104/python-fragment/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ren3104/python-fragment" alt="GitHub license"></a>
  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/v/python-fragment?color=blue" alt="PyPi package version"></a>
  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/pyversions/python-fragment.svg" alt="Supported python versions"></a>
</p>

## Features
- Fast and asynchronous
- Fully typed
- Easy to contribute and use

## Installation
```shell
pip install -U python-fragment
```
Or using poetry:
```shell
poetry add python-fragment
```

## Quick Start
```python
from fragment import FragmentAPI

import asyncio


async def main():
    api = FragmentAPI()
    async with api:
        # Get username auctions
        usernames = await api.usernames.search()
        for username in usernames[:5]:
            print(username)
            # {
            #     'username': 'lynx',
            #     'status': 'auction',
            #     'value': 6619.0,
            #     'datetime': '2023-10-31T06:11:25+00:00',
            #     'is_resale': False
            # }


asyncio.run(main())
```
