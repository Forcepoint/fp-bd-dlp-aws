import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='add_key')
    parser.add_argument('--key', action="store", dest='key', )
    args = parser.parse_args()
    if args.key == 'None' or not args.key:
        args.key = None
    if args.key:
        f = open("constant.py", "w")
        aes_string = f'{args.key}'
        array_of_bytes = aes_string.split()
        count = 0
        for stuff in array_of_bytes:
            array_of_bytes[count] = int(stuff)
            count += 1
        save_my_bytes = bytes(bytearray(array_of_bytes))
        f.write(f'AES = {save_my_bytes}\n')
        f.close()
    else:
        f = open("constant.py", "w")
        f.write(f'AES = {args.key}\n')
        f.close()