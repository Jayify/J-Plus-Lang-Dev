import j_plus as jp

while True:
    text = input("J+ > ")
    result, error = jp.run(text)

    if error:
        print(error.as_string())
    else:
        print(result)
