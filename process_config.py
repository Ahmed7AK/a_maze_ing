def process_confg(config: dict) -> dict:
    process: dict = {}
    check = "WIDTH"
    try:
        if int(config["WIDTH"]) <= 2:
            raise Exception
        else:
            process["WIDTH"] = int(config["WIDTH"])

        check = "HEIGHT"
        if int(config["HEIGHT"]) <= 2:
            raise Exception
        else:
            process["HEIGHT"] = int(config["HEIGHT"])

        check = "ENTRY"
        entry = config["ENTRY"].split(",")
        entry[0], entry[1] = int(entry[0]), int(entry[1])
        process["ENTRY"] = tuple(entry)

        check = "EXIT"
        exit_t = config["EXIT"].split(",")
        exit_t[0], exit_t[1] = int(exit_t[0]), int(exit_t[1])
        process["EXIT"] = tuple(exit_t)

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
    except Exception:
        print(f"Invalid {check}")

    return process


def read_config(path: str) -> dict:
    '''Handles processing the config.txt file and edge cases'''
    possible_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED"
    ]
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
    except Exception as err:
        print(err)
        return {}

    config_dict = process_confg(config_dict)
    return config_dict


if __name__ == "__main__":
    res = read_config("config.txt")
    print(res)
