# Prerequisites for JSC users

Before building and running eCLM on JSC machines, the following prerequisites should be fulfilled:

* Create a JSC/JuDoor account
* Join a compute time project
* Logging in to JSC machines


## Create a JSC/JuDoor account

You need a JSC account to access the HPC system. For that, you first need a JuDoor account for which you can register <a href="https://judoor.fz-juelich.de/register" target="_blank">here</a>.

Enter your e-mail address and click on "Send confirmation mail".

Afterwards, you will receive an e-mail from dispatch@jsc.de with a personalized link. Click on the link and fill in the form with your data.

Submit the form.

With this, the creation of your JSC account is completed. Now, you can log in to your <a href="https://judoor.fz-juelich.de/login" target="_blank">JuDoor account</a> with your username and password:


## Join a compute time project

Log in to your JuDoor account. Join the compute time project you were assigned to. Under "Projects", choose "+ Join a project":

Enter the project id. You can also add some additional information. Then you can join the project.

The PI/PA will be automatically informed about your join request and can add you to the different systems available in the project. Once you are approved to join the project compute time, you should be able to see the project id under "Projects".

## Logging in to JSC machines

To log in to one of the JSC machines you need a JSC account and access to a compute time project (see above).

The final step is to create and upload an SSH key for your account and local machine.

JSC provides thorough instructions for <a href="https://apps.fz-juelich.de/jsc/hps/juwels/access.html#openssh-key-generation" target="_blank">Juwels</a> and <a href="https://apps.fz-juelich.de/jsc/hps/jureca/access.html#openssh-key-generation" target="_blank">Jureca</a> on how to generate and upload SSH keys.


## Additional information on JSC machines

For the full user documentation regarding the JSC systems check:

* <a href="https://apps.fz-juelich.de/jsc/hps/juwels/index.html" target="_blank">Juwels documentation</a>
* <a href="https://apps.fz-juelich.de/jsc/hps/jureca/index.html" target="_blank">Jureca documentation</a>

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