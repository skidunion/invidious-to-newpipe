from sys import argv

import opml
import re


def main():
    if len(argv) != 3:
        print("Usage: main.py <input file> <output file>")
        print("  `input file` must be Invidious exported data as OPML")
        print("  `output file` will be used to save the converted CSV")

        exit(-1)

    with open(argv[1]) as input_file:
        exported_data = opml.from_string(input_file.read())
        root = exported_data[0]

        if root.title != "Invidious Subscriptions":
            print(f"Unknown root title: {root.title}")
            exit(-2)

        output = ["Channel ID,Channel URL,Channel Name"]

        for item in root:
            channel_id = re.search(
                ".*\/feed\/channel\/(.*)", item.xmlUrl).group(1)
            channel_url = f"http://www.youtube.com/channel/{channel_id}"

            output.append(f"\n{channel_id},{channel_url},{item.title}")

        with open(argv[2], "w") as output_file:
            output_file.writelines(output)


if __name__ == "__main__":
    main()
