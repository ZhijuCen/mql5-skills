# Sound alerts

To work with sound, the MQL5 API provides one function: PlaySound.

bool PlaySound(const string soundfile)

The function plays the specified sound file in the format wav.

If the file name is specified without a path (for example, "Ring.wav"), it must be located in the Sounds folder inside the terminal installation directory. If needed, you can organize subfolders inside the Sounds folder. In such cases, the file name in the soundfile parameter should be preceded by a relative path. For example, "Example/Ring.wav" refers to the folders and file Sounds/Example/Ring.wav inside the terminal installation directory.

In addition, you can use sound files located in any other MQL5 subfolder in the terminal's data directory. Such a path must be preceded by a leading slash (forward single '/' or double backslash '\\'), which is the delimiter character you use between adjacent folder levels in the file system. For example, if the sound file Demo.wav is in the terminal_data_directory/MQL5/Files, then in the PlaySound call, we will write the path "/Files/Demo.wav".

Calling the function with a NULL parameter stops the sound from playing. Calling a function with a new file while the old one is still playing will cause the old one to be interrupted and the new one to start playing.

In addition to files located in the file system, a path to the resources — data blocks embedded in the MQL program — can be passed to the function. In particular, a developer can create a sound resource from a file that is available locally at compile time within a sandbox. All resources are located inside the ex5 file, which ensures that the user has them and simplifies the distribution of the program as a single module.

A detailed article about all ways of using resources, including not only sound but also images, arbitrary binary and text data, and dependent programs (indicators), is presented in the corresponding [section](/en/book/advanced/resources) in the seventh part of the book.

The PlaySound function returns true if the file is found, or false otherwise. Note that even if the file is not an audio file and cannot be played, the function will return true.

Sound playback is performed asynchronously, in parallel with the execution of subsequent program instructions. In other words, the function returns control to the calling code immediately after the call, without waiting for the audio effect to complete.

In the strategy tester, the PlaySound function is not executed.

The OutputSound.mq5 script allows you to test the operation of the function.

```
void OnStart()
{
   PRTF(PlaySound("new.txt"));
   PRTF(PlaySound("abracadabra.wav"));
   const uint start = GetTickCount();
   PRTF(PlaySound("request.wav"));
   PRTF(GetTickCount() - start);
}

```

The program is trying to play multiple files. The file "new.txt" exists (created specifically for testing), the file "abracadabra.wav" does not exist, and the "request.wav" file is included in the standard distribution of MetaTrader 5. The time of the last function call is measured using a pair of calls to GetTickCount.

As a result of running the script, we get the following log entries:

```
PlaySound(new.txt)=true / ok
PlaySound(abracadabra.wav)=false / FILE_NOT_EXIST(5019)
PlaySound(request.wav)=true / ok
GetTickCount()-start=0 / ok

```

The file "new.txt" was found and therefore the function returned true, although it did not produce a sound. A call for a second, non-existent file returned false, and the error code in _LastError is 5019 (FILE_NOT_EXIST). Finally, playing the last file (assuming it exists) should succeed in every sense: the function will return true, and the terminal will play the audio. The call processing time is virtually zero (the duration of the sound does not matter).
