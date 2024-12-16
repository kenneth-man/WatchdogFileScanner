import aiohttp
import asyncio

# When you create a function with 'async' keyword it becomes a 'Coroutine' function
# Returns a 'Coroutine' object when called https://docs.python.org/3/library/asyncio-task.html
# In this case, it returns 'Coroutine' object that wraps a 'ClientResponse' object
async def getFetch(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status != 200:
				print(f"{response.status} Error")
			print(f"Returning response for {url}")
			return response

async def main():
	# Tasks are used to run coroutines concurrently
	task1 = asyncio.create_task(getFetch("https://google.com"))
	task2 = asyncio.create_task(getFetch("https://linkedin.com"))
	task3 = asyncio.create_task(getFetch("https://facebook.com"))

	result1 = await task1
	result2 = await task2
	result3 = await task3

	print(result1, "\n", result2, "\n", result3)

if __name__ == "__main__":
	asyncio.run(main())