import time
from fizzbuzz import fizzbuzz_range, LIMIT

VERZIO = "v1"


def main():
    print(f"[{VERZIO}] FizzBuzz indul, felső határ = {LIMIT}", flush=True)
    while True:
        eredmeny = fizzbuzz_range(LIMIT)
        print(
            f"[{VERZIO}] {LIMIT}-ig: ... {' '.join(eredmeny[-5:])}",
            flush=True)
        print(f"[{VERZIO}] elemszám: {len(eredmeny)}", flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
