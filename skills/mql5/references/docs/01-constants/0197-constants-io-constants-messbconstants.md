# Constants of the MessageBox Dialog Window

This section contains return codes of the [MessageBox()](/en/docs/common/messagebox) function. If a message window has a Cancel button, the function returns IDCANCEL, in case if the ESC key or the Cancel button is pressed. If there is no Cancel button in the message window, the pressing of ESC does not give any effect.

| Constant | Value | Description |
| --- | --- | --- |
| IDOK | 1 | "OK" button has been pressed |
| IDCANCEL | 2 | "Cancel" button has been pressed |
| IDABORT | 3 | "Abort" button has been pressed |
| IDRETRY | 4 | "Retry" button has been pressed |
| IDIGNORE | 5 | "Ignore" button has been pressed |
| IDYES | 6 | "Yes" button has been pressed |
| IDNO | 7 | "No" button has been pressed |
| IDTRYAGAIN | 10 | "Try Again" button has been pressed |
| IDCONTINUE | 11 | "Continue" button has been pressed |

The main flags of the [MessageBox()](/en/docs/common/messagebox) function define contents and behavior of the dialog window. This value can be a combination of the following flag groups:

| Constant | Value | Description |
| --- | --- | --- |
| MB_OK | 0x00000000 | Message window contains only one button: OK. Default |
| MB_OKCANCEL | 0x00000001 | Message window contains two buttons: OK and Cancel |
| MB_ABORTRETRYIGNORE | 0x00000002 | Message window contains three buttons: Abort, Retry and Ignore |
| MB_YESNOCANCEL | 0x00000003 | Message window contains three buttons: Yes, No and Cancel |
| MB_YESNO | 0x00000004 | Message window contains two buttons: Yes and No |
| MB_RETRYCANCEL | 0x00000005 | Message window contains two buttons: Retry and Cancel |
| MB_CANCELTRYCONTINUE | 0x00000006 | Message window contains three buttons: Cancel, Try Again, Continue |

To display an icon in the message window it is necessary to specify additional flags:

| Constant | Value | Description |
| --- | --- | --- |
| MB_ICONSTOP,  
 MB_ICONERROR,  
 MB_ICONHAND | 0x00000010 | The STOP sign icon |
| MB_ICONQUESTION | 0x00000020 | The question sign icon |
| MB_ICONEXCLAMATION,  
 MB_ICONWARNING | 0x00000030 | The exclamation/warning sign icon |
| MB_ICONINFORMATION,  
 MB_ICONASTERISK | 0x00000040 | The encircled  i  sign |

Default buttons are defined by the following flags:

| Constant | Value | Description |
| --- | --- | --- |
| MB_DEFBUTTON1 | 0x00000000 | The first button MB_DEFBUTTON1 - is default, if the other buttons MB_DEFBUTTON2, MB_DEFBUTTON3, or MB_DEFBUTTON4 are not specified |
| MB_DEFBUTTON2 | 0x00000100 | The second button is default |
| MB_DEFBUTTON3 | 0x00000200 | The third button is default |
| MB_DEFBUTTON4 | 0x00000300 | The fourth button is default |
