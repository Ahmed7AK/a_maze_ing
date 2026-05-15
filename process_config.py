def process_config(path: str) -> dict:
    '''Handles processing the config.txt file and edge cases'''
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
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
                if key.upper() not in mandatory_keys:
                    raise OSError(f"Unknown key: {key}")
                config_dict[key] = value
    except OSError as err:
        print(err)
        return {}

    return config_dict


if __name__ == "__main__":
    res = process_config("confi.txt")
