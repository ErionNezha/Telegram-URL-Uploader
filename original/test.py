import subprocess

import aiofiles
import aiohttp
import asyncio

async def download_file(url, file_name):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(file_name, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await f.write(chunk)
                    print("FILE DOWNLOADED: " + file_name)
                    return file_name
                else:
                    print("ERROR DOWNLOADING")
                    return False

    except:
        print("ERROR DOWNLOADING")
        return False

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(float(result.stdout))
    return float(result.stdout)