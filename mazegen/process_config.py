def process_config(config: dict) -> dict:
    '''This function handles processing the configuration into a usable dict'''
    process: dict = {}
    check = "WIDTH"
    try:
        if int(config["WIDTH"]) <= 1:
            raise Exception
        else:
            process["WIDTH"] = int(config["WIDTH"])

        check = "HEIGHT"
        if int(config["HEIGHT"]) <= 1:
            raise Exception
        else:
            process["HEIGHT"] = int(config["HEIGHT"])

        check = "ENTRY"
        entry = config["ENTRY"].split(",")
        if len(entry) != 2:
            raise Exception("ENTRY must be in format 'x,y'")
        entry[0], entry[1] = int(entry[0]), int(entry[1])
        process["ENTRY"] = tuple(entry)

        if entry[0] > process["WIDTH"] - 1 or \
           entry[0] < 0 or \
           entry[1] > process["HEIGHT"] - 1 or \
           entry[1] < 0:
            raise Exception

        check = "EXIT"
        exit_t = config["EXIT"].split(",")
        if len(exit_t) != 2:
            raise Exception("EXIT must be in format 'x,y'")
        exit_t[0], exit_t[1] = int(exit_t[0]), int(exit_t[1])
        process["EXIT"] = tuple(exit_t)

        if exit_t[0] > process["WIDTH"] - 1 or \
           exit_t[0] < 0 or \
           exit_t[1] > process["HEIGHT"] - 1 or \
           exit_t[1] < 0:
            raise Exception

        if entry == exit_t:
            raise Exception("ENTRY and EXIT cannot be the same")

        check = "OUTPUT_FILE"
        process["OUTPUT_FILE"] = config["OUTPUT_FILE"]

        check = "PERFECT"
        if config["PERFECT"] == "True":
            process["PERFECT"] = True
        elif config["PERFECT"] == "False":
            process["PERFECT"] = False
        else:
            raise Exception

        check = "SEED"
        process["SEED"] = int(config["SEED"])
    except Exception as err:
        print(f"Invalid {check}: {err}")

    return process


def read_config(path: str) -> dict:
    '''Handles reading the config.txt file'''
    possible_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED"
    ]
    config_dict: dict = {}
    try:
        config_dict: dict = {}
        with open(path, "r") as config:
            out = config.readlines()
            configuration = [c.strip() for c in out if c[0] != "#"]
            for setting in configuration:
                if setting.count("=") != 1:
                    raise OSError("Config Format: 'KEY=VALUE'")
                key, value = setting.split("=")
                if key.upper() not in possible_keys:
                    raise OSError(f"Unknown key: {key}")
                config_dict[key] = value
        if "SEED" not in config_dict.keys():
            config_dict["SEED"] = '42'
        if len(config_dict) < 7:
            raise OSError("Missing configurations")
        config_dict = process_config(config_dict)
    except Exception as err:
        print(err)
        return {}
    return config_dict
