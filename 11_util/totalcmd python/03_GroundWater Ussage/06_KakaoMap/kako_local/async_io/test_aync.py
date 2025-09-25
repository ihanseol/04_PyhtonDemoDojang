import asyncio


async def task(name, delay):
    print(f"{name} 시작")
    await asyncio.sleep(delay)
    print(f"{name} 끝 (대기 {delay}초)")


async def main():
    # 세 개의 작업을 동시에 실행
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3))


asyncio.run(main())


