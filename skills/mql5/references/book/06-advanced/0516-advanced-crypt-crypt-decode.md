# Data decryption and decompression: CryptDecode

To perform data decryption and decompression operations, MQL5 provides the CryptDecode function.

The CryptDecode function performs an inverse transformation of the data array to the receiving result array using the specified method.

int CryptDecode(ENUM_CRYPT_METHOD method, const uchar &data[], const uchar &key[], uchar &result[])

Please note that the obtaining of hash sums performed, in particular, by the CryptEncode function, is a one-way transformation: it is impossible to recover the original data from hashes.

The function returns the number of bytes placed in the destination array or 0 on error. The error code will be added to _LastError. This could be, for example, INVALID_PARAMETER (4003) if we try to decode the hash (method equals one of the CRYPT_HASH constants) or INVALID_ARRAY (4006) if the decryption key is not long enough or is missing.

If the key is incorrect (different from the one used in encryption), we will get gibberish as a result instead of the encoded source data but the error code is zero. This is the normal behavior of the function.

Let's check the work of CryptDecode using the same script CryptDecode.mq5.

In the input parameters, you can specify the text or file to be converted. Text is always implied in encoding Base64 since all encoded data is in binary format and is not supported in input parameters. The conversion method is selected from the Method list.

```
input string Text; // Text (base64, or empty to process File)
input string File = "MQL5Book/clock10.htm.BASE64";
input ENUM_CRYPT_METHOD_EXT Method = _CRYPT_BASE64;

```

Encryption methods require a key which can be specified as a string in the CustomKey field if GenerateKey contains the DUMMY_KEY_CUSTOM option. You can also generate a demo key of the required length from the DUMMY_KEY_LENGTH enumeration (it's the same as in the CryptEncode.mq5 script).

```
input DUMMY_KEY_LENGTH GenerateKey = DUMMY_KEY_CUSTOM; // GenerateKey (length, or from CustomKey)
input string CustomKey = "My top secret key is very strong"; 
input bool DisableCRCinZIP = false;

```

In GenerateKey and CustomKey, you should choose the same values as when launching CryptEncode.mq5.

The algorithm in OnStart starts with a description of the required arrays and obtaining a key from a string or by simple generation (only for a demo, use special software or algorithms to generate a working crypto-resistant key).

```
void OnStart()
{
   ENUM_CRYPT_METHOD method = 0;
   int methods[];
   uchar key[] = {};        // default empty key suitable for zip and base64
   uchar data[], result[];
   uchar zip[], opt[] = {1, 0, 0, 0};
   
   if(GenerateKey == DUMMY_KEY_CUSTOM)
   {
      if(StringLen(CustomKey))
      {
         PRTF(CustomKey);
         StringToCharArray(CustomKey, key, 0, -1, CP_UTF8);
         ArrayResize(key, ArraySize(key) - 1);
      }
   }
   else if(GenerateKey != DUMMY_KEY_0)
   {
      ArrayResize(key, GenerateKey);
      for(int i = 0; i < GenerateKey; ++i) key[i] = (uchar)i;
   }
   
   if(ArraySize(key))
   {   
      Print("Key (bytes):");
      ByteArrayPrint(key);
   }
   else
   {
      Print("Key is not provided");
   }

```

Next, we read the contents of the file or decode Base64 from the Text field (depending on what is filled in) to get the data to process.

```
   method = (ENUM_CRYPT_METHOD)Method;
   Print("- ", EnumToString(method), ", key required: ", KEY_REQUIRED(method));
   if(StringLen(Text))
   {
      if(method != CRYPT_BASE64)
      {
         // since all methods except Base64 produce binary results,
         // they are additionally converted to CryptEncode.mq5 using Base64 to text,
         // so here we want to recover binary data from text input
         // before decryption
         uchar base64[];
         const uchar dummy[] = {};
         PRTF(Text);
         PRTF(StringToCharArray(Text, base64, 0, -1, CP_UTF8));
         ArrayResize(base64, ArraySize(base64) - 1);
         Print("Text (bytes):");
         ByteArrayPrint(base64);
         if(!PRTF(CryptDecode(CRYPT_BASE64, base64, dummy, data)))
         {
            return; // error
         }
         
         Print("Raw data to decipher (after de-base64):");
         ByteArrayPrint(data);
      }
      else
      {
         PRTF(StringToCharArray(Text, data, 0, StringLen(Text), CP_UTF8));
         ArrayResize(data, ArraySize(data) - 1);
      }
   }
   else if(StringLen(File))
   {
      PRTF(File);
      if(PRTF(FileLoad(File, data)) <= 0)
      {
         return; // error
      }
   }

```

If the user tries to recover data from the hash, we will show a warning.

```
   if(IS_HASH(method))
   {
      Print("WARNING: hashes can not be used to restore data! CryptDecode will fail.");
   }

```

Finally, we perform the decryption or decompression (unpacking) directly. In the case of a text, the result is simply logged. In the case of a file, we add the extension ".dec" to the name and write a new file: it can be compared with the original one, which was processed using the CryptEncode.mq5 script.

```
   ResetLastError();
   if(PRTF(CryptDecode(method, data, key, result)))
   {
      if(StringLen(Text))
      {
         Print("Text restored:");
         Print(CharArrayToString(result, 0, WHOLE_ARRAY, CP_UTF8));
      }
      else // File
      {
         const string filename = File + ".dec";
         if(PRTF(FileSave(filename, result)))
         {
            Print("File saved: ", filename);
         }
      }
   }

```

If you run the script with default settings, it will try to decode the file MQL5Book/clock10.htm.BASE64. It is assumed that this was created during the experiments in the previous section, so the process should be successful.

```
- CRYPT_BASE64, key required: false
File=MQL5Book/clock10.htm.BASE64 / ok
FileLoad(File,data)=1320 / ok
CryptDecode(method,data,key,result)=988 / ok
FileSave(filename,result)=true / ok
File saved: MQL5Book/clock10.htm.BASE64.dec

```

The obtained file clock10.htm.BASE64.dec is completely identical to the original clock10.htm. The same should happen if you decrypt files with extensions AES128, AES256, or DES, provided that you specify the same key as the one used when encrypting.

For clarity, let's check the decryption of the text. Previously, encryption of a known phrase using the AES128 method produced a binary which was converted into the following Base64 string for convenience.

```
AQuvVCoSy1szaN8Owy8tQxl9rIrRj9hOqK7KgYYGh9E=

```

Let's enter it in the Text field and select AES128 in the Method dropdown list. We will see the following logs.

```
CustomKey=My top secret key is very strong / ok
Key (bytes):
[00] 4D | 79 | 20 | 74 | 6F | 70 | 20 | 73 | 65 | 63 | 72 | 65 | 74 | 20 | 6B | 65 | 
[16] 79 | 20 | 69 | 73 | 20 | 76 | 65 | 72 | 79 | 20 | 73 | 74 | 72 | 6F | 6E | 67 | 
- CRYPT_AES128, key required: true
Text=AQuvVCoSy1szaN8Owy8tQxl9rIrRj9hOqK7KgYYGh9E= / ok
StringToCharArray(Text,base64,0,-1,CP_UTF8)=44 / ok
Text (bytes):
[00] 41 | 51 | 75 | 76 | 56 | 43 | 6F | 53 | 79 | 31 | 73 | 7A | 61 | 4E | 38 | 4F | 
[16] 77 | 79 | 38 | 74 | 51 | 78 | 6C | 39 | 72 | 49 | 72 | 52 | 6A | 39 | 68 | 4F | 
[32] 71 | 4B | 37 | 4B | 67 | 59 | 59 | 47 | 68 | 39 | 45 | 3D | 
CryptDecode(CRYPT_BASE64,base64,dummy,data)=32 / ok
Raw data to decipher (after de-base64):
[00] 01 | 0B | AF | 54 | 2A | 12 | CB | 5B | 33 | 68 | DF | 0E | C3 | 2F | 2D | 43 | 
[16] 19 | 7D | AC | 8A | D1 | 8F | D8 | 4E | A8 | AE | CA | 81 | 86 | 06 | 87 | D1 | 
CryptDecode(method,data,key,result)=32 / ok
Text restored:
Let's encrypt this message

```

The message was successfully decrypted.

If, with the same input text, you choose to generate an arbitrary key (albeit of sufficient length), you will get gibberish instead of a message.

```
Key (bytes):
[00] 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 0A | 0B | 0C | 0D | 0E | 0F | 
- CRYPT_AES128, key required: true
Text=AQuvVCoSy1szaN8Owy8tQxl9rIrRj9hOqK7KgYYGh9E= / ok
StringToCharArray(Text,base64,0,-1,CP_UTF8)=44 / ok
Text (bytes):
[00] 41 | 51 | 75 | 76 | 56 | 43 | 6F | 53 | 79 | 31 | 73 | 7A | 61 | 4E | 38 | 4F | 
[16] 77 | 79 | 38 | 74 | 51 | 78 | 6C | 39 | 72 | 49 | 72 | 52 | 6A | 39 | 68 | 4F | 
[32] 71 | 4B | 37 | 4B | 67 | 59 | 59 | 47 | 68 | 39 | 45 | 3D | 
CryptDecode(CRYPT_BASE64,base64,dummy,data)=32 / ok
Raw data to decipher (after de-base64):
[00] 01 | 0B | AF | 54 | 2A | 12 | CB | 5B | 33 | 68 | DF | 0E | C3 | 2F | 2D | 43 | 
[16] 19 | 7D | AC | 8A | D1 | 8F | D8 | 4E | A8 | AE | CA | 81 | 86 | 06 | 87 | D1 | 
CryptDecode(method,data,key,result)=32 / ok
Text restored:
??? ?L?? ??J Q+?]?v?9?????n?N?Ű

```

The program will behave similarly if you confuse the encryption method.

It doesn't make sense to choose "unhashing" methods: INVALID_PARAMETER (4003).

```
- CRYPT_HASH_MD5, key required: false
File=MQL5Book/clock10.htm.MD5 / ok
FileLoad(File,data)=16 / ok
WARNING: hashes can not be used to restore data! CryptDecode will fail.
CryptDecode(method,data,key,result)=0 / INVALID_PARAMETER(4003)

```

An attempt to unpack (CRYPT_ARCH_ZIP) something that is not a compressed "deflate" block will result in INTERNAL_ERROR (4001). The same error can be obtained if you enable the skip CRC option for the "archive" without it, or, conversely, uncompress the data without the option, although packing was done with it.
