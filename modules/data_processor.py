import csv

def save_long_data(long_data, output_file):
    if not long_data:
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=long_data[0].keys()
        )
        writer.writeheader()
        writer.writerows(long_data)


def filter_data(long_data, config):
    return list(filter(
        lambda x: (x["continent"] == config["region"])
                  and (x["year"] == int(config["year"]))
                  and (config["country"] is None or x["country"] == config["country"]),
        long_data
    ))

    
def compute_stat(filtered_data, operation):
    values = list(map(lambda x: x["value"], filtered_data))
    if not values:
        return 0
    if operation == "average":
        return sum(values)/len(values)
    elif operation == "sum":
        return sum(values)
    else:
        raise ValueError(f"Invalid operation: {operation}")