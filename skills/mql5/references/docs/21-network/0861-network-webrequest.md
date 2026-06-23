# WebRequest

The function sends an HTTP request to a specified server. The function has two versions:

1. Sending simple requests of type "key=value" using the header Content-Type: application/x-www-form-urlencoded.

```
int  WebRequest(
   const string      method,           // HTTP method 
   const string      url,              // URL
   const string      cookie,           // cookie
   const string      referer,          // referer
   int               timeout,          // timeout
   const char        &data[],          // the array of the HTTP message body
   int               data_size,        // data[] array size in bytes
   char              &result[],        // an array containing server response data
   string            &result_headers   // headers of server response
   );

```

2. Sending a request of any type specifying the custom set of headers for a more flexible interaction with various Web services.

```
int  WebRequest(
   const string      method,           // HTTP method
   const string      url,              // URL
   const string      headers,          // headers 
   int               timeout,          // timeout
   const char        &data[],          // the array of the HTTP message body
   char              &result[],        // an array containing server response data
   string            &result_headers   // headers of server response
   );

```

Parameters

method

[in]  HTTP method.

url

[in]  URL.

headers

[in]  Request headers of type "key: value", separated by a line break "\r\n".

cookie

[in]  Cookie value.

referer

[in]  Value of the Referer header of the HTTP request.

timeout

[in]  Timeout in milliseconds.

data[]

[in]  Data array of the HTTP message body.

data_size

[in]  Size of the data[] array.

result[]

[out]  An array containing server response data.

result_headers

[out] Server response headers.

Return Value

HTTP server response code or -1 for an error.

Note

To use the WebRequest() function, add the addresses of the required servers in the list of allowed URLs in the "Expert Advisors" tab of the "Options" window. Server port is automatically selected on the basis of the specified protocol - 80 for "http://" and 443 for "https://".

The WebRequest() function is synchronous, which means its breaks the program execution and waits for the response from the requested server. Since the delays in receiving a response can be large, the function is not available for calls from indicators, because indicators run in a common thread shared by all indicators and charts on one symbol. Indicator performance delay on one of the charts of a symbol may stop updating of all charts of the same symbol.

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If you try to call the function from an indicator, [GetLastError()](/en/docs/check/getlasterror) will return error 4014 – "Function is not allowed for call".

WebRequest() cannot be executed in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
void OnStart()
  {
   string cookie=NULL,headers;
   char   post[],result[];
   string url="https://finance.yahoo.com";
//--- To enable access to the server, you should add URL "https://finance.yahoo.com"
//--- to the list of allowed URLs (Main Menu->Tools->Options, tab "Expert Advisors"):
//--- Resetting the last error code
   ResetLastError();
//--- Downloading a html page from Yahoo Finance
   int res=WebRequest("GET",url,cookie,NULL,500,post,0,result,headers);
   if(res==-1)
     {
      Print("Error in WebRequest. Error code  =",GetLastError());
      //--- Perhaps the URL is not listed, display a message about the necessity to add the address
      MessageBox("Add the address '"+url+"' to the list of allowed URLs on tab 'Expert Advisors'","Error",MB_ICONINFORMATION);
     }
   else
     {
      if(res==200)
        {
         //--- Successful download
         PrintFormat("The file has been successfully downloaded, File size %d byte.",ArraySize(result));
         //PrintFormat("Server headers: %s",headers);
         //--- Saving the data to a file
         int filehandle=FileOpen("url.htm",FILE_WRITE|FILE_BIN);
         if(filehandle!=INVALID_HANDLE)
           {
            //--- Saving the contents of the result[] array to a file
            FileWriteArray(filehandle,result,0,ArraySize(result));
            //--- Closing the file
            FileClose(filehandle);
           }
         else
            Print("Error in FileOpen. Error code =",GetLastError());
        }
      else
         PrintFormat("Downloading '%s' failed, error code %d",url,res);
     }
  }

```
