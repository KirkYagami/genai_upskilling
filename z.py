import asyncio

async def greet():
    print("Hello, starting coroutine!")
    await asyncio.sleep(1)  # Simulate I/O delay
    print("Coroutine complete!")

if __name__ == "__main__":
    asyncio.run(greet())

    
# Output:
# Hello, starting coroutine!
# (1-second pause)
# Coroutine complete!