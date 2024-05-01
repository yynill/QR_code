import re

# Regular expressions for different encoding modes
NUMERIC_RE = re.compile(r'^[0-9]+$')
ALPHANUMERIC_RE = re.compile(r'^[a-zA-Z0-9]+$')
BYTE_RE = re.compile(
    r'(?:[\x00-\x7F]|[\xC2-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF4][\x80-\xBF]{3})+')
KANJI_RE = re.compile(r'^[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]+$')

# Encoding Mode	    Value bits
# ------------------------------
# Numeric	        0001 (1)
# Alphanumeric	    0010 (2)
# Byte	            0100 (4)
# Kanji	            1000 (8)
# ECI	            0111 (7)
ENCODING_MODES = {
    'Numeric': 0b0001,
    'Alphanumeric': 0b0010,
    'Byte': 0b0100,
    'Kanji': 0b1000,
    'ECI': 0b0111
}

# Length bits lookup table
LENGTH_BITS = [
    [10, 12, 14],
    [9, 11, 13],
    [8, 16, 16],
    [8, 10, 12]
]

# Function to determine encoding mode based on input string


def get_encoding_mode(string):
    if NUMERIC_RE.match(string):
        return ENCODING_MODES['Numeric']
    if ALPHANUMERIC_RE.match(string):
        return ENCODING_MODES['Alphanumeric']
    if KANJI_RE.match(string):
        return ENCODING_MODES['Kanji']
    if BYTE_RE.match(string):
        return ENCODING_MODES['Byte']
    return ENCODING_MODES['ECI']

# Function to encode data


def encode_data(encoding_mode, data_to_encode, eci_designator=None):
    encoded_data = []

    # Add mode indicator
    encoded_data.append(encoding_mode)

    # Add character count indicator
    data_length = len(data_to_encode)
    if encoding_mode == ENCODING_MODES['Numeric']:
        encoded_data.append(data_length)
    elif encoding_mode == ENCODING_MODES['Alphanumeric']:
        if data_length % 2 == 0:
            encoded_data.append(data_length // 2)
        else:
            encoded_data.append((data_length // 2) + 1)
    elif encoding_mode == ENCODING_MODES['Byte']:
        encoded_data.append(data_length)
    elif encoding_mode == ENCODING_MODES['ECI']:
        # ECI mode does not require a character count indicator
        pass
    elif encoding_mode == ENCODING_MODES['Kanji']:
        # Kanji encoding mode requires character count indicator in 2 bytes
        encoded_data.extend(divmod(data_length, 256))

    if eci_designator is not None:
        # ECI mode requires a specific designator value
        encoded_data.extend(divmod(eci_designator, 256))

    # Add data
    if encoding_mode == ENCODING_MODES['Byte']:
        for char in data_to_encode.encode('iso-8859-1'):
            encoded_data.append(char)
    elif encoding_mode == ENCODING_MODES['Kanji']:
        for char in data_to_encode:
            # Encode Kanji characters using Shift JIS encoding
            encoded_data.extend(divmod(char.encode('shift_jis')[0], 256))
    else:
        for char in data_to_encode:
            if encoding_mode == ENCODING_MODES['Numeric']:
                # Convert numeric characters to integers
                encoded_data.append(int(char))
            elif encoding_mode == ENCODING_MODES['Alphanumeric']:
                # Convert alphanumeric characters to their corresponding values
                if char.isdigit():
                    encoded_data.append(int(char))
                elif char.isupper():
                    encoded_data.append(ord(char) - ord('A') + 10)
                elif char.islower():
                    encoded_data.append(ord(char) - ord('a') + 36)

    return encoded_data


# Example data to encode

# Numeric Mode Example
data_numeric = "123456"  # Numeric Mode
encoded_numeric = encode_data(ENCODING_MODES['Numeric'], data_numeric)
print("Encoded Numeric Data:", encoded_numeric)

# Alphanumeric Mode Example
data_alphanumeric = "HELLO123"  # Alphanumeric Mode
encoded_alphanumeric = encode_data(
    ENCODING_MODES['Alphanumeric'], data_alphanumeric)
print("Encoded Alphanumeric Data:", encoded_alphanumeric)

# Byte Mode Example (Text Data)
data_byte_text = "Hello, World!"  # Byte Mode (Text Data)
encoded_byte_text = encode_data(ENCODING_MODES['Byte'], data_byte_text)
print("Encoded Byte Mode (Text) Data:", encoded_byte_text)

# Byte Mode Example (Binary Data)
data_byte_binary = '01'  # Byte Mode (Binary Data)
encoded_byte_binary = encode_data(ENCODING_MODES['Byte'], data_byte_binary)
print("Encoded Byte Mode (Binary) Data:", encoded_byte_binary)

# Kanji Mode Example
data_kanji = "漢字"  # Kanji Mode
encoded_kanji = encode_data(ENCODING_MODES['Kanji'], data_kanji)
print("Encoded Kanji Data:", encoded_kanji)

# ECI Mode Example
eci_designator = 3  # Example ECI Designator Value
data_eci = "Some Text"  # ECI Mode
encoded_eci = encode_data(ENCODING_MODES['ECI'], data_eci, eci_designator)
print("Encoded ECI Data with Designator:", encoded_eci)
