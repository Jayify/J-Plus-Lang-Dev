import j_plus as jp

while True:
    text = input("J+ stdin> ")
    result, error = jp.run("<stdin terminal>", text)

    if error:
        print(f'\033[0;31mERROR: {error.as_string()} \033[0;0m')
    else:
        print(result)
