
# Table of Contents

1.  [mc<sub>backup</sub><sub>tool</sub>](#orge202ae7)
    1.  [Useage](#org406d5df)
    2.  [Dependencies](#org645ecc4)
    3.  [Notes](#org3ac3314)



<a id="orge202ae7"></a>

# mc<sub>backup</sub><sub>tool</sub>

This tool backs up a Minecraft server live with retries, logging and snapshot safety.


<a id="org406d5df"></a>

## Useage

    python3 src/mcserver-backup.py /path/to/server_dir /path/to/backkups


<a id="org645ecc4"></a>

## Dependencies

-   Python 3.10+ (standard libraries only)
-   pixz (for compression)
-   Cron or systemd timer or any thing that can run this script in a fix interval


<a id="org3ac3314"></a>

## Notes

-   The program is developed by a beginner. If there are any obvious mistakes please kindly point it out.
-   Some features that will be added in later on include multiple compression level of format.
-   The program is developed for UNIX system only. If window users want to use this, please modify the source code accordingly. But come on, who host a server in windows anyway.

