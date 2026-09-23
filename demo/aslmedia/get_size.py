import aiohttp
import asyncio

async def get_file_size(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url, allow_redirects=True) as response:
            if response.status == 200:
                file_size = response.headers.get('content-length')

                if file_size:
                    file_size = int(file_size)
                    if file_size < 1024:
                        return f"{file_size} B", file_size
                    elif file_size < 1024 * 1024:
                        return f"{file_size / 1024:.2f} KB", file_size
                    else:
                        return f"{file_size / (1024 * 1024):.2f} MB", file_size
                else:
                    return False
            else:
                return False


async def get_size(url):
    file_size = await get_file_size(url)
    if file_size:
        mb, bytes = file_size
        if int(bytes) > 2097152000:
            return {'ok': False, 'size': mb}
        else:
            return {'ok': True, 'size': mb}
