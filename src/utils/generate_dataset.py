import argparse

from utils.handle_datasets import save_dataset


def generate_datasets(topics):
    print(topics)
    for topic in topics:
        print(topic)
        save_dataset(topic)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate datasets on passed topics.")
    parser.add_argument("topics", nargs="+", action="append", help="Topics to be queried on Twitter.")
    args = parser.parse_args()
    generate_datasets(args.topics[0])
