#!/bin/bash
# Generate PNG images from Mermaid diagram files

set -e

echo "SyInfo Documentation Diagram Generator"
echo "====================================="

# Check if mermaid-cli is installed
if ! command -v mmdc &> /dev/null; then
    echo "Error: mermaid-cli (mmdc) is not installed"
    echo "Please install it with: npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

# Create images directory if it doesn't exist
mkdir -p ../images

echo "Generating diagram images..."

# Generate each diagram
diagrams=(
    "package-architecture"
    "data-flow" 
    "cli-workflow"
    "monitoring-workflow"
    "system-components"
)

for diagram in "${diagrams[@]}"; do
    echo "  -> Generating ${diagram}.png..."
    mmdc -i "${diagram}.mmd" -o "../images/${diagram}.png" \
         --width 1200 --height 800 --backgroundColor white \
         --theme default --scale 2
done

echo ""
echo "Successfully generated $(echo ${#diagrams[@]}) diagram images in docs/images/"
echo ""
echo "Generated files:"
for diagram in "${diagrams[@]}"; do
    echo "  - images/${diagram}.png"
done

echo ""
echo "You can now reference these images in your documentation:"
echo "  RST: .. image:: images/package-architecture.png"
echo "  MD:  ![Architecture](images/package-architecture.png)"
