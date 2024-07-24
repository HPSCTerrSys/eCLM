# Prerequisites for JSC users

Before building and running eCLM on JSC machines, the following prerequisites should be fulfilled:

* Create a JSC/JuDoor account
* Join a compute time project
* Logging in to JSC machines

Follow the startup-guide <https://go.fzj.de/ibg-3-supercomputer-guide> for creating a JSC/JuDoor account, joining a compute time project and logging in to JSC machines. 

## Additional software for windows users

### Xming

Xming allows Windows machines to display a graphical Linux program which is running on a remote Linux server. You can download Xming <a href="http://www.straightrunning.com/XmingNotes/" target="_blank">here</a>.

To enable Xming in the PuTTY configuration, navigate to "Connection > SSH > X11" (left side panel), and check the box  "Enable X11 forwarding". If you save this configuration to your session, you only need to do this once.

```{image} ../../images/Putty_X11.png
:height: 400px 
```
<p>

If Xming is active, you will see its' symbol in your taskbar.

### WinSCP

WinSCP allows transferring files from your local system (e.g., laptop) to the cluster or vice-versa. You can download it <a href="https://winscp.net/eng/download.php" target="_blank">here</a>.

When you open WinSCP you need to connect to a "New site". You will need to fill in the "Host name", "User name", and "Password". Jureca host name is `jureca.fz-juelich.de`. Juwels host name is `juwels.fz-juelich.de`.

When you press "Login", you will be prompted to type in your passphrase for the SSH key that you created previously.

```{image} ../../images/winSCP.png
:height: 300px
``` 
<p>

After that, you will see two panels. To the left is your local system and to the right the JSC system. Simply drag a file or folder to transfer it from one system to the other.
