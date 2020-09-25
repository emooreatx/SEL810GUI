# SEL810GUI
First run the SEL 810A emulator from https://github.com/phar/sel810emu.

then, load the HELLO_WORLD binary with the command:

load 0 sel810asm/asm/HELLO_WORLD_ORG_000000.BIN

python3 sel810emu.py
started external unit nulldev on /tmp/SEL810_nulldev
started external unit asr33 on /tmp/SEL810_asr33
started external unit paper tape on /tmp/SEL810_paper_tape
started external unit card punch on /tmp/SEL810_card_punch
started external unit card reader on /tmp/SEL810_card_reader
started external unit line printer on /tmp/SEL810_line_printer
started external unit TCU 1 on /tmp/SEL810_TCU_1
started external unit TCU 2 on /tmp/SEL810_TCU_2
started external unit typewriter on /tmp/SEL810_typewriter
started external unit X-Y plotter on /tmp/SEL810_X-Y_plotter
started external unit interval timer on /tmp/SEL810_interval_timer
started external unit movable head disc on /tmp/SEL810_movable_head_disc
started external unit CRT on /tmp/SEL810_CRT
started external unit fixed head disc on /tmp/SEL810_fixed_head_disc
started external unit NIXIE Minute Second on /tmp/SEL810_NIXIE_Minute_Second
started external unit NIXIE Day Hour on /tmp/SEL810_NIXIE_Day_Hour
started external unit NIXIE Months on /tmp/SEL810_NIXIE_Months
started external unit SWITCH0 on /tmp/SEL810_SWITCH0
started external unit SWITCH1 on /tmp/SEL810_SWITCH1
started external unit SWITCH2 on /tmp/SEL810_SWITCH2
started external unit RELAY0 on /tmp/SEL810_RELAY0
started external unit RELAY1 on /tmp/SEL810_RELAY1
started external unit SENSE0 on /tmp/SEL810_SENSE0
started external unit SENSE1 on /tmp/SEL810_SENSE1
started Control panel server on /tmp/SEL810_control_panel
Welcome to the SEL emulator/debugger. Type help or ? to list commands.

started ASR33 7-bit telnet driver on 0.0.0.0:9999
(SEL810x) load 0 sel810asm/asm/HELLO_WORLD_ORG_000000.BIN
test 0
(SEL810x)

Next, load the sel810gui.py, and then telnet to localhost port 9999

Now, if you click the start toggle, you should the string "HELLO WORLD!" print to the telnet client

Don't expect a lot more to work, still very WIP
