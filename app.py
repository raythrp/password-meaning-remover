import streamlit as st

def autokey_encrypt(text):
    key = text[-1]  # Karakter terakhir sebagai key
    key = key + text[:-1]
    encrypted = ''
    for i in range(len(text)):
        if text[i].isalpha():
            base = ord('A') if text[i].isupper() else ord('a')
            shift = ord(key[i]) - base
            encrypted += chr((ord(text[i]) - base + shift) % 26 + base)
        else:
            encrypted += text[i]
    return encrypted

def autokey_decrypt(text):
    if not text:
        return ""
    key = text[-1]  # Karakter terakhir sebagai key
    decrypted = ''
    key_list = [key] 
    for i in range(len(text)):
        if text[i].isalpha():
            base = ord('A') if text[i].isupper() else ord('a')
            shift = ord(key_list[i]) - base
            decrypted_char = chr((ord(text[i]) - base - shift) % 26 + base)
            decrypted += decrypted_char
            key_list.append(decrypted_char)
        else:
            decrypted += text[i]
            key_list.append(text[i])
    return decrypted

def zigzag_encrypt(text, key):
    if key <= 1:
        return text 
    rail = [''] * key
    row = 0
    direction = 1
    for char in text:
        rail[row] += char
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    return ''.join(rail)

def zigzag_decrypt(text, key):
    if key <= 1:
        return text 
    rail = [''] * key
    pattern = [0] * len(text)
    row, direction = 0, 1
    for i in range(len(text)):
        pattern[i] = row
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    index = 0
    for r in range(key):
        for i in range(len(text)):
            if pattern[i] == r:
                rail[r] += text[index]
                index += 1
    result = ''
    row, direction = 0, 1
    for i in range(len(text)):
        result += rail[row][0]
        rail[row] = rail[row][1:]
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    return result

# Streamlit
st.title("Password Meaning Remover")
st.sidebar.title("Menu")

mode = st.sidebar.radio("Modes", ["Remove Meaning", "Restore Meaning"])

text = st.text_area("Enter your text")
if st.button("Process"):
    if not text:
        st.error("Please enter the text.")
    elif len(text) < 2:
        st.error("Text must have at least two characters.")
    elif len(text) > 15 and mode == "Encrypt (Autokey + Zigzag)":
        st.error("Text must have at most fifteen characters.")
    elif len(text) > 16 and mode == "Decrypt (Zigzag + Autokey)":
        st.error("Text must have at most sixteen characters.")
    else:
        key_char = text[-1]  # Karakter terakhir sebagai key
        key_value = ord(key_char.lower()) - ord('a') + 1 
        
        if mode == "Encrypt (Autokey + Zigzag)":
            autokey_result = autokey_encrypt(text)
            zigzag_result = zigzag_encrypt(autokey_result, key_value)
            st.success(f"Encrypted Text: {zigzag_result}{key_char}")
        elif mode == "Decrypt (Zigzag + Autokey)":
            zigzag_result = zigzag_decrypt(text, key_value)
            autokey_result = autokey_decrypt(zigzag_result)
            st.success(f"Decrypted Text: {autokey_result[:-1]}")
