<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div align="center">Not Ready Yet !!!!</div>
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
        <a href="#configuration">Configuration</a>
    </div>
    <div id="requirements">
        <h2 align="center">Requirements</h2>
        <ul>
            <li>Linux (Tested on ParrotOS)</li>
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
</body>
</html>
