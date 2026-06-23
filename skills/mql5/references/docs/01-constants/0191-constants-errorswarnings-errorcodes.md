# Runtime Errors

[GetLastError()](/en/docs/check/getlasterror) is the function that returns the last error code that is stored in the predefined variable [_LastError](/en/docs/predefined/_lasterror). This value can be reset to zero by the [ResetLastError()](/en/docs/common/resetlasterror) function.

| Constant | Code | Description |
| --- | --- | --- |
| ERR_SUCCESS | 0 | The operation completed successfully |
| ERR_INTERNAL_ERROR | 4001 | Unexpected internal error |
| ERR_WRONG_INTERNAL_PARAMETER | 4002 | Wrong parameter in the inner call of the client terminal function |
| ERR_INVALID_PARAMETER | 4003 | Wrong parameter when calling the system function |
| ERR_NOT_ENOUGH_MEMORY | 4004 | Not enough memory to perform the system function |
| ERR_STRUCT_WITHOBJECTS_ORCLASS | 4005 | The structure contains objects of strings and/or dynamic arrays and/or structure of such objects and/or classes |
| ERR_INVALID_ARRAY | 4006 | Array of a wrong type, wrong size, or a damaged object of a dynamic array |
| ERR_ARRAY_RESIZE_ERROR | 4007 | Not enough memory for the relocation of an array, or an attempt to change the size of a static array |
| ERR_STRING_RESIZE_ERROR | 4008 | Not enough memory for the relocation of string |
| ERR_NOTINITIALIZED_STRING | 4009 | Not initialized string |
| ERR_INVALID_DATETIME | 4010 | Invalid date and/or time |
| ERR_ARRAY_BAD_SIZE | 4011 | Total amount of elements in the array cannot exceed 2147483647 |
| ERR_INVALID_POINTER | 4012 | Wrong pointer |
| ERR_INVALID_POINTER_TYPE | 4013 | Wrong type of pointer |
| ERR_FUNCTION_NOT_ALLOWED | 4014 | Function is not allowed for call |
| ERR_RESOURCE_NAME_DUPLICATED | 4015 | The names of the  dynamic  and the  static  resource match |
| ERR_RESOURCE_NOT_FOUND | 4016 | Resource with this name has not been found in EX5 |
| ERR_RESOURCE_UNSUPPORTED_TYPE | 4017 | Unsupported resource type or its size exceeds 16 Mb |
| ERR_RESOURCE_NAME_IS_TOO_LONG | 4018 | The resource name exceeds 63 characters |
| ERR_MATH_OVERFLOW | 4019 | Overflow occurred when calculating math function |
| ERR_SLEEP_ERROR | 4020 | Out of test end date after calling Sleep() |
| ERR_PROGRAM_STOPPED | 4022 | Test forcibly stopped from the outside. For example, optimization interrupted, visual testing window closed or testing agent stopped |
| ERR_INVALID_TYPE | 4023 | Invalid type |
| ERR_INVALID_HANDLE | 4024 | Invalid handle |
| ERR_TOO_MANY_OBJECTS | 4025 | Object pool filled out |
| Charts |  |  |
| ERR_CHART_WRONG_ID | 4101 | Wrong chart ID |
| ERR_CHART_NO_REPLY | 4102 | Chart does not respond |
| ERR_CHART_NOT_FOUND | 4103 | Chart not found |
| ERR_CHART_NO_EXPERT | 4104 | No Expert Advisor in the chart that could handle the event |
| ERR_CHART_CANNOT_OPEN | 4105 | Chart opening error |
| ERR_CHART_CANNOT_CHANGE | 4106 | Failed to change chart symbol and period |
| ERR_CHART_WRONG_PARAMETER | 4107 | Error value of the parameter for the  function of working with charts |
| ERR_CHART_CANNOT_CREATE_TIMER | 4108 | Failed to create timer |
| ERR_CHART_WRONG_PROPERTY | 4109 | Wrong chart property ID |
| ERR_CHART_SCREENSHOT_FAILED | 4110 | Error creating screenshots |
| ERR_CHART_NAVIGATE_FAILED | 4111 | Error navigating through chart |
| ERR_CHART_TEMPLATE_FAILED | 4112 | Error applying template |
| ERR_CHART_WINDOW_NOT_FOUND | 4113 | Subwindow containing the indicator was not found |
| ERR_CHART_INDICATOR_CANNOT_ADD | 4114 | Error adding an indicator to chart |
| ERR_CHART_INDICATOR_CANNOT_DEL | 4115 | Error deleting an indicator from the chart |
| ERR_CHART_INDICATOR_NOT_FOUND | 4116 | Indicator not found on the specified chart |
| Graphical Objects |  |  |
| ERR_OBJECT_ERROR | 4201 | Error working with a graphical object |
| ERR_OBJECT_NOT_FOUND | 4202 | Graphical object was not found |
| ERR_OBJECT_WRONG_PROPERTY | 4203 | Wrong ID of a graphical object property |
| ERR_OBJECT_GETDATE_FAILED | 4204 | Unable to get date corresponding to the value |
| ERR_OBJECT_GETVALUE_FAILED | 4205 | Unable to get value corresponding to the date |
| MarketInfo |  |  |
| ERR_MARKET_UNKNOWN_SYMBOL | 4301 | Unknown symbol |
| ERR_MARKET_NOT_SELECTED | 4302 | Symbol is not selected in MarketWatch |
| ERR_MARKET_WRONG_PROPERTY | 4303 | Wrong identifier of a symbol property |
| ERR_MARKET_LASTTIME_UNKNOWN | 4304 | Time of the last tick is not known (no ticks) |
| ERR_MARKET_SELECT_ERROR | 4305 | Error adding or deleting a symbol in MarketWatch |
| ERR_MARKET_SELECT_LIMIT | 4306 | Exceeded the limit of selected symbols in MarketWatch |
| ERR_MARKET_SESSION_INDEX | 4307 | Wrong session ID when calling the SymbolInfoSessionQuote/SymbolInfoSessionTrade function |
| History Access |  |  |
| ERR_HISTORY_NOT_FOUND | 4401 | Requested history not found |
| ERR_HISTORY_WRONG_PROPERTY | 4402 | Wrong ID of the history property |
| ERR_HISTORY_TIMEOUT | 4403 | Exceeded history request timeout |
| ERR_HISTORY_BARS_LIMIT | 4404 | Number of requested bars limited by terminal settings |
| ERR_HISTORY_LOAD_ERRORS | 4405 | Multiple errors when loading history |
| ERR_HISTORY_SMALL_BUFFER | 4407 | Receiving array is too small to store all requested data |
| Global_Variables |  |  |
| ERR_GLOBALVARIABLE_NOT_FOUND | 4501 | Global variable of the client terminal is not found |
| ERR_GLOBALVARIABLE_EXISTS | 4502 | Global variable of the client terminal with the same name already exists |
| ERR_GLOBALVARIABLE_NOT_MODIFIED | 4503 | Global variables were not modified |
| ERR_GLOBALVARIABLE_CANNOTREAD | 4504 | Cannot read file with global variable values |
| ERR_GLOBALVARIABLE_CANNOTWRITE | 4505 | Cannot write file with global variable values |
| ERR_MAIL_SEND_FAILED | 4510 | Email sending failed |
| ERR_PLAY_SOUND_FAILED | 4511 | Sound playing failed |
| ERR_MQL5_WRONG_PROPERTY | 4512 | Wrong identifier of the program property |
| ERR_TERMINAL_WRONG_PROPERTY | 4513 | Wrong identifier of the terminal property |
| ERR_FTP_SEND_FAILED | 4514 | File sending via ftp failed |
| ERR_NOTIFICATION_SEND_FAILED | 4515 | Failed to send a  notification |
| ERR_NOTIFICATION_WRONG_PARAMETER | 4516 | Invalid parameter for sending a notification – an empty string or  NULL  has been passed to the  SendNotification()  function |
| ERR_NOTIFICATION_WRONG_SETTINGS | 4517 | Wrong settings of notifications in the terminal (ID is not specified or permission is not set) |
| ERR_NOTIFICATION_TOO_FREQUENT | 4518 | Too frequent sending of notifications |
| ERR_FTP_NOSERVER | 4519 | FTP server is not specified |
| ERR_FTP_NOLOGIN | 4520 | FTP login is not specified |
| ERR_FTP_FILE_ERROR | 4521 | File not found in the MQL5\Files directory to send on FTP server |
| ERR_FTP_CONNECT_FAILED | 4522 | FTP connection failed |
| ERR_FTP_CHANGEDIR | 4523 | FTP path not found on server |
| Custom Indicator Buffers |  |  |
| ERR_BUFFERS_NO_MEMORY | 4601 | Not enough memory for the distribution of indicator buffers |
| ERR_BUFFERS_WRONG_INDEX | 4602 | Wrong indicator buffer index |
| Custom Indicator Properties |  |  |
| ERR_CUSTOM_WRONG_PROPERTY | 4603 | Wrong ID of the custom indicator property |
| Account |  |  |
| ERR_ACCOUNT_WRONG_PROPERTY | 4701 | Wrong account property ID |
| ERR_TRADE_WRONG_PROPERTY | 4751 | Wrong trade property ID |
| ERR_TRADE_DISABLED | 4752 | Trading by Expert Advisors prohibited |
| ERR_TRADE_POSITION_NOT_FOUND | 4753 | Position not found |
| ERR_TRADE_ORDER_NOT_FOUND | 4754 | Order not found |
| ERR_TRADE_DEAL_NOT_FOUND | 4755 | Deal not found |
| ERR_TRADE_SEND_FAILED | 4756 | Trade request sending failed |
| ERR_TRADE_CALC_FAILED | 4758 | Failed to calculate profit or margin |
| Indicators |  |  |
| ERR_INDICATOR_UNKNOWN_SYMBOL | 4801 | Unknown symbol |
| ERR_INDICATOR_CANNOT_CREATE | 4802 | Indicator cannot be created |
| ERR_INDICATOR_NO_MEMORY | 4803 | Not enough memory to add the indicator |
| ERR_INDICATOR_CANNOT_APPLY | 4804 | The indicator cannot be applied to another indicator |
| ERR_INDICATOR_CANNOT_ADD | 4805 | Error applying an indicator to chart |
| ERR_INDICATOR_DATA_NOT_FOUND | 4806 | Requested data not found |
| ERR_INDICATOR_WRONG_HANDLE | 4807 | Wrong indicator handle |
| ERR_INDICATOR_WRONG_PARAMETERS | 4808 | Wrong number of parameters when creating an indicator |
| ERR_INDICATOR_PARAMETERS_MISSING | 4809 | No parameters when creating an indicator |
| ERR_INDICATOR_CUSTOM_NAME | 4810 | The first parameter in the array must be the name of the custom indicator |
| ERR_INDICATOR_PARAMETER_TYPE | 4811 | Invalid parameter type in the array when creating an indicator |
| ERR_INDICATOR_WRONG_INDEX | 4812 | Wrong index of the requested indicator buffer |
| Depth of Market |  |  |
| ERR_BOOKS_CANNOT_ADD | 4901 | Depth Of Market can not be added |
| ERR_BOOKS_CANNOT_DELETE | 4902 | Depth Of Market can not be removed |
| ERR_BOOKS_CANNOT_GET | 4903 | The data from Depth Of Market can not be obtained |
| ERR_BOOKS_CANNOT_SUBSCRIBE | 4904 | Error in subscribing to receive new data from Depth Of Market |
| File Operations |  |  |
| ERR_TOO_MANY_FILES | 5001 | More than 64 files cannot be opened at the same time |
| ERR_WRONG_FILENAME | 5002 | Invalid file name |
| ERR_TOO_LONG_FILENAME | 5003 | Too long file name |
| ERR_CANNOT_OPEN_FILE | 5004 | File opening error |
| ERR_FILE_CACHEBUFFER_ERROR | 5005 | Not enough memory for cache to read |
| ERR_CANNOT_DELETE_FILE | 5006 | File deleting error |
| ERR_INVALID_FILEHANDLE | 5007 | A file with this handle was closed, or was not opening at all |
| ERR_WRONG_FILEHANDLE | 5008 | Wrong file handle |
| ERR_FILE_NOTTOWRITE | 5009 | The file must be opened for writing |
| ERR_FILE_NOTTOREAD | 5010 | The file must be opened for reading |
| ERR_FILE_NOTBIN | 5011 | The file must be opened as a binary one |
| ERR_FILE_NOTTXT | 5012 | The file must be opened as a text |
| ERR_FILE_NOTTXTORCSV | 5013 | The file must be opened as a text or CSV |
| ERR_FILE_NOTCSV | 5014 | The file must be opened as CSV |
| ERR_FILE_READERROR | 5015 | File reading error |
| ERR_FILE_BINSTRINGSIZE | 5016 | String size must be specified, because the file is opened as binary |
| ERR_INCOMPATIBLE_FILE | 5017 | A text file must be for string arrays, for other arrays - binary |
| ERR_FILE_IS_DIRECTORY | 5018 | This is not a file, this is a directory |
| ERR_FILE_NOT_EXIST | 5019 | File does not exist |
| ERR_FILE_CANNOT_REWRITE | 5020 | File can not be rewritten |
| ERR_WRONG_DIRECTORYNAME | 5021 | Wrong directory name |
| ERR_DIRECTORY_NOT_EXIST | 5022 | Directory does not exist |
| ERR_FILE_ISNOT_DIRECTORY | 5023 | This is a file, not a directory |
| ERR_CANNOT_DELETE_DIRECTORY | 5024 | The directory cannot be removed |
| ERR_CANNOT_CLEAN_DIRECTORY | 5025 | Failed to clear the directory (probably one or more files are blocked and removal operation failed) |
| ERR_FILE_WRITEERROR | 5026 | Failed to write a resource to a file |
| ERR_FILE_ENDOFFILE | 5027 | Unable to read the next piece of data from a CSV file (FileReadString, FileReadNumber, FileReadDatetime, FileReadBool), since the end of file is reached |
| String Casting |  |  |
| ERR_NO_STRING_DATE | 5030 | No date in the string |
| ERR_WRONG_STRING_DATE | 5031 | Wrong date in the string |
| ERR_WRONG_STRING_TIME | 5032 | Wrong time in the string |
| ERR_STRING_TIME_ERROR | 5033 | Error converting string to date |
| ERR_STRING_OUT_OF_MEMORY | 5034 | Not enough memory for the string |
| ERR_STRING_SMALL_LEN | 5035 | The string length is less than expected |
| ERR_STRING_TOO_BIGNUMBER | 5036 | Too large number, more than ULONG_MAX |
| ERR_WRONG_FORMATSTRING | 5037 | Invalid format string |
| ERR_TOO_MANY_FORMATTERS | 5038 | Amount of format specifiers more than the parameters |
| ERR_TOO_MANY_PARAMETERS | 5039 | Amount of parameters more than the format specifiers |
| ERR_WRONG_STRING_PARAMETER | 5040 | Damaged parameter of string type |
| ERR_STRINGPOS_OUTOFRANGE | 5041 | Position outside the string |
| ERR_STRING_ZEROADDED | 5042 | 0 added to the string end, a useless operation |
| ERR_STRING_UNKNOWNTYPE | 5043 | Unknown data type when converting to a string |
| ERR_WRONG_STRING_OBJECT | 5044 | Damaged string object |
| Operations with Arrays |  |  |
| ERR_INCOMPATIBLE_ARRAYS | 5050 | Copying incompatible arrays. String array can be copied only to a string array, and a numeric array - in numeric array only |
| ERR_SMALL_ASSERIES_ARRAY | 5051 | The receiving array is declared as AS_SERIES, and it is of insufficient size |
| ERR_SMALL_ARRAY | 5052 | Too small array, the starting position is outside the array |
| ERR_ZEROSIZE_ARRAY | 5053 | An array of zero length |
| ERR_NUMBER_ARRAYS_ONLY | 5054 | Must be a numeric array |
| ERR_ONEDIM_ARRAYS_ONLY | 5055 | Must be a one-dimensional array |
| ERR_SERIES_ARRAY | 5056 | Timeseries cannot be used |
| ERR_DOUBLE_ARRAY_ONLY | 5057 | Must be an array of type double |
| ERR_FLOAT_ARRAY_ONLY | 5058 | Must be an array of type float |
| ERR_LONG_ARRAY_ONLY | 5059 | Must be an array of type long |
| ERR_INT_ARRAY_ONLY | 5060 | Must be an array of type int |
| ERR_SHORT_ARRAY_ONLY | 5061 | Must be an array of type short |
| ERR_CHAR_ARRAY_ONLY | 5062 | Must be an array of type char |
| ERR_STRING_ARRAY_ONLY | 5063 | String array only |
| Operations with OpenCL |  |  |
| ERR_OPENCL_NOT_SUPPORTED | 5100 | OpenCL functions  are not supported on this computer |
| ERR_OPENCL_INTERNAL | 5101 | Internal error occurred when  running OpenCL |
| ERR_OPENCL_INVALID_HANDLE | 5102 | Invalid  OpenCL handle |
| ERR_OPENCL_CONTEXT_CREATE | 5103 | Error creating the  OpenCL context |
| ERR_OPENCL_QUEUE_CREATE | 5104 | Failed to create a run queue in OpenCL |
| ERR_OPENCL_PROGRAM_CREATE | 5105 | Error occurred when  compiling an OpenCL program |
| ERR_OPENCL_TOO_LONG_KERNEL_NAME | 5106 | Too long kernel name  (OpenCL kernel) |
| ERR_OPENCL_KERNEL_CREATE | 5107 | Error creating an  OpenCL kernel |
| ERR_OPENCL_SET_KERNEL_PARAMETER | 5108 | Error occurred when  setting parameters  for the OpenCL kernel |
| ERR_OPENCL_EXECUTE | 5109 | OpenCL program  runtime error |
| ERR_OPENCL_WRONG_BUFFER_SIZE | 5110 | Invalid size of the OpenCL buffer |
| ERR_OPENCL_WRONG_BUFFER_OFFSET | 5111 | Invalid offset in the OpenCL buffer |
| ERR_OPENCL_BUFFER_CREATE | 5112 | Failed to create an  OpenCL buffer |
| ERR_OPENCL_TOO_MANY_OBJECTS | 5113 | Too many OpenCL objects |
| ERR_OPENCL_SELECTDEVICE | 5114 | OpenCL device selection error |
| Working with databases |  |  |
| ERR_DATABASE_INTERNAL | 5120 | Internal database error |
| ERR_DATABASE_INVALID_HANDLE | 5121 | Invalid database handle |
| ERR_DATABASE_TOO_MANY_OBJECTS | 5122 | Exceeded the maximum acceptable number of Database objects |
| ERR_DATABASE_CONNECT | 5123 | Database connection error |
| ERR_DATABASE_EXECUTE | 5124 | Request execution error |
| ERR_DATABASE_PREPARE | 5125 | Request generation error |
| ERR_DATABASE_NO_MORE_DATA | 5126 | No more data to read |
| ERR_DATABASE_STEP | 5127 | Failed to move to the next request entry |
| ERR_DATABASE_NOT_READY | 5128 | Data for reading request results are not ready yet |
| ERR_DATABASE_BIND_PARAMETERS | 5129 | Failed to auto substitute parameters to an SQL request |
| Operations with WebRequest |  |  |
| ERR_WEBREQUEST_INVALID_ADDRESS | 5200 | Invalid URL |
| ERR_WEBREQUEST_CONNECT_FAILED | 5201 | Failed to connect to specified URL |
| ERR_WEBREQUEST_TIMEOUT | 5202 | Timeout exceeded |
| ERR_WEBREQUEST_REQUEST_FAILED | 5203 | HTTP request failed |
| Operations with network (sockets) |  |  |
| ERR_NETSOCKET_INVALIDHANDLE | 5270 | Invalid socket handle passed to function |
| ERR_NETSOCKET_TOO_MANY_OPENED | 5271 | Too many open sockets (max 128) |
| ERR_NETSOCKET_CANNOT_CONNECT | 5272 | Failed to connect to remote host |
| ERR_NETSOCKET_IO_ERROR | 5273 | Failed to send/receive data from socket |
| ERR_NETSOCKET_HANDSHAKE_FAILED | 5274 | Failed to establish secure connection (TLS Handshake) |
| ERR_NETSOCKET_NO_CERTIFICATE | 5275 | No data on certificate protecting the connection |
| Custom Symbols |  |  |
| ERR_NOT_CUSTOM_SYMBOL | 5300 | A custom symbol must be specified |
| ERR_CUSTOM_SYMBOL_WRONG_NAME | 5301 | The name of the custom symbol is invalid. The symbol name can only contain Latin letters without punctuation, spaces or special characters (may only contain ".", "_", "&" and "#"). It is not recommended to use characters <, >, :, ", /,\, |, ?, *. |
| ERR_CUSTOM_SYMBOL_NAME_LONG | 5302 | The name of the custom symbol is too long. The length of the symbol name must not exceed 32 characters including the ending 0 character |
| ERR_CUSTOM_SYMBOL_PATH_LONG | 5303 | The path of the custom symbol is too long. The path length should not exceed 128 characters including "Custom\\", the symbol name, group separators and the ending 0 |
| ERR_CUSTOM_SYMBOL_EXIST | 5304 | A custom symbol with the same name already exists |
| ERR_CUSTOM_SYMBOL_ERROR | 5305 | Error occurred while creating, deleting or changing the custom symbol |
| ERR_CUSTOM_SYMBOL_SELECTED | 5306 | You are trying to delete a custom symbol selected in Market Watch |
| ERR_CUSTOM_SYMBOL_PROPERTY_WRONG | 5307 | An invalid custom symbol property |
| ERR_CUSTOM_SYMBOL_PARAMETER_ERROR | 5308 | A wrong parameter while setting the property of a custom symbol |
| ERR_CUSTOM_SYMBOL_PARAMETER_LONG | 5309 | A too long string parameter while setting the property of a custom symbol |
| ERR_CUSTOM_TICKS_WRONG_ORDER | 5310 | Ticks  in the array are  not arranged  in the order of time |
| Economic Calendar |  |  |
| ERR_CALENDAR_MORE_DATA | 5400 | Array size is insufficient for receiving descriptions of all values |
| ERR_CALENDAR_TIMEOUT | 5401 | Request time limit exceeded |
| ERR_CALENDAR_NO_DATA | 5402 | Country is not found |
| Working with databases |  |  |
| ERR_DATABASE_ERROR | 5601 | Generic error |
| ERR_DATABASE_LOGIC | 5602 | SQLite internal logic error |
| ERR_DATABASE_PERM | 5603 | Access denied |
| ERR_DATABASE_ABORT | 5604 | Callback routine requested abort |
| ERR_DATABASE_BUSY | 5605 | Database file locked |
| ERR_DATABASE_LOCKED | 5606 | Database table locked |
| ERR_DATABASE_NOMEM | 5607 | Insufficient memory for completing operation |
| ERR_DATABASE_READONLY | 5608 | Attempt to write to readonly database |
| ERR_DATABASE_INTERRUPT | 5609 | Operation terminated by sqlite3_interrupt() |
| ERR_DATABASE_IOERR | 5610 | Disk I/O error |
| ERR_DATABASE_CORRUPT | 5611 | Database disk image corrupted |
| ERR_DATABASE_NOTFOUND | 5612 | Unknown operation code in sqlite3_file_control() |
| ERR_DATABASE_FULL | 5613 | Insertion failed because database is full |
| ERR_DATABASE_CANTOPEN | 5614 | Unable to open the database file |
| ERR_DATABASE_PROTOCOL | 5615 | Database lock protocol error |
| ERR_DATABASE_EMPTY | 5616 | Internal use only |
| ERR_DATABASE_SCHEMA | 5617 | Database schema changed |
| ERR_DATABASE_TOOBIG | 5618 | String or BLOB exceeds size limit |
| ERR_DATABASE_CONSTRAINT | 5619 | Abort due to constraint violation |
| ERR_DATABASE_MISMATCH | 5620 | Data type mismatch |
| ERR_DATABASE_MISUSE | 5621 | Library used incorrectly |
| ERR_DATABASE_NOLFS | 5622 | Uses OS features not supported on host |
| ERR_DATABASE_AUTH | 5623 | Authorization denied |
| ERR_DATABASE_FORMAT | 5624 | Not used |
| ERR_DATABASE_RANGE | 5625 | Bind parameter error, incorrect index |
| ERR_DATABASE_NOTADB | 5626 | File opened that is not database file |
| Matrix and Vector Methods |  |  |
| ERR_MATRIX_INTERNAL | 5700 | Internal error of the matrix/vector executing subsystem |
| ERR_MATRIX_NOT_INITIALIZED | 5701 | Matrix/vector not  initialized |
| ERR_MATRIX_INCONSISTENT | 5702 | Inconsistent size of matrices/vectors in operation |
| ERR_MATRIX_INVALID_SIZE | 5703 | Invalid matrix/vector size |
| ERR_MATRIX_INVALID_TYPE | 5704 | Invalid matrix/vector type |
| ERR_MATRIX_FUNC_NOT_ALLOWED | 5705 | Function not available for this matrix/vector |
| ERR_MATRIX_CONTAINS_NAN | 5706 | Matrix/vector contains non-numbers (Nan/Inf) |
| ONNX models |  |  |
| ERR_ONNX_INTERNAL | 5800 | ONNX internal error |
| ERR_ONNX_NOT_INITIALIZED | 5801 | ONNX Runtime API initialization error |
| ERR_ONNX_NOT_SUPPORTED | 5802 | Property or value not supported by MQL5 |
| ERR_ONNX_RUN_FAILED | 5803 | ONNX runtime API run error |
| ERR_ONNX_INVALID_PARAMETERS_COUNT | 5804 | Invalid number of parameters passed to OnnxRun |
| ERR_ONNX_INVALID_PARAMETER | 5805 | Invalid parameter value |
| ERR_ONNX_INVALID_PARAMETER_TYPE | 5806 | Invalid parameter type |
| ERR_ONNX_INVALID_PARAMETER_SIZE | 5807 | Invalid parameter size |
| ERR_ONNX_WRONG_DIMENSION | 5808 | Tensor dimension not set or invalid |
| User errors |  |  |
| ERR_USER_ERROR_FIRST | 65536 | User defined  errors start with this code |

See also

[Trade Server Return Codes](/en/docs/constants/errorswarnings/enum_trade_return_codes)
