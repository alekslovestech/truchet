"""
Graphical Text Renderer
Takes an input string and outputs a special graphical version of it.
"""
import argparse

from formatter import process_text
from svg.svg_render import display_svg, lines_to_svg
from tilestyle import TileStyle


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Render text as Truchet-style graphics.")
    parser.add_argument("--word", "-w", metavar="TEXT", help="Text to render (if omitted, read from stdin)")
    parser.add_argument("--style", "-t", choices=["bowtie", "circle", "triangle"], default="bowtie", help="Rendering style (default: bowtie)")
    parser.add_argument("--inverted", "-i", action="store_true", help="Use inverted (empty-space) style")
    parser.add_argument("--init_tile_flipped", "-f", action="store_true", help="First tile is hourglass (⧗), as opposed to the bowtie (⧓, default)")
    parser.add_argument("--svg", "-s", action="store_true", help="Render as SVG and open in browser")
    args = parser.parse_args()

    if args.word is not None:
        user_input = args.word
    else:
        print("Graphical Text Renderer")
        print("=" * 30)
        user_input = input("Enter text to render: ")

    output = process_text(user_input, is_inverted=args.inverted)

    if args.word is None:
        print("\nOutput:")
    if args.inverted:
        print(output)
    else:
        print("\n" + output + "\n")

    style = TileStyle(args.style)
    if args.svg and output:
        lines = output.split("\n")
        init_tile_flipped = not args.init_tile_flipped
        svg = lines_to_svg(lines, init_tile_flipped, style=style)
        display_svg(svg)

if __name__ == "__main__":
    main()

