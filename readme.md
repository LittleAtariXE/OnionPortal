<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div id="title" align="center"><h1>Onion Portal</h1></div>
    <div align="center">
        <img src="web_api/static/img/portal2.jpg" style="width: 50%;">
    </div>
    <br/>
    <div align="center">
        <p>The Docker image contains multiple TOR proxies, making it highly configurable and flexible. It includes an HTTP API built with Flask. The image and container creation, along with the entire configuration process, is fully automated. The application also generates the startup command for the image, so you don't have to manually input, for example, 20 ports in the Docker command.</p>
    </div>
    <div id="content" align="center">
        <a href="#requirements">Requirements</a> &nbsp;|&nbsp;
        <a href="#installation">Installation</a> &nbsp;|&nbsp;
        <a href="#configuration">Configuration</a> &nbsp;|&nbsp;
        <a href="#handling">Handling the Program</a> &nbsp;|&nbsp;
        <a href="#controls">Controls</a> &nbsp;|&nbsp;
        <a href="#screenshot">Screenshot</a>
    </div>
    <div id="requirements">
        <h2 align="center">Requirements</h2>
        <ul>
            <li>Linux (Tested on ParrotOS, Debian)</li>
            <li>Docker installed</li>
            <li>Python 3.11</li>
        </ul>
    </div>
    <div id="installation">
        <h2 align="center">Installation</h2>
        <ol>
            <li>Clone the repository:
                <pre><code>git clone https://github.com/LittleAtariXE/OnionPortal</code></pre>
            </li>
        </ol>
    </div>
    <div id="configuration">
        <h2 align="center">Configuration</h2>
        <p>Navigate to the repository and edit the "CONSTRUCTOR.ini" file.
            <br/>You will find a description of each option and a sample configuration.
            <br/>After editing the file, run "Build.py":
            <pre><code>python3 Build.py</code></pre>
        </p>
        <p>If your user does not belong to the Docker group, you may need to use the command:
            <pre><code>sudo python3 Build.py</code></pre>
        </p>
        <p>This command will automatically build the Docker image according to the configuration in the CONSTRUCTOR.ini file, create a container from the image, and prepare a ready-to-use start command. You do not need to manually enter all the ports. After completing all the steps and creating the image, a "start_portal.sh" file will appear. Run this file with the command:
            <pre><code>sh start_portal.sh</code></pre>
            <br/>This will start the application.
        </p>
    </div>
    <div id="handling">
        <h2 align="center">Handling the Program</h2>
        <p>To manage the TOR proxies, you need to connect to the application through a web browser. Open your browser and navigate to the address:
            <pre><code>http://127.0.0.1:CONTROL_PORT</code></pre>
            <br/>Replace <code>CONTROL_PORT</code> with the actual control port number specified in your configuration. The application interface will be displayed, allowing you to manage the proxies.
        </p>
    </div>
    <div id="controls">
        <h2 align="center"> Controls </h2>
        <div id="controls-portals">
            <p align="center"><strong>SECTION: Portals:</strong></p>
            <p><strong>START:</strong> This function starts all non-running TOR proxies. It will only start the "not running" portals.</p>
            <p><strong>STOP:</strong> This function stops all TOR proxies. A few seconds after stopping, the portals will reload, allowing you to start them again.</p>
            <p>When you click on the portal icon, you will enter the portal information. Here you can also use the START and STOP functions, but they will only work on that specific portal.</p>
            <p><strong>NEW CIRCUIT:</strong> This function attempts to create a new circuit. This is dependent on the TOR network.</p>
            <p>Each portal object will automatically fetch the IP address of the Exit Node.</p>
            <p>If you need to reload a portal (due to errors, etc.), use the STOP function. Wait a few seconds, and the portal will be available to start again.</p>
            <p>Each portal also displays whether it is connected to TOR and the TOR Proxy port.</p>
            <p>Note: Portals update automatically, but the display on the page does not. Using the "refresh" button will update the portal information.</p>
        </div>
        <div id="controls-logs">
            <p align="center"><strong>SECTION: Show Logs:</strong></p>
            <p>Here you can browse the logs. Selecting "Master" displays the logs of the entire program. It shows when a portal connected to TOR, when it obtained an IP address, etc.</p>
            <p>Each portal has separate logs, which are logged when the connection to TOR is established. These are standard TOR logs.</p>
         </div>
        <div id="controls-add-portal">
            <p align="center"><strong>SECTION: Add Portal:</strong></p>
            <p>In this section, you can add an additional portal on one of the selected ports from EXTRA_PORT. You cannot add more portals than the number of EXTRA_PORT.</p>
            <p>If you need more proxies, you must edit the CONSTRUCTOR.ini file and increase the number of EXTRA_PORT, then build a new container.</p>
            <p>Each added portal will appear in the Portals section.</p>
        </div>
    </div>
    <br/>
    <br/>
    <div id="screenshot">
        <h2 align="center">Screenshot</h2>
        <div align="center">
            <img src="screenshot/p1.jpg">
        </div>
        <br/>
        <div align="center">
            <img src="screenshot/p2.jpg">
        </div>
        <br/>
        <div align="center">
            <img src="screenshot/p3.jpg">
        </div>
        <br/>
        <div align="center">
            <img src="screenshot/p4.jpg">
        </div>
        <br/>
    </div>
</body>
</html>
