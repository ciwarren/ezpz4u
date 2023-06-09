import requests, re, subprocess, json
from .config import Settings
# Uses pzlsm for server management: https://github.com/openzomboid/pzlsm

class PZServer():
    def __init__(self, settings):
        self.settings = settings

    def fetch_mod_list(self):
        res = requests.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={self.settings.collection_id}")
        content = res.content.decode()
        results = set(re.findall(r'sharedfile_(\d*)', content))
        self.workshop_string = ";".join(results)

        ids_list = []
        for res in results:
            raw = requests.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={res}").content.decode()
            ids = re.findall(r'Mod ID: ([A-Za-z]*)', raw)
            ids_list += ids
        self.ids_string = ";".join(ids_list)

    def update_mods_ini(self):
        with open(self.settings.server_config_path, "r") as fh:
            config_contents = fh.readlines()
        
        line_num = 0
        updated_mods = False
        updated_workshop = False
        for line in config_contents:
            
            if "WorkshopItems=" in line:
                updated_workshop = True
                config_contents[line_num] = f"WorkshopItems={self.workshop_string} \n"
            
            if "Mods=" in line:
                updated_mods = True
                config_contents[line_num] = f"Mods={self.ids_string} \n"
            
            if updated_mods and updated_workshop:
                break

            line_num += 1

        if not updated_workshop:
            config_contents.append(f"WorkshopItems={self.workshop_string} \n")
        if not updated_mods:
            config_contents.append(f"Mods={self.ids_string} \n")
        

        for line in config_contents:
            if line == "WorkshopItems=" or line == "Mods=":
                config_contents.remove(line)

        with open(self.settings.server_config_path, "w") as fh:
            fh.writelines(config_contents)

    def proxy_server_commands(self, action):
        stdout = subprocess.Popen(action, stdout=subprocess.PIPE).communicate()[0].decode()
        return stdout

    def start_server(self):
        self.proxy_server_commands(["sudo", "systemctl", "start", "pz"])
        return self.get_stats_server()
    
    def stop_server(self):
        self.proxy_server_commands(["sudo", "systemctl", "stop", "pz"])
        return self.get_stats_server()
    
    def restart_server(self):
        self.proxy_server_commands(["sudo", "systemctl", "restart", "pz"])
        return self.get_stats_server()
  
    def get_stats_server(self):
        return self.proxy_server_commands(["journalctl", "-u", "-n", "100", "pz.service"])

    def update_server_mods(self):
        self.fetch_mod_list()
        self.stop_server()
        self.update_mods_ini()
        self.start_server()
        return self.get_stats_server()

    def update_server(self):
        self.stop_server()
        self.update_server()
        self.start_server()
        return self.get_stats_server()

