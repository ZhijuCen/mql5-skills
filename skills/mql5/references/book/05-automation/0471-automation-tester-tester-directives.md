# Preprocessor directives for the tester

In the section on [General properties of programs](/en/book/basis/preprocessor/preprocessor_properties), we first become acquainted with #property directives in MQL programs. Then we met directives intended for [scripts](/en/book/applications/script_service/scripts), [services](/en/book/applications/script_service/services), and [indicators](/en/book/applications/indicators_make/indicators_buffers_plots). There is also a group of directives for the tester. We have already mentioned some of them. For example, [tester_everytick_calculate](/en/book/applications/indicators_make/indicators_test) affects the calculation of indicators.

The following table lists all tester directives with explanations.

| Directive | Description |
| --- | --- |
| tester_indicator "string" | The name of the custom indicator in the format "indicator_name.ex5" |
| tester_file "string" | File name in the format "file_name.extension" with the initial data required for the program test |
| tester_library "string" | Library  name with an extension such as "library.ex5" or "library.dll" |
| tester_set "string" | File name in the format "file_name.set" with settings for values and ranges of optimization of program input parameters |
| tester_no_cache | Disabling reading the existing cache of previous optimizations (opt files) |
| tester_everytick_calculate | Disabling the resource-saving mode for calculating indicators in the tester |

The last two directives have no arguments. All others expect a double-quoted string with the name of a file of one type or another. It also follows from this that directives can be repeated with different files, i.e., you can include several settings files or several indicators.

The tester_indicator directive is required to connect to the testing process those indicators that are not mentioned in the source code of the program under test in the form of constant strings (literals). As a rule, the required indicator can be determined automatically by the compiler from iCustom calls if its name is explicitly specified in the corresponding parameter, for example, iCustom(symbol, period, "indicator_name",...). However, this is not always the case.

Let's say we are writing a universal Expert Advisor that can use different moving average indicators, not just the standard built-in ones. Then we can create an input variable to specify the name of the indicator by the user. Then, the iCustom call will turn into iCustom(symbol, period, CustomIndicatorName,...), where CustomIndicatorName is an input variable of the Expert Advisor, the content of which is not known at the time of compilation. Moreover, the developer in this case is likely to apply IndicatorCreate instead of iCustom, since the number and types of indicator parameters must also be configured. In such cases, to debug the program or demonstrate it with a specific indicator, we should provide the name to the tester using the tester_indicator directive.

The need to report indicator names in the source code significantly limits the ability to test such universal programs that can connect various indicators online.

Without the tester_indicator directive, the terminal will not be able to send an indicator to the agent that is not explicitly declared in the source code, as a result of which the dependent program will lose part or all of its functionality.

The tester_file directive allows you to specify a file that will be transferred to the agents and placed in the sandbox before testing. The content and type of the file is not regulated. For example, these can be the weights of a pre-trained neural network, pre-collected Depth of Market data (because such data cannot be reproduced by the tester), and so on.

Note, that the file from the tester_file directive is only read if it existed at compile time. If the source code was compiled when there was no corresponding file, then its appearance in the future will no longer help: the compiled program will be sent to the agent without an auxiliary file. Therefore, for example, if the file specified in tester_file is generated in OnTesterInit, you should make sure that the file with the given name already existed at the time of compilation, even if it was empty. We will demonstrate this below.

Please note that the compiler does not generate warnings if the file specified in the tester_file directive does not exist.

The connected files must be in the terminal's sandbox" MQL5/Files/.

The tester_library directive informs the tester about the need to transfer the library, which is an auxiliary program that can only work in the context of another MQL program, to the agents. We will talk about libraries in detail in a separate [section](/en/book/advanced/libraries).

The libraries required for testing are determined automatically by the #import directives in the source code. However, if any library is used by an external indicator, then this property must be enabled. The library can be both with the dll extension, as well as with the ex5 extension.

The tester_set directive operates with set files with MQL program settings. The file specified in the directive will become available from the context menu of the tester and will allow the user to quickly apply the settings.

If the name is specified without a path, the set file must be in the same directory as the Expert Advisor. This is somewhat unexpected, because the default directory for set files is Presets, and this is where they are saved by commands from the terminal interface. To connect the set file from the given directory, you must explicitly specify it in the directive and precede it with a slash, which indicates the absolute path inside the MQL5 folder.

```
#property tester_set "/Presets/xyz.set"

```

When there is no leading slash, the path is relative to where the source text was placed.

Immediately after adding the file and recompiling the program, you need to reselect the Expert Advisor in the tester; otherwise, the file will not be picked up!

If you specify the Expert Advisor name and version number as "<expert_name> _<number> .set"  in the name of the set file, then it will automatically be added to the parameter version download menu under the version number <number>. For example, the name "MACD Sample_4.set" means that it is a set file for the Expert Advisor "MACD Sample.mq5" with version number 4.

Those interested can study the format of set files: to do this, manually save the testing/optimization settings in the strategy tester and then open the file created in this way in a text editor.

Now let's look at the directive tester_no_cache. When performing optimization, the strategy tester saves all the results of the performed passes to the optimization cache (files with the extension opt), in which the test result is stored for each set of input parameters. This allows, when re-optimizing on the same parameters, to take ready-made results without re-calculation and time wasting.

However, for some tasks, such as mathematical calculations, it may be necessary to perform calculations regardless of the presence of ready-made results in the optimization cache. In this case, in the source code, you must include the property tester_no_cache. At the same time, the test results themselves will still be stored in the cache so that you can see all the data on the completed passes in the strategy tester.

The directive tester_everytick_calculate is designed to enable the indicator calculation mode on each tick in the tester.

By default, indicators are calculated in the tester only when they are accessed for data, i.e., when the values of indicator buffers are requested. This gives a significant speed-up in testing and optimization if you do not need to get the indicator values at each tick.

However, some programs may require indicators to be recalculated on every tick. It is in such cases that the property tester_everytick_calculate is useful.

Indicators in the strategy tester are also forced to be calculated on each tick in the following cases:

- when testing in visual mode
- if there are the EventChartCustom, OnChartEvent, or OnTimer functions in the indicator

This property applies only to operations in the strategy tester. In the terminal, indicators are always calculated on each incoming tick.

The directive has actually been used in the [FrameTransfer.mq5](/en/book/automation/tester/tester_framenext) Expert Advisor:

```
#property tester_set "FrameTransfer.set"

```

We just didn't focus on it. The file "FrameTransfer.set" is located next to the source code. In the same Expert Advisor, we also needed another directive from the above table:

```
#property tester_no_cache

```

In addition, let's consider an example of a directive tester_file. Earlier in the section on [auto-tuning of Expert Advisor parameters](/en/book/automation/tester/tester_parameterrange) when optimizing, we introduced BandOsMApro.mq5, in which it was necessary to introduce several shadow parameters to pass optimization ranges to our source code running on agents.

The tester_file directive will allow us to get rid of these extra parameters. Let's name the new version BandOsMAprofile.mq5.

Since we are now familiar with the directive tester_set, let's add to the new version the previously mentioned file /Presets/MQL5Book/BandOsMA.set.

```
#property tester_set "/Presets/MQL5Book/BandOsMA.set"

```

Information about the range and step of changing periods of FastOsMA and SlowOsMA will be saved to file BandOsMAprofile.csv" instead of three additional input parameters FastShadow4Optimization, SlowShadow4Optimization, StepsShadow4Optimization.

```
#define SETTINGS_FILE "BandOsMAprofile.csv"
#property tester_file SETTINGS_FILE
   
const string SettingsFile = SETTINGS_FILE;

```

Shadow setting FastSlowCombo4Optimization is still needed for a complete enumeration of allowed combinations of periods.

```
input group "A U X I L I A R Y"
sinput int FastSlowCombo4Optimization = 0;   // (reserved for optimization)

```

Recall that we find its range for optimization in the Iterate function. The first time we call it in OnTesterInit with a complete enumeration of combinations of fast and slow periods.

Basically, we could store all valid combinations in the array of structures PairOfPeriods and write it to a binary file for transmission to agents. Then, on the agents, our Expert Advisor could read the ready array from the file and by the FastSlowCombo4Optimization index extract the corresponding pair of FastOsMA and SlowOsMA from the array.

Instead, we will focus on a minimal change in the working logic of the program: we will continue to restore a couple of periods due to the second call Iterate in the OnInit handler. This time, we will get the range and step of enumeration of period values not from the shadow parameters, but from the CSV file.

Here are the changes to OnTesterInit.

```
int OnTesterInit()
{
   ...
        // check if the file already exists before compiling
        // - if not, the tester will not be able to send it to agents
         const bool preExisted = FileIsExist(SettingsFile);
         
         // write the settings to a file for transfer to copy programs on agents
         int handle = FileOpen(SettingsFile, FILE_WRITE | FILE_CSV | FILE_ANSI, ",");
         FileWrite(handle, "FastOsMA", start1, step1, stop1);
         FileWrite(handle, "SlowOsMA", start2, step2, stop2);
         FileClose(handle);
         
         if(!preExisted)
         {
            PrintFormat("Required file %s is missing. It has been just created."
               " Please restart again.",
               SettingsFile);
            ChartClose();
            return INIT_FAILED;
         }
   ...
   return INIT_SUCCEEDED;
}

```

Note that we have made the OnTesterInit handler with the return type int, which makes it possible to cancel optimization if the file does not exist. However, in any case, the actual data is written to the file, so if it did not exist, it is now created, and the subsequent start of the optimization will definitely be successful.

If you want to skip this step, you can create an empty file MQL5/Files/BandOsMAprofile.csv beforehand.

The OnInit handler has been changed as follows.

```
int OnInit()
{
   if(FastOsMA >= SlowOsMA) return INIT_PARAMETERS_INCORRECT;
   
   PairOfPeriods p = {FastOsMA, SlowOsMA}; // default initial parameters
   int handle = FileOpen(SettingsFile, FILE_READ | FILE_TXT | FILE_ANSI);
   
   // during optimization, a file with shadow parameters is needed
   if(MQLInfoInteger(MQL_OPTIMIZATION) && handle == INVALID_HANDLE)
   {
      return INIT_PARAMETERS_INCORRECT;
   }
   
   if(handle != INVALID_HANDLE)
   {
      if(FastSlowCombo4Optimization != -1)
      {
         // if there is a shadow copy, read the period values from it
         const string line1 = FileReadString(handle);
         string settings[];
         if(StringSplit(line1, ',', settings) == 4)
         {
            int FastStart = (int)StringToInteger(settings[1]);
            int FastStep = (int)StringToInteger(settings[2]);
            int FastStop = (int)StringToInteger(settings[3]);
            const string line2 = FileReadString(handle);
            if(StringSplit(line2, ',', settings) == 4)
            {
               int SlowStart = (int)StringToInteger(settings[1]);
               int SlowStep = (int)StringToInteger(settings[2]);
               int SlowStop = (int)StringToInteger(settings[3]);
               p = Iterate(FastStart, FastStop, FastStep,
                  SlowStart, SlowStop, SlowStep, FastSlowCombo4Optimization);
               PrintFormat("MA periods are restored from shadow: FastOsMA=%d SlowOsMA=%d",
                  p.fast, p.slow);
            }
         }
      }
      FileClose(handle);
   }

```

When running single tests after optimization, we will see decoded period values in the log FastOsMA and SlowOsMA based on the optimized value FastSlowCombo4Optimization. In the future, we can substitute these values in the period parameters, and delete the csv file. We also provided that the file will not be taken into account if FastSlowCombo4Optimization is set to -1.
