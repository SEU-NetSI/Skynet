# stm32-openocd-config
Config flies included for debuging stm32 by vscode-IDE
## device list
- Crazyflie 2.X * 1
- debug adapter
- ARM Jlink Debugger

## software environment
- vscode IDE
- openocd debug tools
- Jlink Drivers
- Ubuntu 18.04 (x64)

### 1. Software Configuration(Debug in CLI)
- You should download Jlink drivers first: J-Link Software and Documentation Pack,choose the right version for your system.
<a href = "https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack">Download site</a>
- After download and install,execute command:
```
JlinkExe
```
- If it connect successfully,you can use Jlink Debugger debug.Here is the primary command:
<table border = "1">
<tr>
<td><b>Command</b></td>
<td><b>Introduction</b></td>
</tr>
<tr>
<td>f</td>
<td>Firmware info</td>
</tr>
<tr>
<td>h</td>
<td>halt</td>
</tr>
<tr>
<td>isHalted</td>
<td>Returns the current CPU state(halt / running)</td>
</tr>
<tr>
<td>WaitHalt</td>
<td>Waits until the CPU is halted or the given timeout is exceeded.</td>
</tr>
<tr>
<td>g</td>
<td>go</td>
</tr>
<tr>
<td>Sleep</td>
<td>Waits the given time(in milliseconds)</td>
</tr>
<tr>
<td>s</td>
<td>single step the target chip</td>
</tr>
<tr>
<td>st</td>
<td>show hardware status</td>
</tr>
<tr>
<td>hwinfo</td>
<td>Show hardware info</td>
</tr>
</table>

- install the openocd tools:
```
sudo apt install openocd
```
- check version:
```
openocd -v
```
- openocd working regulation:

<img src="https://seunetsi.feishu.cn/docs/doccn8FNbjgemrNvCBNnmFsWZzg">

> Here openocd is a GDB Server

openocd command:

<table border = "1">
<tr>
<td><b>Option</b></td>
<td><b>Option(abbr)</b></td>
<td><b>Function</b></td>
</tr>
<tr>
<td>--help</td>
<td>-h</td>
<td>display this help</td>
</tr>
<tr>
<td>--version</td>
<td>-v</td>
<td>display Openocd version</td>
</tr>
<tr>
<td>--file</td>
<td>-f</td>
<td>use configuration file <name></td>
</tr>
<tr>
<td>--search</td>
<td>-s</td>
<td>dir to search for config files and scripts</td>
</tr>
<tr>
<td>--debug</td>
<td>-d</td>
<td>set debug level <0-3></td>
</tr>
<tr>
<td>--log_output</td>
<td>-l</td>
<td>redirect log output to file<name></td>
</tr>
<tr>
<td>--command</td>
<td>-c</td>
<td>run <command></td>
</tr>
</table>

- openocd debug command:

build gdb server

```
openocd -f interface/jlink.cfg -f target/stm32f4x.cfg -c init -c targets 'transport select swd
```

connect gdb server

```
telnet localhost 4444
```

### 2. VSCode Environment Configuration(Debug in GUI)
Install the cortex-debug extension,use the following files:

- openocd.cfg

used for openocd configuration

- stm32f405.svd

contains some chip and Peripherals info

- .vscode/

contains c_cpp_properties.json and launch.json,the former specify compiler,the latter sets some debug information.








