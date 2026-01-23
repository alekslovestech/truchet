"""
Graphical Text Renderer
Takes an input string and outputs a special graphical version of it.
"""
from formatter import process_text


def main():
    """Main entry point for the application."""
    print("Graphical Text Renderer")
    print("=" * 30)
    
    # Get input from user
    user_input = input("Enter text to render: ")
    
    # Process the text
    output = process_text(user_input)
    
    # Display the result
    print("\nOutput:")
    print(output)


if __name__ == "__main__":
    main()

