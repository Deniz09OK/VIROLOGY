// Persistence mechanisms — survive reboot and process kill — T1547, T1053.005
//
// registry        : HKCU\Software\Microsoft\Windows\CurrentVersion\Run (no admin needed)
// scheduled_task  : "OneDrive Updater Service" at logon, hidden (T1036.005 masquerade)
// watchdog        : RegisterWaitForSingleObject — respawn beacon if killed
