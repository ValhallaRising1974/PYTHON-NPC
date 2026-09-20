#!/usr/bin/env python3
"""Reference-level verification of the firmware's RLE format and vectors."""

from pathlib import Path


def rle(data: bytes) -> bytes:
    if not data:
        return b""
    output = bytearray()
    current = data[0]
    count = 1
    for value in data[1:]:
        if value == current and count < 255:
            count += 1
        else:
            output.extend((count, current))
            current, count = value, 1
    output.extend((count, current))
    return bytes(output)


source = bytes((10, 10, 10, 20, 20, 30, 40, 40, 40, 40, 40))
expected = bytes((3, 10, 2, 20, 1, 30, 5, 40))
assert rle(source) == expected
assert rle(b"") == b""
assert rle(bytes([7]) * 256) == bytes((255, 7, 1, 7))

required = {
    "startup.s": (".word _estack", ".word Reset_Handler", "_sbss", "_ebss", "bl main"),
    "linker.ld": ("KEEP(*(.isr_vector))", "ORIGIN = 0x00000000", "_estack"),
    "rle.s": ("rle_compress:", "cmp r4, #255", "strb r4", "strb r3"),
}
root = Path(__file__).parent
for filename, markers in required.items():
    text = (root / filename).read_text(encoding="utf-8")
    for marker in markers:
        assert marker in text, f"Missing {marker!r} in {filename}"

print("PASS: reference RLE and source-structure checks completed.")
