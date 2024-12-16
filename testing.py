import aiohttp
import asyncio

# https://www.youtube.com/watch?v=Qb9s3UiMSTA

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
	##############
	# Example 1...
	##############
		# Tasks are used to run coroutines concurrently
	# task1 = asyncio.create_task(getFetch("https://google.com"))
	# task2 = asyncio.create_task(getFetch("https://linkedin.com"))
	# task3 = asyncio.create_task(getFetch("https://facebook.com"))

	# result1 = await task1
	# result2 = await task2
	# result3 = await task3

	# print(result1, "\n", result2, "\n", result3)

	##############
	# Example 2...
	##############
		# More concise way using 'asyncio.gather()'
	# results = await asyncio.gather(
	# 	getFetch("https://google.com"),
	# 	getFetch("https://linkedin.com"),
	# 	getFetch("https://facebook.com")
	# )

	# for r in results:
	# 	print(r)


	##############
	# Example 3...
	##############
		# Another way is to use 'asyncio.TaskGroup()' which allows for error handling
	urls = [
		"https://google.com",
		"https://linkedin.com",
		"https://facebook.com"
	]
	tasks = []

	async with asyncio.TaskGroup() as taskGroup:
		for u in urls:
			task = taskGroup.create_task(getFetch(u))
			tasks.append(task)
	
	# After the Task Group block, all tasks have finished
	results = [t.result() for t in tasks]

	for r in results:
		print(r)

if __name__ == "__main__":
	asyncio.run(main())