
# Table of Contents

1.  [mc-backup-tool](#org1b968dc)
    1.  [Useage](#org5a62976)
    2.  [Dependencies](#orgbaf6305)
    3.  [Notes](#org18ff3aa)



<a id="org1b968dc"></a>

# mc-backup-tool

This tool backs up a Minecraft server live with retries, logging and snapshot safety.


<a id="org5a62976"></a>

## Useage

    python3 src/mcserver-backup.py /path/to/server_dir /path/to/backkups


<a id="orgbaf6305"></a>

## Dependencies

-   Python 3.10+ (standard libraries only)
-   pixz (for compression)
-   Cron or systemd timer or any thing that can run this script in a fix interval


<a id="org18ff3aa"></a>

## Notes

-   The program is developed by a beginner. If there are any obvious mistakes please kindly point it out.
-   The program is developed for UNIX system only. If window users want to use this, please modify the source code accordingly. But come on, who host a server in windows anyway.

