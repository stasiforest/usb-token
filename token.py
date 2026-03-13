#!/usr/bin/env python3
import argparse


def usb_crc5(addr: int, endp: int) -> int:
    data = addr | (endp << 7)
    crc = 0x1F

    for i in range(11):
        bit = (data >> i) & 1
        c = (crc & 1) ^ bit
        crc >>= 1
        if c:
            crc ^= 0x14

    crc ^= 0x1F
    return crc & 0x1F


def usb_token(pid: int, addr: int, endp: int) -> bytes:
    crc5 = usb_crc5(addr, endp)
    token = addr | (endp << 7) | (crc5 << 11)

    b0 = pid
    b1 = token & 0xFF
    b2 = (token >> 8) & 0xFF

    return bytes([b0, b1, b2])


def main():
    parser = argparse.ArgumentParser(description="USB token generator")
    parser.add_argument("-a", "--addr", type=int, required=True, help="USB device address (0-127)")
    parser.add_argument("-e", "--endpoint", type=int, required=True, help="USB endpoint (0-15)")
    parser.add_argument("-p", "--pid", type=lambda x: int(x,0), default=0xE1,
                        help="PID byte (default 0xE1)")

    args = parser.parse_args()

    frame = usb_token(args.pid, args.addr, args.endpoint)

    print(" ".join(f"{b:02X}" for b in frame))


if __name__ == "__main__":
    main()
