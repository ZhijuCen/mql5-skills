# Working with tpl chart templates

MQL5 API provides two functions for working with templates. Templates are files with the extension tpl, which save the contents of the charts, that is, all their settings, along with plotted objects, indicators, and an EA (if any).

bool ChartSaveTemplate(long chartId, const string filename)

The function saves the current chart settings to a tpl template with the specified name.

The chart is set by the chartId, 0 means the current graph.

The name of the file to save the template (filename) can be specified without the ".tpl" extension: it will be added automatically. The default template is saved to the terminal_dir/Profiles/Templates/ folder and can then be used for manual application in the terminal. However, it is possible to specify not just a name, but also a path relative to the MQL5 directory, in particular, starting with "/Files/". Thus, it will be possible to open the saved template using [files](/en/book/common/files) operation functions, analyze, and, if necessary, edit them (see the example ChartTemplate.mq5 further along).

If a file with the same name already exists at the specified path, its contents will be overwritten.

We will look at a combined example for saving and applying a template a little later.

bool ChartApplyTemplate(long chartId, const string filename)

The function applies a template from the specified file to the chartId chart.

The template file is searched according to the following rules:

- If filename contains a path (starts with a backslash "\\" or a forward slash "/"), then the pattern is matched relative to the path terminal_data_directory/MQL5.
- If there is no path in the name, the template is searched for in the same place where the executable of the EX5 file is located, in which the function is called.
- If the template is not found in the first two places, it is searched for in the standard template folder terminal_dir/Profiles/Templates/.

Note that terminal_data_directory refers to the folder where modified files are stored, and its location may vary depending on the type of the operating system, username, and computer security settings. Normally it differs from the terminal_dir folder although in some cases (for example, when working under an account from the Administrators group), they may be the same. The location of folders terminal_data_directory and terminal_directory can be found using the [TerminalInfoString](/en/book/common/environment/env_descriptive) function (see constants TERMINAL_DATA_PATH and TERMINAL_PATH, respectively).

ChartApplyTemplate call creates a command that is added to the chart's message queue and is only executed after all previous commands have been processed.

Loading a template stops all MQL programs running on the chart, including the one that initiated the loading. If the template contains indicators and an Expert Advisor, its new instances will be launched.

For security purposes, when applying a template with an Expert Advisor to a chart, [trading permissions](/en/book/common/environment/env_permissions) can be limited. If the MQL program that calls the ChartApplyTemplate function has no permission to trade, then the Expert Advisor loaded using the template will have no permission to trade, regardless of the template settings. If the MQL program that calls ChartApplyTemplate is allowed to trade but trading is not allowed in the template settings, then the Expert Advisor loaded using the template will not be allowed to trade.

An example of script ChartDuplicate.mq5 allows you to create a copy of the current chart.

```
void OnStart()
{
   const string temp = "/Files/ChartTemp";
   if(ChartSaveTemplate(0, temp))
   {
      const long id = ChartOpen(NULL, 0);
      if(!ChartApplyTemplate(id, temp))
      {
         Print("Apply Error: ", _LastError);
      }
   }
   else
   {
      Print("Save Error: ", _LastError);
   }
}

```

First, a temporary tpl file is created using ChartSaveTemplate, then a new chart is opened (ChartOpen call), and finally, the ChartApplyTemplate function applies this template to the new chart.

However, in many cases, the programmer faces a more difficult task: not just apply the template but pre-edit it.

Using templates, you can change many chart properties that are not available using other MQL5 API functions, for example, the visibility of indicators in the context of timeframes, the order of indicator subwindows along with the objects applied to them, etc.

The tpl file format is identical to the chr files used by the terminal for storing charts between sessions (in the folder terminal_directory/Profiles/Charts/profile_name).

A tpl file is a text file with a special syntax. The properties in it can be a key=value pair written on a single line or some kind of group containing several key=value properties. Such groups will be called containers below because, in addition to individual properties, they can also contain other, nested containers.

The container starts with a line that looks like "<tag>", where tag is one of the predefined container types (see below), and ends with a pair of lines like "</tag>" (tag names must match). In other words, the format is similar in some sense to XML (without a header), in which all lexical units must be written on separate lines and tag properties are not indicated by their attributes (as in XML inside the opening part "<tag attribute1=value1...> "), but in the inner text of the tag.

The list of supported tags:

- chart — a root container with main chart properties and all subordinate containers;
- expert — a container with general properties of an Expert Advisor, for example, permission to trade (inside a chart);
- window — a container with window/subwindow properties and its subordinate containers (inside chart);
- object — a container with graphical object properties (inside window);
- indicator — a container with indicator properties (inside window);
- graph — a container with indicator chart properties (inside indicator);
- level — a container with indicator level properties (inside indicator);
- period — a container with visibility properties of an object or indicator on a specific timeframe (inside an object or indicator);
- inputs — a container with settings (input variables) of custom indicators and Expert Advisors.

The possible list of properties in key=value pairs is quite extensive and has no official documentation. If necessary, you can deal with these features of the platform yourself.

Here are fragments from one tpl file (the indents in the formatting are made to visualize the nesting of containers).

```
<chart>
id=0
symbol=EURUSD
description=Euro vs US Dollar
period_type=1
period_size=1
digits=5
...
<window>
  height=117.133747
  objects=0
  <indicator>
    name=Main
    path=
    apply=1
    show_data=1
    ...
    fixed_height=-1
  </indicator>
</window>
<window>
  <indicator>
    name=Momentum
    path=
    apply=6
    show_data=1
    ...
    fixed_height=-1
    period=14
    <graph>
      name=
      draw=1
      style=0
      width=1
      color=16748574
    </graph>
  </indicator>
  ...
</window>
</chart>

```

We have the TplFile.mqh header file for working with tpl files, with which you can analyze and modify templates. It has two classes:

- Container — to read and store file elements, taking into account the hierarchy (nesting), as well as to write to a file after possible modification;
- Selector — to sequentially traverse the elements of the hierarchy (Container objects) in search of a match with a certain query that writes as a string similar to an xpath selector ("/path/element[attribute=value]").

Objects of the Container class are created using a constructor that takes the tpl file descriptor to read as the first parameter and the tag name as the second parameter. By default, the tag name is NULL, which means the root container (the entire file). Thus, the container itself fills itself with content in the process of reading the file (see the read method).

The properties of the current element, that is, the "key=value" pairs located directly inside this container, are supposed to be added to the map MapArray<string,string> properties. Nested containers are added to the array Container *children[].

```
#include <MQL5Book/MapArray.mqh>
   
#define PUSH(A,V) (A[ArrayResize(A, ArraySize(A) + 1) - 1] = V)
   
class Container
{
   MapArray<string,string> properties;
   Container *children[];
   const string tag;
   const int handle;
public:
   Container(const int h, const string t = NULL): handle(h), tag(t) { }
   ~Container()
   {
      for(int i = 0; i < ArraySize(children); ++i)
      {
         if(CheckPointer(children[i]) == POINTER_DYNAMIC) delete children[i];
      }
   }
      
   bool read(const bool verbose = false)
   {
      while(!FileIsEnding(handle))
      {
         string text = FileReadString(handle);
         const int len = StringLen(text);
         if(len > 0)
         {
            if(text[0] == '<' && text[len - 1] == '>')
            {
               const string subtag = StringSubstr(text, 1, len - 2);
               if(subtag[0] == '/' && StringFind(subtag, tag) == 1)
               {
                  if(verbose)
                  {
                     print();
                  }
                  return true;       // the element is ready
               }
               
               PUSH(children, new Container(handle, subtag)).read(verbose);
            }
            else
            {
               string pair[];
               if(StringSplit(text, '=', pair) == 2)
               {
                  properties.put(pair[0], pair[1]);
               }
            }
         }
      }
      return false;
   }
   ...
};

```

In the read method, we read and parse the file line by line. If the opening tag of the form "<tag>", we create a new container object and continue reading in it. If a closing tag of the form "</tag>" with the same name, we return a flag of success (true) which means that the container has been generated. In the remaining lines, we read the "key=value" pairs and add them to the properties array.

We have prepared the Selector to search for elements in a template. A string with the hierarchy of the searched tags is passed to its constructor. For example, the string "/chart/window/indicator" corresponds to a chart that has a window/subwindow, which, in turn, contains any indicator. The search result will be the first match. This query, as a rule, will find the quotes chart, because it is stored in the template as an indicator named "Main" and goes at the beginning of the file, before other subwindows.

More practical queries specifying the name and value of a particular attribute. In particular, the modified string "/chart/window/indicator[name=Momentum]" will only look for the Momentum indicator. This search is different from calling ChartWindowFind, because here the name is specified without parameters, while ChartWindowFind uses a short name of the indicator, which usually includes parameter values, but they can vary.

For built-in indicators, the name property contains the name itself, and for custom ones, it will say "Custom Indicator". The link to the custom indicator is given in the path property as a path to the executable file, for example, "Indicators\MQL5Book\IndTripleEMA.ex5".

Let's see the internal structure of the Selector class.

```
class Selector
{
   const string selector;
   string path[];
   int cursor;
public:
   Selector(const string s): selector(s), cursor(0)
   {
      StringSplit(selector, '/', path);
   }
   ...

```

In the constructor, we decompose the selector query into separate components and save them in the path array. The current path component that is being matched in the pattern is given by the cursor variable. At the beginning of the search, we are in the root container (we are considering the entire tpl file), and the cursor is 0. As matches are found, cursor should increase (see the accept method below).

The operator [], with the help of which you can get the i-th fragment of the path, is overloaded in the class. It also takes into account that in the fragment, in square brackets, the pair "[key=value]" can be specified.

```
   string operator[](int i) const
   {
      if(i < 0 || i >= ArraySize(path)) return NULL;
      const int param = StringFind(path[i], "[");
      if(param > 0)
      {
         return StringSubstr(path[i], 0, param);
      }
      return path[i];
   }
   ...

```

The accept method checks if the element name (tag) and its properties (properties) match with the data specified in the selector path for the current cursor position. The this[cursor] record uses the above overload of the operator [] .

```
   bool accept(const string tag, MapArray<string,string> &properties)
   {
      const string name = this[cursor];
      if(!(name == "" && tag == NULL) && (name != tag))
      {
         return false;
      }
      
      // if the request has a parameter, check it among the properties
      // NB! so far only one attribute is supported, but many "tag[a1=v1][a2=v2]..." are needed
      const int start = StringLen(path[cursor]) > 0 ? StringFind(path[cursor], "[") : 0;
      if(start > 0)
      {
         const int stop = StringFind(path[cursor], "]");
         const string prop = StringSubstr(path[cursor], start + 1, stop - start - 1);
         
         // NB! only '=' is supported, but it should be '>', '<', etc.
         string kv[];   // key and value
         if(StringSplit(prop, '=', kv) == 2)
         {
            const string value = properties[kv[0]];
            if(kv[1] != value)
            {
               return false;
            }
         }
      }
      
      cursor++;
      return true;
   }
   ...

```

The method will return false if the tag name does not match the current fragment of the path, and also if the fragment contained the value of some parameter and it is not equal or is not in the array properties. In other cases, we will get a match of the conditions, as a result of which the cursor will move forward (cursor++) and the method will return true.

The search process will be completed successfully when the cursor reaches the last fragment in the request, so we need a method to determine this moment, which is isComplete.

```
   bool isComplete() const
   {
      return cursor == ArraySize(path);
   }
   
   int level() const
   {
      return cursor;
   }

```

Also, during the template analysis, there may be situations when we went through the container hierarchy part of the path (that is, found several matches), after which the next request fragment did not match. In this case, you need to "return" to the previous levels of the request, for which the method unwind is implemented.

```
   bool unwind()
   {
      if(cursor > 0)
      {
         cursor--;
         return true;
      }
      return false;
   }
};

```

Now everything is ready to organize the search in the hierarchy of containers (which we get after reading the tpl file) using the Selector object. All necessary actions will be performed by the find method in the Container class. It takes the Selector object as an input parameter and recursively calls itself while there are matches according to the method Selector::accept. Reaching the end of the request means success, and the find method will return the current container to the calling code.

```
   Container *find(Selector *selector)
   {
      const string element = StringFormat("%*s", 2 * selector.level(), " ")
         + "<" + tag + "> " + (string)ArraySize(children);
      if(selector.accept(tag, properties))
      {
         Print(element + " accepted");
         
         if(selector.isComplete())
         {
            return &this;
         }
         
         for(int i = 0; i < ArraySize(children); ++i)
         {
            Container *c = children[i].find(selector);
            if(c) return c;
         }
         selector.unwind();
      }
      else
      {
         Print(element);
      }
      
      return NULL;
   }
   ...

```

Note that as we move along the object tree, the find method logs the tag name of the current object and the number of nested objects, and does so with an indent proportional to the nesting level of the objects. If the item matches the request, the log entry is appended with the word "accepted".

It is also important to note that this implementation returns the first matching element and does not continue searching for other candidates, and in theory, this can be useful for templates because they often have several tags of the same type inside the same container. For example, a window may contain many objects, and an MQL program may be interested in parsing the entire list of objects. This aspect is proposed to be studied optionally.

To simplify the search call, a method of the same name has been added that takes a string parameter and creates the Selector object locally.

```
   Container *find(const string selector)
   {
      Selector s(selector);
      return find(&s);
   }

```

Since we are going to edit the template, we should provide methods for modifying the container, in particular, to add a key=value pair and a new nested container with a given tag.

```
   void assign(const string key, const string value)
   {
      properties.put(key, value);
   }
   
   Container *add(const string subtag)
   {
      return PUSH(children, new Container(handle, subtag));
   }
   
   void remove(const string key)
   {
      properties.remove(key);
   }

```

After editing, you will need to write the contents of the containers back to a file (same or different). A helper method save saves the object in the tpl format described above: starts with the opening tag "<tag>", continues by unloading all key=value properties, and calls save for nested objects, after which it ends with the closing tag "</tag>". The file descriptor is passed as a parameter for saving.

```
   bool save(const int h)
   {
      if(tag != NULL)
      {
         if(FileWriteString(h, "<" + tag + ">\n") <= 0)
            return false;
      }
      for(int i = 0; i < properties.getSize(); ++i)
      {
         if(FileWriteString(h, properties.getKey(i) + "=" + properties[i] + "\n") <= 0)
            return false;
      }
      for(int i = 0; i < ArraySize(children); ++i)
      {
         children[i].save(h);
      }
      if(tag != NULL)
      {
         if(FileWriteString(h, "</" + tag + ">\n") <= 0)
            return false;
      }
      return true;
   }

```

The high-level method of writing an entire template to a file is called write. Its input parameter (file descriptor) can be equal to 0, which means writing to the same file from which it was read. However, the file must be opened with permission to write.

It is important to note that when overwriting a Unicode text file, MQL5 does not write the initial UTF mark (the so-called BOM, Byte Order Mark), and therefore we have to do it ourselves. Otherwise, without the mark, the terminal will not read and apply our template.

If the calling code passes in the h parameter another file opened exclusively for writing in Unicode format, MQL5 will write the BOM automatically.

```
   bool write(int h = 0)
   {
      bool rewriting = false;
      if(h == 0)
      {
         h = handle;
         rewriting = true;
      }
      if(!FileGetInteger(h, FILE_IS_WRITABLE))
      {
         Print("File is not writable");
         return false;
      }
      
      if(rewriting)
      {
         // NB! We write the BOM manually because MQL5 does not do this when overwritten
         ushort u[1] = {0xFEFF};
         FileSeek(h, SEEK_SET, 0);
         FileWriteString(h, ShortArrayToString(u));
      }
      
      bool result = save(h);
      
      if(rewriting)
      {
         // NB! MQL5 does not allow to reduce file size,
         // so we fill in the extra ending with spaces
         while(FileTell(h) < FileSize(h) && !IsStopped())
         {
            FileWriteString(h, " ");
         }
      }
      return result;
   }

```

To demonstrate the capabilities of the new classes, consider the problem of hiding the window of a specific indicator. As you know, the user can achieve this by resetting the visibility flags for timeframes in the indicator properties dialog (tab Display). Programmatically, this cannot be done directly. This is where the ability to edit the template comes to the rescue.

In the template, indicator visibility for timeframes is specified in the container <indicator>, inside which a separate container is written for each visible timeframe <period>. For example, visibility on the M15 timeframe looks like this:

```
<period>
period_type=0
period_size=15
</period>

```

Inside the container <period> properties period_type and period_size are used. period_type is a unit of measurement, one of the following:

- 0 for minutes
- 1 for hours
- 2 for weeks
- 3 for months

period_size is the number of measurement units in the timeframe. It should be noted that the daily timeframe is designated as 24 hours.

When there is no nested container <period> in the container <indicator>, the indicator is displayed on all timeframes.

The book comes with the script ChartTemplate.mq5, which adds the Momentum indicator to the chart (if it is not already present) and makes it visible on a single monthly timeframe.

```
void OnStart()
{
   // if Momentum(14) is not on the chart yet, add it
   const int w = ChartWindowFind(0, "Momentum(14)");
   if(w == -1)
   {
      const int momentum = iMomentum(NULL, 0, 14, PRICE_TYPICAL);
      ChartIndicatorAdd(0, (int)ChartGetInteger(0, CHART_WINDOWS_TOTAL), momentum);
      // not necessarily here because the script will exit soon,
      // however explicitly declares that the handle will no longer be needed in the code
      IndicatorRelease(momentum);
   }
   ...

```

Next, we save the current chart template to a file, which we then open for writing and reading. It would be possible to allocate a separate file for writing.

```
   const string filename = _Symbol + "-" + PeriodToString(_Period) + "-momentum-rw";
   if(PRTF(ChartSaveTemplate(0, "/Files/" + filename)))
   {
      int handle = PRTF(FileOpen(filename + ".tpl",
         FILE_READ | FILE_WRITE | FILE_TXT | FILE_SHARE_READ | FILE_SHARE_WRITE));
      // alternative - another file open for writing only
      // int writer = PRTF(FileOpen(filename + "w.tpl",
      //    FILE_WRITE | FILE_TXT | FILE_SHARE_READ | FILE_SHARE_WRITE));

```

Having received a file descriptor, we create a root container main and read the entire file into it (nested containers and all their properties will be read automatically).

```
      Container main(handle);
      main.read();

```

Then we define a selector to search for the Momentum indicator. In theory, a more rigorous approach would also require checking the specified period (14), but our classes do not support querying multiple properties at the same time (this possibility is left for independent study).

Using the selector, we search, print the found object (just for reference) and add its nested container <period> with settings for displaying the monthly timeframe.

```
      Container *found = main.find("/chart/window/indicator[name=Momentum]");
      if(found)
      {
         found.print();
         Container *period = found.add("period");
         period.assign("period_type", "3");
         period.assign("period_size", "1");
      }

```

Finally, we write the modified template to the same file, close it and apply it on the chart.

```
      main.write(); // or main.write(writer);
      FileClose(handle);
      
      PRTF(ChartApplyTemplate(0, "/Files/" + filename));
   }
}

```

When running the script on a clean chart, we will see such entries in the log.

```
ChartSaveTemplate(0,/Files/+filename)=true / ok
FileOpen(filename+.tpl,FILE_READ|FILE_WRITE|FILE_TXT| »
» FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_UNICODE)=1 / ok
 <> 1 accepted
  <chart> 2 accepted
    <window> 1 accepted
      <indicator> 0
    <window> 1 accepted
      <indicator> 1 accepted
Tag: indicator
                    [key]    [value]
[ 0] "name"               "Momentum"
[ 1] "path"               ""        
[ 2] "apply"              "6"       
[ 3] "show_data"          "1"       
[ 4] "scale_inherit"      "0"       
[ 5] "scale_line"         "0"       
[ 6] "scale_line_percent" "50"      
[ 7] "scale_line_value"   "0.000000"
[ 8] "scale_fix_min"      "0"       
[ 9] "scale_fix_min_val"  "0.000000"
[10] "scale_fix_max"      "0"       
[11] "scale_fix_max_val"  "0.000000"
[12] "expertmode"         "0"       
[13] "fixed_height"       "-1"      
[14] "period"             "14"      
ChartApplyTemplate(0,/Files/+filename)=true / ok

```

It can be seen here that before finding the required indicator (marked "accepted"), the algorithm found the indicator in the previous, main window, but it did not fit, because its name is not equal to the desired "Momentum".

Now, if you open the list of indicators on the chart, there will be momentum, and in its properties dialog, on the Display tab the only enabled timeframe is Month.

The book is accompanied by an extended version of the file TplFileFull.mqh, which supports different comparison operations in the conditions for selecting tags and their multiple selection into arrays. An example of using it can be found in the script ChartUnfix.mq5, which unfixes the sizes of all chart subwindows.
