## Disable Tracker Procedure

Follow these steps to disable the Winegard G2 portable satellite
dish's tracker procedure.

1) Remove power from the satellite dish

2) Connect your computer to the RJ12 port via the RS422 converter

3) Disconnect both stepper motors from the controller board. This
will prevent the dish from spinning while re-programming it.

4) Apply power to the satellite dish

5) Using a serial program (eg: PuTTY), open a serial connection
using the COM port (eg: `/dev/ttyUSB0`) and a baud rate of `115200`.

6) Enter `nvs` to enter the non volatile storage menu:
```
TRK>nvs
NVS>
```

7) Enter `d 20` and confirm this is the tracker procedure option:
```
NVS>d 20
Num  Name                         Current      Saved      Default
---- --------------------------  ----------  ----------  ----------
 20) Disable Tracker Proc?            FALSE       FALSE       FALSE
```

8) Enter `e 20 1` to disable the tracker procedure:
```
NVS>e 20 1
 20) Disable Tracker Proc?           FALSE .       TRUE
```

9) Enter `s` to save the change:
```
NVS>s
    Saving ... 
Flash file flashx:bank0 opened
Flash sector cache enabled.
Flash doneSuccess
```

10) Remove power from the satellite dish

11) Reconnect both stepper motors to the controller board

12) Apply power to the satellite dish to confirm the tracker procedure
is now disabled