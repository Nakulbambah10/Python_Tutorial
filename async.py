import asyncio
import aiohttp
import time
from typing import Any

class RateLimitedAPIClient:
    def __init__(self, base_url: str, max_requests: int, period: float, concurrency: int = 5):
        """
        Initialize the API client with rate limits and concurrency control.
        
        :param base_url: The base URL of the API.
        :param max_requests: Maximum requests allowed within the period.
        :param period: Time window for the rate limit in seconds.
        :param concurrency: Maximum number of concurrent requests.
        """
        self.base_url = base_url
        self.max_requests = max_requests
        self.period = period
        self.semaphore = asyncio.Semaphore(concurrency)
        self.session = aiohttp.ClientSession()
        self.request_times = []  # Track request timestamps

    async def _throttle(self):
        """Ensure requests do not exceed the rate limit."""
        while len(self.request_times) >= self.max_requests:
            elapsed = time.monotonic() - self.request_times[0]
            if elapsed < self.period:
                await asyncio.sleep(self.period - elapsed)
            self.request_times.pop(0)  # Remove old request timestamps

        self.request_times.append(time.monotonic())

    async def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Make an API request with rate limiting and concurrency control.

        :param method: HTTP method (GET, POST, etc.).
        :param endpoint: API endpoint.
        :param kwargs: Additional request arguments.
        :return: JSON response or None in case of failure.
        """
        url = f"{self.base_url}{endpoint}"

        async with self.semaphore:  # Limit concurrent requests
            await self._throttle()  # Enforce rate limit

            for attempt in range(3):  # Retry up to 3 times
                try:
                    async with self.session.request(method, url, **kwargs) as response:
                        if response.status == 429:  # Rate limited
                            retry_after = int(response.headers.get("Retry-After", 1))
                            await asyncio.sleep(retry_after)
                            continue
                        response.raise_for_status()
                        return await response.json()
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    print(f"Request failed: {e}, retrying... ({attempt+1}/3)")
                    await asyncio.sleep(2**attempt)  # Exponential backoff

        return None  # Return None if all retries fail

    async def close(self):
        """Close the aiohttp session properly."""
        await self.session.close()

# Example Usage
async def main():
    client = RateLimitedAPIClient("https://api.example.com", max_requests=5, period=10, concurrency=2)

    tasks = [client.request("GET", "/data") for _ in range(10)]
    results = await asyncio.gather(*tasks)

    await client.close()
    print(results)

asyncio.run(main())
