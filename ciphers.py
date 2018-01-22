#!/bin/python

import re, fractions

# The full uppercase alphabet
u_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# The full upper and lowercased alphabet
ul_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# ----------------------------------------------------------------------------
# VIGENERE CIPHER
class VigenereCipher:
    """
    Encrypt/decrypt text using a Vigenere cipher
    
    :param str plaintext: The text to encrypt/decrypt
    :param bool full: Flag that switches between full/uppercase only alphabets
    """ 
    def __init__( self, plaintext, full ):
        alpha = ul_alpha if full else u_alpha
        vtable = [ alpha for a in alpha ]

        for i,row in enumerate(vtable):
            back, front = row[-i:], row[:-i]
            vtable[i] = back + front

        vtable.sort()
        
        self.full = full
        self.text = re.sub(r"\W+", "", plaintext, flags=re.UNICODE)
        if not full: self.text = self.text.upper()
        self.table = [ [ c for c in l ] for l in vtable ]

    @classmethod
    def from_file( cls, filename, full = False ):
        """
        Initialize from the contents of a file

        :param str filename: The file to encrypt/decrypt
        :return: A new VigenereCipher object
        """
        with open(filename) as f:
            return cls(f.read(),full)

    @classmethod
    def from_string( cls, plaintext, full = False ):
        """
        Initialize from a string

        :param str plaintext: The string to encrypt/decrypt
        :return: A new VigenereCipher object
        """
        return cls(plaintext,full)

    def encrypt( self, key ):
        """
        Encrypt the held text

        :param str key: The key to encrypt with
        :return: This VigenereCipher object
        """
        key = self.expand(key, len(self.text))
        result = ['' for x in range(len(self.text))]
        for i,c in enumerate(self.text):
            ci = self.table[0].index( self.text[i] )
            ri = 0
            for j,l in enumerate(self.table):
                if l[0] == key[i]:
                    ri = j


            result[i] = self.table[ ri ][ ci ]

        self.text = ''.join(result)

        return self

    def decrypt( self, key ):
        """
        Decrypt the held text

        :param str key: The key to decrypt with
        :return: This VigenereCipher object
        """
        key = self.expand(key,len(self.text))
        result = ['' for x in range(len(self.text))]
        for i,c in enumerate(self.text):
            ri = 0
            for j,l in enumerate(self.table):
                if l[0] == key[i]:
                    result[i] = self.table[ 0 ][ self.table[j].index(c) ]

        self.text = ''.join(result)

        return self

    def expand( self, key, length ):
        """
        Repeat the key to match the text length

        :param str key: The short form of the key
        "param int length: The length to expand to
        """
        vkey = '' 
        key = re.sub(r"\W+", "", key, flags=re.UNICODE)
        if not self.full: key = key.upper()

        for i in range(length):
            i = i % len(key)
            vkey += key[i]

        return vkey

    def save( self, filename ):
        """
        Write the held text to a file

        :param str filename: The path to save the text to
        """
        try:
            with open(filename,'w') as f:
                f.write(self.text)
                return True
        except:
            return False

    def __str__( self ):
        """
        Get the current form of the text

        :return: The held text
        """
        return self.text

# ----------------------------------------------------------------------------
# BLOCK AFFINE CIPHER
class BlockAffineCipher:
    """
    Encrypt/decrypt text using a Block Affine cipher
    
    :param str plaintext: The text to encrypt/decrypt
    :param int modulo: The modulo to encrypt with
    :param bool full: Flag that switches between full/uppercase only alphabets
    """ 

    def __init__( self, plaintext, modulo, full ):
        self.block = 2
        self.modulo = modulo
        self.alpha = ul_alpha if full else u_alpha
        self.text = re.sub(r"\W+","",plaintext,flags=re.UNICODE)
        if not full: self.text = self.text.upper()

        while (len(self.text) % self.block) > 0:
            self.text += 'A'

    @classmethod
    def from_file( cls, filename, mod, full = False ):
        """
        Initialize from the contents of a file

        :param str filename: The file to encrypt/decrypt
        :param int mod: The modulo to use
        :param bool full: Flag to switch between full/upper alphabets
        :return: A new BlockAffineCipher object
        """
        with open(filename) as f:
            return cls( f.read(), mod, full)
            
    @classmethod
    def from_string( cls, plaintext, mod, full = False ):
        """
        Initialize from a string

        :param str plaintext: The string to encrypt/decrypt
        :param int mod: The modulo to use
        :param bool full: Flag to switch between full/upper alphabets
        :return: A new BlockAffineCipher object
        """
        return cls( plaintext, mod, full )


    def encrypt( self, keya, keyb ):
        """
        Encrypt the held text

        :param int keya: A user-provided multiplier
        :param int keyb: A user-provided offset
        :return: This BlockAffineCipher object
        """
        result = ['' for x in self.text]
        for i,ch in enumerate(self.text):
            num = self.alpha.find(ch)
            num = ((keya*num) + keyb) % self.modulo
            result[i] = self.alpha[num]

        self.text = ''.join(result)

        return self

    
    def decrypt( self, keya, keyb ):
        """
        Decrypt the held text

        :param int keya: A user-provided multiplier
        :param int keyb: A user-provided offset
        :return: This BlockAffineCipher object
        """
        result = ['' for x in self.text]

        def get_inverse( a, m ):
            if fractions.gcd(a,m) == 1:
                for i in range(1,m):
                    if (a*i)%m == 1: return i
            raise Exception("Couldn't find a modulo inverse")

        for i,ch in enumerate(self.text):
            num = self.alpha.find(ch)
            mod_inv = get_inverse( keya, self.modulo )
            num = (mod_inv*(num - keyb)) % self.modulo
            result[i] = self.alpha[num]

        self.text = ''.join(result)

        return self

    def save( self, filename ):
        """
        Write the held text to a file

        :param str filename: The path to save the text to
        """
        try:
            with open(filename,'w') as f:
                f.write(self.text)
                return True
        except:
            return False

    def __str__( self ):
        """
        Get the current form of the text

        :return: The held text
        """
        return self.text

if __name__=='__main__':
    # Init/set variables
    full     = False
    mod      = 26
    keya     = 0
    keyb     = 0
    text     = "plaintext.txt"
    vkey     = "vcipherkey.txt"
    vout_enc = "vigenerecipheroutput.txt"
    bout_enc = "blockaffinecipheroutput.txt"
    vout_dec = "secondplaintextoutput.txt"
    bout_dec = "blockaffinecipherplaintextoutput.txt"

    # Get the alphabet option
    while True:
        alpha_opt = raw_input("Which alphabet will you use? (S or L): ")
        if alpha_opt == 'S':
            break
        elif alpha_opt == 'L':
            full = True
            mod  = 52
            break
        else:
            print("Not a valid option")

    # Get the multiplier value
    while True:
        keya_opt = raw_input("Input multiplier for Block Affine cipher: ")
        try:
            keya = int(keya_opt)
            break
        except:
            print("Not a valid number")

    # Get the offset value
    while True:
        keyb_opt = raw_input("Input offset for Block Affine cipher: ")
        try:
            keyb = int(keyb_opt)
            break
        except:
            print("Not a valid number")

    # Get key for Vigenere encryption
    with open(vkey) as f:
        vkey = f.read()

    # Perform Vigenere encryption
    vcipher = VigenereCipher.from_file(text,full).encrypt(vkey)
    vcipher.save(vout_enc)

    # Re-encrypt with Block Affine
    bfcipher = BlockAffineCipher.from_string( str(vcipher), mod, full ).encrypt( keya, keyb )
    bfcipher.save(bout_enc)

    # Decrypt with Block Affine
    bfcipher.decrypt( keya, keyb )
    bfcipher.save(bout_dec)

    # Decrypt with Vigenere
    vcipher = VigenereCipher.from_string( str(bfcipher), full ).decrypt(vkey)
    vcipher.save(vout_dec)

    # Print the results
    print "------ Encryption complete! ------"
    print "Vigenere Cipher (encrypted):     {}".format(vout_enc)
    print "Vigenere Cipher (decrypted):     {}".format(vout_dec)
    print "Block Affine Cipher (encrypted): {}".format(bout_enc)
    print "Block Affine Cipher (decrypted): {}".format(bout_dec)
