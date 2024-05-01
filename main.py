from encode import *

if __name__ == "__main__":

    data = "abcd"

    mode = get_encoding_mode(data)
    encoded_data = encode_data(mode, data)
    binary = encode_data_to_binary(encoded_data)

    print("")
    print("Data:", data)
    print("Encoding Mode:", mode, "-",  list(ENCODING_MODES.keys())
          [list(ENCODING_MODES.values()).index(mode)])
    print("Encoded Data:", encoded_data)
    print("Encoded Binary:", binary)

    print(get_qr_code_format(encoded_data))

# leading numbers are off
