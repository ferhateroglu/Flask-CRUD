def find_max(t, z):
    max_value = 0
    len_t = len(t)

    for i in range(len_t):
        for j in range(i + 1, len_t + 1):
            substring = t[i:j]
            count = z.count(substring)
            value = len(substring) * count
            if value > max_value:
                max_value = value

    return max_value


if __name__ == '__main__':
    result = find_max("acldm1labcdhsnd", "shabcdacasklksjabcdfueuabcdfhsndsabcdmdabcdfa")
    print(result)