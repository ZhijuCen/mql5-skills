# Computing resources: memory, disk, and CPU

Like all programs, MQL applications consume computer resources, including memory, disk space, and CPU. Taking into account that the terminal itself is resources-intensive (in particular, due to the potential download of quotes and ticks for multiple financial instruments with a long history), sometimes it is necessary to analyze and control the situation in terms of the proximity of available limits.

The MQL5 API provides several properties that allow you to estimate the maximum achievable and expended resources. The properties are summarized in the ENUM_MQL_INFO_INTEGER and ENUM_TERMINAL_INFO_INTEGER enumerations.

| Identifier | Description |
| --- | --- |
| MQL_MEMORY_LIMIT | Maximum possible amount of dynamic memory for an MQL program in Kb |
| MQL_MEMORY_USED | Memory used by an MQL program in Mb |
| MQL_HANDLES_USED | Number of class objects |
| TERMINAL_MEMORY_PHYSICAL | Physical RAM in the system in Mb |
| TERMINAL_MEMORY_TOTAL | Memory (physical+swap file, i.e. virtual) available to the terminal (agent) process in Mb |
| TERMINAL_MEMORY_AVAILABLE | Free memory of the terminal (agent) process in Mb, part of TOTAL |
| TERMINAL_MEMORY_USED | Memory used by the terminal (agent) in Mb, part of TOTAL |
| TERMINAL_DISK_SPACE | Free disk space, taking into account possible quotas for the MQL5/Files folder of the terminal (agent), in Mb |
| TERMINAL_CPU_CORES | Number of processor cores in the system |
| TERMINAL_OPENCL_SUPPORT | Supported OpenCL  version as 0x00010002 = 1.2; "0" means that OpenCL is not supported |

The maximum amount of memory available to an MQL program is described by the MQL_MEMORY_LIMIT property. This is the only property listed that uses kilobytes (Kb). All others are returned in megabytes (Mb). As a rule, MQL_MEMORY_LIMIT is equal to TERMINAL_MEMORY_TOTAL, i.e., all memory available on the computer can be allocated to one MQL program by default. However, the terminal, in particular its cloud implementation for MetaTrader VPS, and cloud testing agents may limit the memory for a single MQL program. Then MQL_MEMORY_LIMIT will be significantly less than TERMINAL_MEMORY_TOTAL.

Since Windows typically creates a swap file that is equal in size to physical memory (RAM), the TERMINAL_MEMORY_TOTAL property can be up to 2 times the size of TERMINAL_MEMORY_PHYSICAL.

All available virtual memory TERMINAL_MEMORY_TOTAL is divided between used (TERMINAL_MEMORY_USED) and still free (TERMINAL_MEMORY_AVAILABLE) memory.

The book comes with the script EnvProvision.mq5, which logs all specified properties.

```
void OnStart()
{
   PRTF(MQLInfoInteger(MQL_MEMORY_LIMIT)); // Kb!
   PRTF(MQLInfoInteger(MQL_MEMORY_USED));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_PHYSICAL));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_TOTAL));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_AVAILABLE));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_USED));
   PRTF(TerminalInfoInteger(TERMINAL_DISK_SPACE));
   PRTF(TerminalInfoInteger(TERMINAL_CPU_CORES));
   PRTF(TerminalInfoInteger(TERMINAL_OPENCL_SUPPORT));
   
   uchar array[];
   PRTF(ArrayResize(array, 1024 * 1024 * 10)); // allocate 10 Mb
   PRTF(MQLInfoInteger(MQL_MEMORY_USED));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_AVAILABLE));
   PRTF(TerminalInfoInteger(TERMINAL_MEMORY_USED));
}

```

After the initial output of the properties, we allocate 10 Mb for the array and then check the memory again. A result example is shown below (you will have your own values).

```
MQLInfoInteger(MQL_MEMORY_LIMIT)=8388608 / ok
MQLInfoInteger(MQL_MEMORY_USED)=1 / ok
TerminalInfoInteger(TERMINAL_MEMORY_PHYSICAL)=4095 / ok
TerminalInfoInteger(TERMINAL_MEMORY_TOTAL)=8190 / ok
TerminalInfoInteger(TERMINAL_MEMORY_AVAILABLE)=7842 / ok
TerminalInfoInteger(TERMINAL_MEMORY_USED)=348 / ok
TerminalInfoInteger(TERMINAL_DISK_SPACE)=4528 / ok
TerminalInfoInteger(TERMINAL_CPU_CORES)=4 / ok
TerminalInfoInteger(TERMINAL_OPENCL_SUPPORT)=0 / ok
ArrayResize(array,1024*1024*10)=10485760 / ok
MQLInfoInteger(MQL_MEMORY_USED)=11 / ok
TerminalInfoInteger(TERMINAL_MEMORY_AVAILABLE)=7837 / ok
TerminalInfoInteger(TERMINAL_MEMORY_USED)=353 / ok

```

Note that the total virtual memory (8190) is twice the physical memory (4095). The amount of memory available for the script is 8388608 Kb, which is almost equal to the entire memory of 8190 Mb. Free (7842) and used (348) system memory also add up to 8190.

If before allocating memory for an array, the MQL program occupied 1 Mb, then after allocating it, it is already 11 Mb. Meanwhile, the amount of memory occupied by the terminal increased by only 5 Mb (from 348 to 353), since some resources were reserved in advance.
