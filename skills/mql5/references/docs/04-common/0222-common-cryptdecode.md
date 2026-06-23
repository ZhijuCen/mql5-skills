# CryptDecode

Performs the inverse transformation of the data from array, tranformed by [CryptEncode()](/en/docs/common/cryptencode).

```
int  CryptEncode(
   ENUM_CRYPT_METHOD   method,        // method
   const uchar&        data[],        // source array
   const uchar&        key[],         // key
   uchar&              result[]       // destination array
   );

```

Parameters

method

[in]  Data transformation method. Can be one of the values of [ENUM_CRYPT_METHOD](/en/docs/constants/namedconstants/otherconstants#enum_crypt_method) enumeration.

data[]

[in]  Source array.

key[]

[in]  Key array.

result[]

[out]  Destination array.

Return Value

Amount of bytes in the destination array or 0 in case of error. To obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes) call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
input string InpKey = "ABCDEFG";  // Encryption key
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string text="The quick brown fox jumps over the lazy dog";
   uchar src[],dst[],key[];
 
//--- prepare the encryption key
   StringToCharArray(InpKey,key);
//--- prepare the src[] source array
   StringToCharArray(text,src);
//--- display source data
   PrintFormat("Initial data: size=%d, string='%s'",ArraySize(src),CharArrayToString(src));
 
//--- encrypt the src[] array using the DES method with the key[] 56-bit key
   int res=CryptEncode(CRYPT_DES,src,key,dst);
 
//--- check the encryption result
   if(res>0)
     {
      //--- display encrypted data
      PrintFormat("Encoded data: size=%d %s",res,ArrayToHex(dst));
      //--- decrypt the dst[] array data using the DES method with the key[] 56-bit key
      res=CryptDecode(CRYPT_DES,dst,key,src);
      //--- check the result
      if(res>0)
        {
         //--- display decrypted data
         PrintFormat("Decoded data: size=%d, string='%s'",ArraySize(src),CharArrayToString(src));
        }
      else
         Print("CryptDecode failed. Error: ",GetLastError());
     }
   else
      Print("CryptEncode failed. Error: ",GetLastError());
  }
//+------------------------------------------------------------------+
//| ArrayToHex                                                       |
//+------------------------------------------------------------------+
string ArrayToHex(uchar &arr[],int count=-1)
  {
   string res="";
 
//--- check the size
   if(count<0 || count>ArraySize(arr))
      count=ArraySize(arr);
 
//--- convert to hexadecimal string
   for(int i=0; i<count; i++)
      res+=StringFormat("%.2X",arr[i]);
 
   return(res);
  }

```

See also

[Array Functions](/en/docs/array),[ ](/en/docs/common/cryptdecode)[CryptEncode()](/en/docs/common/cryptencode)
