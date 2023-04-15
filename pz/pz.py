import requests, re, subprocess, json

# Uses pzlsm for server management: https://github.com/openzomboid/pzlsm



class PZServer():
    def __init__(self, config_path):
        self.config = json.load(config_path)
        self.collection_id = self.get("collection_id")
        self.server_management_path = self.get("server_management_path")
        self.server_config_path = self.get("server_config_path")

    def fetch_mod_list(self):
        res = requests.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={self.collection_id}")
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
        with open(self.server_config_path, "r") as fh:
            config_contents = fh.readlines()
        
        line_num = 0
        updated_mods = False
        updated_workshop = False
        for line in config_contents:
            
            if "WorkshopItems=" in line:
                config_contents[line_num] = f"WorkshopItems={self.workshop_string} \n"
                updated_workshop = True
            if "Mods=" in line:
                updated_mods = True
                config_contents[line_num] = f"Mods={self.ids_string} \n"
            
            if updated_mods and updated_workshop:
                break

            line_num += 1

        with open(self.server_config_path, "w") as fh:
            fh.writelines(config_contents)

    def proxy_server_commands(self, action):
        stdout = subprocess.Popen([self.server_management_path, action])
        return stdout

    def start_server(self):
        self.proxy_server_commands("start")
        return self.get_stats_server()
    
    def stop_server(self):
        self.proxy_server_commands("stop")
        return self.get_stats_server()
    
    def restart_server(self):
        self.proxy_server_commands("restart")
        return self.get_stats_server()
    def update_server(self):
        self.proxy_server_commands("update")
        return self.get_stats_server()
    
    def get_stats_server(self):
        return self.proxy_server_commands("stats")

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

