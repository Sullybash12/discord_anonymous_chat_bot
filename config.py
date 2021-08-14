import yaml


def read_config():
    """Reads and parses data from config file."""

    with open("config.yaml", "r", encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    return data


def save_config(data):
    with open("config.yaml", "w") as file:
        thing = yaml.dump(data, file)


if __name__ == "__main__":
    print(read_config())
