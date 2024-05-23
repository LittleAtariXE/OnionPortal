import os
from constructor.constructor import Constructor


class DockerBuilder:
    def __init__(self):
        self.Constructor = Constructor()
        self.conf = self.Constructor.conf
        self.docker_file_path = os.path.join(os.path.dirname(__file__), "Dockerfile")
        self.docker_builder_path = os.path.join(os.path.dirname(__file__), "DockerBuilder.py")
        self.run_file_path = os.path.join(os.path.dirname(__file__), "start.sh")
    
    def exposePort(self) -> str:
        expose = ""
        for port in self.conf["PORT_MAPPING"]:
            expose += f"EXPOSE {port[0]}\n"
        return expose
    
    def exposeExtraPort(self) -> str:
        expose = ""
        for port in self.conf["EXTRA_PORT"]:
            expose += f"EXPOSE {port[0]}\n"
        return expose

    def buildDockerfile(self) -> None:
        text = "FROM debian:latest\nLABEL Creator: "
        text += r"https://github.com/LittleAtariXE"
        text += "\nWORKDIR /app\n"
        text += "COPY . /app\n"
        text += "RUN apt update && \\\n\tapt install -y python3 python3-flask python3-requests python3-socks tor\n"
        text += "# Control Port:\n"
        text += f"EXPOSE {self.conf['CONTROL_PORT'][0]}\n"
        text += "# TOR Socks:\n"
        text += self.exposePort()
        text += "# Extra Opening Ports\n"
        text += self.exposeExtraPort()
        text += 'CMD ["python3", "app.py"]\n'
        with open(self.docker_file_path, "w") as f:
            f.write(text)
    
    def buildDockerImage(self) -> None:
        os.system(f"docker build -t {self.conf['IMAGE_NAME'].lower()} .")
    
    def buildDockerStartSh(self) -> None:
        text = "#!/bin/bash\n"
        
        ports = f"-p {self.conf['CONTROL_PORT'][0]}:{self.conf['CONTROL_PORT'][1]}"
        for port in self.conf["PORT_MAPPING"]:
            ports += f" -p {port[0]}:{port[1]}"
        for port in self.conf["EXTRA_PORT"]:
            ports += f" -p {port[0]}:{port[1]}"
        text += f"docker run --name {self.conf['CONTAINER_NAME']} {ports} {self.conf['IMAGE_NAME'].lower()}\n"
        with open(os.path.join(os.getcwd(), "start_portal.sh"), "w") as f:
            f.write(text)
        print("Docker Start File Ready")


    
if __name__ == "__main__":
    builder = DockerBuilder()
    print(builder.conf)
    builder.buildDockerfile()
    # builder.buildDockerImage()
    # builder.buildDockerStartSh()
    print("\nDONE")


