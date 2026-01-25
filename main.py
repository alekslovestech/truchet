"""
Graphical Text Renderer
Takes an input string and outputs a special graphical version of it.
"""
import argparse

from formatter import process_text, process_text_empty_space
from svg_render import display_svg, lines_to_svg


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Render text as Truchet-style graphics.")
    parser.add_argument("--word", "-w", metavar="TEXT", help="Text to render (if omitted, read from stdin)")
    parser.add_argument("--inverted", "-i", action="store_true", help="Use inverted (empty-space) style")
    parser.add_argument("--svg", "-s", action="store_true", help="Render as SVG and open in browser")
    args = parser.parse_args()

    if args.word is not None:
        user_input = args.word
    else:
        print("Graphical Text Renderer")
        print("=" * 30)
        user_input = input("Enter text to render: ")

    process = process_text_empty_space if args.inverted else process_text
    output = process(user_input)

    if args.word is None:
        print("\nOutput:")
    if args.inverted:
        print(output)
    else:
        print("\n" + output + "\n")

    if args.svg and output:
        lines = output.split("\n")
        svg = lines_to_svg(lines)
        display_svg(svg)


if __name__ == "__main__":
    main()

