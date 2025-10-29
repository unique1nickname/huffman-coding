import pickle as pl
import argparse, os

def main():
    args = getArgs()
    match args.mode.lower():
        case 'encode':
            encode(args.path)
        case 'decode':
            decode(args.path) 

def getArgs():
    ap = argparse.ArgumentParser(description='Encodes and decodes text using the Huffman method')
    ap.add_argument('mode', type=str, help='Choose between "encode" and "decode" modes')
    ap.add_argument('path', type=str, help='Path to the file')
    return ap.parse_args()

def encode(path):
    with open(path, 'r') as file:
        text = file.read()
    symbolFrequency = dict()

    for i in text:
        if i in symbolFrequency:
            symbolFrequency[i] += 1
        else:
            symbolFrequency[i] = 1

    symbols = sorted(symbolFrequency.items(), key=lambda item : item[1])
    print(symbols)

    symbolCodes = dict()
    while len(symbols) > 1:
        for x in range(2):
            for i in symbols[x][0]:
                if i in symbolCodes:
                    symbolCodes[i] = str(1-x) + symbolCodes[i]
                else:
                    symbolCodes[i] = str(1-x)
        symbols.append(
            (
                symbols[0][0]+symbols[1][0],
                symbols[0][1]+symbols[1][1]
            )
        )
        symbols.pop(1)
        symbols.pop(0)
        symbols.sort(key=lambda item : item[1])

    newText = ''
    for i in text:
        newText += symbolCodes[i]

    print(newText)

    dirPath, fileName = os.path.split(path)
    fileName = os.path.splitext(fileName)[0]

    binData = int(newText, 2).to_bytes((len(newText) + 7) // 8, byteorder='big')
    print(binData)
    with open(f'{dirPath}{fileName}.huffman', 'wb') as f:
        pl.dump((symbolCodes, binData), f)

def decode(path):
    with open(path, 'rb') as file:
        data = pl.load(file)

    symbolCodes = data[0]
    binData = data[1]

    strBin = ''.join(format(byte, '08b') for byte in binData)

    for i in range(len(strBin)):
        if strBin[i] == '1':
            strBin = strBin[i:]
            break

    symbolCodesBack = dict()
    for i in symbolCodes.items():
        symbolCodesBack[i[1]] = i[0]

    textBack = ''
    part = ''
    for i in strBin:
        part += i
        if part in symbolCodesBack:
            textBack += symbolCodesBack[part]
            part = ''

    print(strBin)
    print(textBack)

    dirPath, fileName = os.path.split(path)
    fileName = os.path.splitext(fileName)[0]
    with open(f'{dirPath}{fileName}_decoded.txt', 'w') as f:
        f.write(textBack)

if __name__ == "__main__":
    main()