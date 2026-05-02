# python-fragment
<p align="center">
  <a href="https://github.com/ren3104/python-fragment/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ren3104/python-fragment" alt="GitHub license"></a>
  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/v/python-fragment?color=blue" alt="PyPi package version"></a>
  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/pyversions/python-fragment.svg" alt="Supported python versions"></a>
</p>

An unofficial Python library for interacting with [Fragment](https://fragment.com). The library scrapes Fragment's HTML pages and exposes a clean, fully typed interface.

## Features
- Both **synchronous** and **asynchronous** clients
- **Fast HTML parsing** powered by [selectolax](https://github.com/rushter/selectolax)
- **Fully typed** - all returned data is described with `TypedDict` schemas
- **Automatic retries** on network failures with exponential back-off

## Installation
```shell
pip install python-fragment
```

**Requirements:** Python 3.9+

## Quick Start

### Async client
```python
import asyncio
import fragment

async def main():
  async with fragment.AsyncClient() as client:
    # Search usernames currently on auction
    usernames = await client.search_usernames(
      query="crypto",
      filter="auction",
      sort="price_desc"
    )
    for u in usernames[:3]:
      print(u)
      # {
      #   'username': 'crypto',
      #   'status': 'auction',
      #   'value': 15000.0,
      #   'datetime': '2024-08-01T12:00:00+00:00',
      #   'is_resale': False
      # }

asyncio.run(main())
```

### Sync client
```python
import fragment

with fragment.Client() as client:
  # Detailed info for a specific username
  info = client.username_info("durov")
  print(info["status"])
  print(info["bid_history"])
  print(info["ownership_history"])
```

## Proxy Usage
Both clients forward `**request_kwargs` directly to the underlying HTTP library, so proxies are configured per-call.

### Async client (`aiohttp`)
Pass a single proxy URL string via the `proxy` keyword argument:

```python
import asyncio
import fragment

PROXY = "http://{user}:{password}@{host}:{port}"

async def main():
  async with fragment.AsyncClient() as client:
    print(await client.username_info("crypto", proxy=PROXY))

asyncio.run(main())
```

### Sync client (`requests`)
Pass a `proxies` dict that maps URL schemes to the proxy URL:

```python
import fragment

PROXY = "http://{user}:{password}@{host}:{port}"

with fragment.Client() as client:
  print(client.username_info("crypto", proxies={"http": PROXY, "https": PROXY}))
```

## Error Handling
```python
import fragment
from fragment.errors import FragmentHTTPError, ParserError


async with fragment.AsyncClient() as client:
  try:
    info = await client.username_info("someusername")
  except FragmentHTTPError as e:
    print(f"HTTP error: {e}")
  except ParserError as e:
    print(f"Failed to parse Fragment HTML: {e}")
```

**`FragmentHTTPError`** - raised when the server returns a non-OK response.

**`ParserError`** - raised when the Fragment page structure has changed and data cannot be extracted.
