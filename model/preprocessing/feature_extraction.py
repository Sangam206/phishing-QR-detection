import math

def calculate_randomness(text):
    # This measures how random a word looks. 
    # Normal words have a low score. Random letter mashing has a high score.
    if text == "":
        return 0
        
    length = len(text)
    letter_counts = {}
    
    # Count how many times each letter appears
    for letter in text:
        if letter in letter_counts:
            letter_counts[letter] = letter_counts[letter] + 1
        else:
            letter_counts[letter] = 1
            
    # Calculate the randomness score (called Entropy)
    total_score = 0
    for letter in letter_counts:
        count = letter_counts[letter]
        probability = count / length
        total_score = total_score + (probability * math.log2(probability))
        
    return -total_score

def extract_features(url):
    # This function turns a URL into a list of 17 numbers that a computer can understand.
    
    # 1. Clean up whitespace
    url = url.strip()
    
    # 2. Separate the main website name from the folders/files
    # For example, in "http://google.com/images", website = "google.com", folders = "/images"
    parts = url.split("/")
    
    if len(parts) > 2:
        website_name = parts[2]
    else:
        website_name = url
        
    # Put all the folders back together
    if len(parts) > 3:
        folders = "/"
        for part in parts[3:]:
            folders = folders + part + "/"
    else:
        folders = ""

    # Feature 1: How long is the entire URL?
    length = len(url)

    # Feature 2: How many dots (.) are there? Phishing links often have too many dots.
    dots = url.count(".")

    # Feature 3: How many hyphens (-) are in the main website name?
    hyphens = website_name.count("-")

    # Feature 4: How many subdomains? (dots in the name minus 1)
    subdomains = website_name.count(".")
    if subdomains > 0:
        subdomains = subdomains - 1

    # Feature 5: How many weird symbols are there?
    weird_symbols = 0
    for letter in url:
        if letter in "?=&#%-_~":
            weird_symbols = weird_symbols + 1
    
    # Feature 6: What percentage of the URL is weird symbols?
    if length > 0:
        symbol_percent = weird_symbols / length
    else:
        symbol_percent = 0

    # Feature 7: How long are the folders at the end?
    folder_length = len(folders)

    # Feature 8: Does it use tricky words?
    tricky_words = ["login", "verify", "update", "secure", "bank", "account", 
                    "password", "confirm", "signin", "free", "prize", "error"]
    
    has_tricky_word = 0
    url_lower = url.lower()
    for word in tricky_words:
        if word in url_lower:
            has_tricky_word = 1
            break

    # Feature 9: How random does the whole URL look?
    randomness_score = calculate_randomness(url)

    # Feature 10: What percentage of the URL is numbers?
    number_count = 0
    for letter in url:
        if letter in "0123456789":
            number_count = number_count + 1
            
    if length > 0:
        number_percent = number_count / length
    else:
        number_percent = 0

    # Feature 11: How long is the ending part (like .com or .org)?
    name_pieces = website_name.split(".")
    ending = name_pieces[-1]
    ending_length = len(ending)

    # Feature 12: How many folders deep does it go?
    folder_count = folders.count("/")

    # Feature 13: Does it link directly to a dangerous file type?
    dangerous_files = [".exe", ".zip", ".rar", ".sh", ".php", ".js"]
    has_dangerous_file = 0
    folders_lower = folders.lower()
    for file_type in dangerous_files:
        if file_type in folders_lower:
            has_dangerous_file = 1
            break

    # Feature 14: Is it a hidden short link (like bit.ly)?
    short_links = ["bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "is.gd"]
    is_short_link = 0
    website_lower = website_name.lower()
    for short in short_links:
        if short in website_lower:
            is_short_link = 1
            break

    # Feature 15: How long is the very first piece of the website name?
    first_piece_length = 0
    if len(name_pieces) > 2:
        first_piece_length = len(name_pieces[0])

    # Feature 16: Is it trying to imitate a famous brand? 
    # Example: yahoo.bad-site.com
    famous_brands = ["yahoo", "microsoft", "google", "paypal", "apple", "amazon"]
    is_faking_brand = 0
    
    if len(name_pieces) > 2:
        # The real website name is the last two pieces
        real_name = name_pieces[-2] + "." + name_pieces[-1]
        
        # The fake prefix is everything before the last two pieces
        fake_prefix = ""
        for piece in name_pieces[:-2]:
            fake_prefix = fake_prefix + piece + "."
            
        real_name = real_name.lower()
        fake_prefix = fake_prefix.lower()
        
        for brand in famous_brands:
            # If the brand name is in the prefix, but NOT the real name, it's a fake!
            if brand in fake_prefix:
                if brand not in real_name:
                    is_faking_brand = 1
                    break
    
    # Feature 17: How random do the folders look?
    folder_randomness = calculate_randomness(folders)

    # Finally, group all 17 numbers into a list and return it
    sixteen_numbers = [
        length, dots, hyphens, subdomains, 
        weird_symbols, symbol_percent, folder_length, has_tricky_word, 
        randomness_score, number_percent, ending_length, folder_count, 
        has_dangerous_file, is_short_link, first_piece_length, 
        is_faking_brand, folder_randomness
    ]
    return sixteen_numbers
