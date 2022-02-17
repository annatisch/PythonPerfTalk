import dis


def test_func(a):
    multiplier = 2
    return [
        i*multiplier for i in range(a)
    ]


if __name__ == '__main__':
    dis.dis(test_func)


