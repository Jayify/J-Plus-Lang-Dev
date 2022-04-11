import j_plus as jp

while True:
    text = input("J+ stdin> ")
    result, error = jp.run("<stdin>", text)

    if error:
        print(error.as_string())
    else:
        print(result)
