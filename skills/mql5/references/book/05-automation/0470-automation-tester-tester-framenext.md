# Getting data frames in terminal

Frames sent from testing agents by the [FrameAdd](/en/book/automation/tester/tester_frameadd) function are delivered into the terminal and written in the order of receipt to an mqd file having the name of the Expert Advisor into the folder terminal_directory/MQL5/Files/Tester. The arrival of one or more frames at once generates the [OnTesterPass](/en/book/automation/tester/tester_ontester_init_pass_deinit) event.

The MQL5 API provides 4 functions for analyzing and reading frames: FrameFirst, FrameFilter, FrameNext, and FrameInputs. All functions return a boolean value with an indication of success (true) or error (false).

To access existing frames, the kernel maintains the metaphor of an internal pointer to the current frame. The pointer automatically moves forward when the next frame is read by the FrameNext function, but it can be returned to the beginning of all frames with FrameFirst or FrameFilter. Thus, an MQL program can organize the iteration of frames in a loop until it has looked through all the frames. This process can be repeated if necessary, for example, by applying different filters in OnTesterDeinit.

bool FrameFirst()

The FrameFirst function sets the internal frame reading pointer to the beginning and resets the filter (if it was previously set using the FrameFilter function).

In theory, for a single reception and processing of all frames, it is not necessary to call FrameFirst, since the pointer is already at the beginning when the optimization starts.

bool FrameFilter(const string name, ulong id)

It sets the frame reading filter and sets the internal frame pointer to the beginning. The filter will affect which frames are included in subsequent calls of FrameNext.

If an empty string is passed as the first parameter, the filter will work only by a numeric parameter, that is, all frames with the specified id. If the value of the second parameter is equal to ULONG_MAX, then only the text filter works.

Calling FrameFilter("", ULONG_MAX) is equivalent to calling FrameFirst(), which is equivalent to the absence of a filter.

If you call FrameFirst or FrameFilter in OnTesterPass, make sure this is really what you need: the code probably contains a logical error as it is possible to loop, read the same frame, or increase the computational load exponentially.

bool FrameNext(ulong &pass, string &name, ulong &id, double &value)

bool FrameNext(ulong &pass, string &name, ulong &id, double &value, void &data[])

The FrameNext function reads one frame and moves the pointer to the next one. The pass parameter will have the optimization pass number recorded in it. The name, id, and value parameters will receive the values passed in the corresponding parameters of the FrameAdd function.

It is important to note that the function can return false while operating normally when there are no more frames to read. In this case, the built-in variable _LastError contains the value 4000 (it has no built-in notation).

No matter which form of the FrameAdd function was used to send data, the contents of the file or array will be placed in the receiving data array. The type of the receiving array must match the type of the sent array, and there are certain nuances in the case of sending a file.

A binary file (FILE_BIN) should preferably be accepted in a byte array uchar to ensure compatibility with any size (because other larger types may not be a multiple of the file size). If the file size (in fact, the size of the data block in the received frame) is not a multiple of the size of the receiving array type, the FrameNext function will not read the data and will return an INVALID_ARRAY (4006) error.

A Unicode text file (FILE_TXT or FILE_CSV without FILE_ANSI modifier) should be accepted into an array of ushort type and then converted to a string by calling ShortArrayToString. An ANSI text file should be received in a uchar array and converted using CharArrayToString.

bool FrameInputs(ulong pass, string &parameters[], uint &count)

The FrameInputs function allows you to get descriptions and values of Expert Advisor input parameters on which the pass with the specified pass number is formed. The parameters string array will be filled with lines like "ParameterNameN=ValueParameterN". The count parameter will be filled with the number of elements in the parameters array.

The calls of these four functions are only allowed inside the [OnTesterPass](/en/book/automation/tester/tester_ontester_init_pass_deinit)[ and ](/en/book/automation/tester/tester_ontester_init_pass_deinit)[OnTesterDeinit](/en/book/automation/tester/tester_ontester_init_pass_deinit) handlers.

Frames can arrive to the terminal in batches, in which case it takes time to deliver them. So, it is not necessary that all of them have time to generate the OnTesterPass event and will be processed until the end of the optimization. In this regard, in order to guarantee the receipt of all late frames, it is necessary to place a block of code with their processing (using the FrameNext function) in OnTesterDeinit.

Consider a simple example FrameTransfer.mq5.

The Expert Advisor has four test parameters. All of them, except for the last string, can be included in the optimization.

```
input bool Parameter0;
input long Parameter1;
input double Parameter2;
input string Parameter3;

```

However, to simplify the example, the number of steps for parameters Parameter1 and Parameter2 is limited to 10 (for each). Thus, if you do not use Parameter0, the maximum number of passes is 121. Parameter3 is an example of a parameter that cannot be included in the optimization.

The Expert Advisor does not trade but generates random data that mimics arbitrary application data. Do not use randomization like this in your work projects: it is only suitable for demonstration.

```
ulong startup; // track the time of one run (just like demo data)
   
int OnInit()
{
   startup = GetMicrosecondCount();
   MathSrand((int)startup);
   return INIT_SUCCEEDED;
}

```

Data is sent in two types of frames: from a file and from an array. Each type has its own identifier.

```
#define MY_FILE_ID 100
#define MY_TIME_ID 101
   
double OnTester()
{
 // send file in one frame
   const static string filename = "binfile";
   int h = FileOpen(filename, FILE_WRITE | FILE_BIN | FILE_ANSI);
   FileWriteString(h, StringFormat("Random: %d", MathRand()));
   FileClose(h);
   FrameAdd(filename, MY_FILE_ID, MathRand(), filename);
   
 // send array in another frame
   ulong dummy[1];
   dummy[0] = GetMicrosecondCount() - startup;
   FrameAdd("timing", MY_TIME_ID, 0, dummy);
   
   return (Parameter2 + 1) * (Parameter1 + 2);
}

```

The file is written as binary, with simple strings. The result (criterion) of OnTester is a simple arithmetic expression involving Parameter1 and Parameter2.

On the receiving side, in the Expert Advisor instance running in the service mode on the terminal chart, we collect data from all frames with files and put them into a common CSV file. The file is opened in the handler OnTesterInit.

```
int handle; // file for collecting applied results
void OnTesterInit()
{
   handle = FileOpen("output.csv", FILE_WRITE | FILE_CSV | FILE_ANSI, ",");
}

```

As mentioned earlier, all frames may not have time to get into the handler OnTesterPass, and they need to be additionally checked in OnTesterDeinit. Therefore, we have implemented one helper function ProcessFileFrames, which we will call from OnTesterPass, and from OnTesterDeinit.

Inside ProcessFileFrames we keep our internal counter of processed frames, framecount. Using it as an example, we will make sure that the order of arrival of frames and the numbering of test passes often do not match.

```
void ProcessFileFrames()
{
   static ulong framecount = 0;
   ...

```

To receive frames in the function, the variables necessary according to the prototype FrameNext are described. The receiving data array is described here as uchar. If we were to write some structures to our binary file, we could take them directly into an array of structures of the same type.

```
   ulong   pass;
   string  name;
   long    id;
   double  value;
   uchar   data[];
   ...

```

The following describes the variables for obtaining the Expert Advisor inputs for the current pass to which the frame belongs.

```
   string  params[];
   uint    count;
   ...

```

We then read frames in a loop with FrameNext. Recall that several frames can enter the handler at once, so a loop is needed. For each frame, we output to the terminal log the pass number, the name of the frame, and the resulting double value. We skip frames with an ID other than MY_FILE_ID and will process them later.

```
   ResetLastError();
   
   while(FrameNext(pass, name, id, value, data))
   {
      PrintFormat("Pass: %lld Frame: %s Value:%f", pass, name, value);
      if(id != MY_FILE_ID) continue;
      ...
   }
   
   if(_LastError != 4000 && _LastError != 0)
   {
      Print("Error: ", E2S(_LastError));
   }
}

```

For frames with MY_FILE_ID, we do the following: query the input variables, find out which ones are included in the optimization, and save their values to a common CSV file along with the information from the frame. When the frame count is 0, we form the header of the CSV file in the header variable. In all frames, the current (new) record for the CSV file is formed in the record variable.

```
void ProcessFileFrames()
{
   ...
      if(FrameInputs(pass, params, count))
      {
         string header, record;
         if(framecount == 0) // prepare CSV header
         {
            header = "Counter,Pass ID,";
         }
         record = (string)framecount + "," + (string)pass + ",";
         // collect optimized parameters and their values
         for(uint i = 0; i < count; i++)
         {
            string name2value[];
            int n = StringSplit(params[i], '=', name2value);
            if(n == 2)
            {
               long pvalue, pstart, pstep, pstop;
               bool enabled = false;
               if(ParameterGetRange(name2value[0],
                  enabled, pvalue, pstart, pstep, pstop))
               {
                  if(enabled)
                  {
                     if(framecount == 0) // prepare CSV header
                     {
                        header += name2value[0] + ",";
                     }
                     record += name2value[1] + ","; // data field
                  }
               }
            }
         }
         if(framecount == 0) // prepare CSV header
         {
            FileWriteString(handle, header + "Value,File Content\n");
         }
         // write data to CSV
         FileWriteString(handle, record + DoubleToString(value) + ","
            + CharArrayToString(data) + "\n");
      }
      framecount++;
   ...
}

```

Calling ParameterGetRange could also be done more efficiently, only with a zero value of framecount. You can try to do so.

In the OnTesterPass handler, we just call ProcessFileFrames.

```
void OnTesterPass()
{
   ProcessFileFrames(); // standard processing of frames on the go
}

```

Additionally, we call the same function from OnTesterDeinit and close the CSV file.

```
void OnTesterDeinit()
{
   ProcessFileFrames(); // pick up late frames
   FileClose(handle);   // close the CSV file
   ..
}

```

In OnTesterDeinit, we process frames with MY_TIME_ID. The durations of test passes is delivered in these frames, and the average duration of one pass is calculated here. In theory, it makes sense to do this only for analysis in your program, since for the user the duration of the passes is already displayed by the tester in the log.

```
void OnTesterDeinit()
{
   ...
   ulong   pass;
   string  name;
   long    id;
   double  value;
   ulong   data[]; // same array type as sent
   
   FrameFilter("timing", MY_TIME_ID); // rewind to the first frame
   
   ulong count = 0;
   ulong total = 0;
   // cycle through 'timing' frames only
   while(FrameNext(pass, name, id, value, data))
   {
      if(ArraySize(data) == 1)
      {
         total += data[0];
      }
      else
      {
         total += (ulong)value;
      }
      ++count;
   }
   if(count > 0)
   {
      PrintFormat("Average timing: %lld", total / count);
   }
}

```

The Expert Advisor is ready. Let's enable the complete optimization for it (because the total number of options is artificially limited and is too small for the genetic algorithm). We can choose open prices only since the Expert Advisor does not trade. Because of this, you should choose a custom criterion (all other criteria will give 0). For example, let's set the range Parameter1 from 1 to 10 in single steps, and Parameter2 is set from -0.5 to +0.5 in steps of 0.1.

Let's run the optimization. In the expert log in the terminal, we will see entries about received frames of the form:

```
Pass: 0 Frame: binfile Value:5105.000000
Pass: 0 Frame: timing Value:0.000000
Pass: 1 Frame: binfile Value:28170.000000
Pass: 1 Frame: timing Value:0.000000
Pass: 2 Frame: binfile Value:17422.000000
Pass: 2 Frame: timing Value:0.000000
...
Average timing: 1811

```

The corresponding lines with pass numbers, parameter values and frame contents will appear in the output.csv file:

```
Counter,Pass ID,Parameter1,Parameter2,Value,File Content
0,0,0,-0.5,5105.00000000,Random: 87
1,1,1,-0.5,28170.00000000,Random: 64
2,2,2,-0.5,17422.00000000,Random: 61
...
37,35,2,-0.2,6151.00000000,Random: 68
38,62,7,0.0,17422.00000000,Random: 61
39,36,3,-0.2,16899.00000000,Random: 71
40,63,8,0.0,17422.00000000,Random: 61
...
117,116,6,0.5,27648.00000000,Random: 74
118,117,7,0.5,16899.00000000,Random: 71
119,118,8,0.5,17422.00000000,Random: 61
120,119,9,0.5,28170.00000000,Random: 64

```

Obviously, our internal numbering (column Count) goes in order, and the pass numbers Pass ID can be mixed (this depends on many factors of parallel processing of job batches by agents). In particular, the batch of tasks can be the first to finish the agent to which the tasks with higher sequence numbers were assigned: in this case, the numbering in the file will start from the higher passes.

In the tester's log, you can check service statistics by frames.

```
242 frames (42.78 Kb total, 181 bytes per frame) received
local 121 tasks (100%), remote 0 tasks (0%), cloud 0 tasks (0%)
121 new records saved to cache file 'tester\cache\FrameTransfer.EURUSD.H1. »
  » 20220101.20220201.20.9E2DE099D4744A064644F6BB39711DE8.opt'

```

It is important to note that during genetic optimization, run numbers are presented in the optimization report as a pair (generation number, copy number), while the pass number obtained in the FrameNext function is ulong. In fact, it is the pass number in batch jobs in the context of the current optimization run. MQL5 does not provide a means to match pass numbering with a genetic report. For this purpose, the checksums of the input parameters of each pass should be calculated. Opt files with an optimization cache already contain such a field with an MD5 hash.
