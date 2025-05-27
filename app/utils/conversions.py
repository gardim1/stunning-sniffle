from functools import lru_cache

@lru_cache(maxsize=32)
def pixels_to_mm(pixels: int, mm_por_pixel: float = 0.0927) -> float:
    return pixels * mm_por_pixel

#pixel pra mm