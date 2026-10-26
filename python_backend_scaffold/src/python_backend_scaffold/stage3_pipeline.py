import asyncio
from collections.abc import Awaitable, Callable, Iterator
from dataclasses import dataclass
from functools import wraps
from time import perf_counter


def measured[**P, R](
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started = perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            print(f"总耗时：{perf_counter() - started:.4f}s")

    return wrapper


@dataclass(frozen=True)
class Job:
    item_id: int


@dataclass
class Report:
    succeeded: int = 0
    timed_out: int = 0
    active: int = 0
    peak: int = 0

    def __call__(self) -> dict[str, int]:
        return {"succeeded": self.succeeded, "timed_out": self.timed_out}

    def __str__(self) -> str:
        return f"成功={self.succeeded}，超时={self.timed_out}，峰值并发={self.peak}"


def iter_jobs(total: int) -> Iterator[Job]:
    for item_id in range(total):
        yield Job(item_id)


async def enrich(job: Job) -> int:
    if job.item_id == 7:
        await asyncio.Event().wait()  # 确定性地等待，直到外部超时取消。
    await asyncio.sleep(0.01)
    return job.item_id * 10


async def worker(queue: asyncio.Queue[Job | None], report: Report) -> None:
    while True:
        job = await queue.get()
        try:
            if job is None:
                return

            report.active += 1
            report.peak = max(report.peak, report.active)
            try:
                async with asyncio.timeout(0.2):
                    result = await enrich(job)
                assert result == job.item_id * 10
                report.succeeded += 1
            except TimeoutError:
                report.timed_out += 1
            finally:
                report.active -= 1
        finally:
            queue.task_done()


@measured
async def run_pipeline() -> Report:
    worker_count = 3
    queue: asyncio.Queue[Job | None] = asyncio.Queue(maxsize=6)
    report = Report()

    async with asyncio.TaskGroup() as group:
        for _ in range(worker_count):
            group.create_task(worker(queue, report))

        for job in iter_jobs(12):
            await queue.put(job)

        for _ in range(worker_count):
            await queue.put(None)

        await queue.join()

    assert report() == {"succeeded": 11, "timed_out": 1}
    assert report.active == 0
    assert 1 <= report.peak <= worker_count
    assert queue.empty()
    return report


if __name__ == "__main__":
    print(asyncio.run(run_pipeline()))
