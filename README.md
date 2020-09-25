# SEL810GUI
First run the SEL 810A emulator from https://github.com/phar/sel810emu.

then, load the HELLO_WORLD binary with the command:

load 0 sel810asm/asm/HELLO_WORLD_ORG_000000.BIN

Next, load the sel810gui.py, and then telnet to localhost port 9999

Now, if you click the start toggle, you should the string "HELLO WORLD!" print to the telnet client

Don't expect a lot more to work, still very WIP
