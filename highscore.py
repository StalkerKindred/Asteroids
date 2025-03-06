import hashlib
import base64
import os

def save_high_score(score, filename="highscore.dat"):
    # Score to string
    data_string = str(score)
    
    # Convert to string
    checksum = hashlib.md5(data_string.encode()).hexdigest()
    
    # Combine data and checksum
    combined = data_string + "|" + checksum
    
    # Encode
    encoded = base64.b64encode(combined.encode()).decode()
    
    # Save to file
    with open(filename, 'w') as file:
        file.write(encoded)

def load_high_score(filename="highscore.dat"):
    try:
        # Read file
        with open(filename, 'r') as file:
            encoded = file.read()
        
        # Decode
        combined = base64.b64decode(encoded).decode()

        # Split data and checksum
        parts = combined.split('|')
        if len(parts) != 2:
            return 0 # Invalid format

        data_string, stored_checksum = parts

        # Calculate new checksum from the data
        new_checksum = hashlib.md5(data_string.encode()).hexdigest()

        # Verify checksums match
        if new_checksum != stored_checksum:
            return 0  # Data has been tampered with

        # Convert string back to int
        try:
            score = int(data_string)
            return score
        except ValueError:
            return 0  # Couldn't convert to integer
      
    except FileNotFoundError:
        return 0  # No high score file exists yet