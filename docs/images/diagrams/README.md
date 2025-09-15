# SyInfo Documentation Diagrams

This directory contains Mermaid diagram source files for the SyInfo documentation.

## Diagrams

### 1. Package Architecture (`package-architecture.mmd`)
Shows the simplified package structure and module relationships after the over-engineering cleanup.

**Key Features:**
- Public API layer
- Core modules (device_info, network_info, sys_info)
- Support modules (monitoring, exceptions)
- External dependencies
- Clean separation of concerns

### 2. Data Flow (`data-flow.mmd`) 
Illustrates how data flows through the system from input sources to output formats.

**Flow Stages:**
- Input Sources → Data Collection → Processing → Output → Delivery
- Shows transformation and formatting steps
- Demonstrates multiple output formats (JSON, YAML, Tree, Tables)

### 3. CLI Workflow (`cli-workflow.mmd`)
Detailed flowchart of the flag-based CLI interface logic.

**Features:**
- Flag detection and routing
- Output option handling
- Error and help flows
- Decision trees for different combinations

### 4. Monitoring Workflow (`monitoring-workflow.mmd`)
Sequence diagram showing the real-time monitoring process.

**Process:**
- User command → Monitor creation → Background thread → Data collection → Output
- Shows timing and threading aspects
- Demonstrates JSON vs formatted output paths

### 5. System Components (`system-components.mmd`)
High-level overview of all system components and their relationships.

**Components:**
- User interfaces (CLI, API)
- Core functionality modules  
- Real-time monitoring
- Output formats
- Data sources

## Usage

### Rendering Diagrams

These Mermaid diagrams can be rendered using:

1. **GitHub/GitLab** - Automatic rendering in markdown files
2. **Mermaid CLI** - Generate PNG/SVG files
3. **Online Editor** - https://mermaid.live/
4. **IDE Extensions** - VSCode, etc.

### Generating Images

To generate PNG images from these diagrams:

```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Generate images  
mmdc -i package-architecture.mmd -o ../images/package-architecture.png
mmdc -i data-flow.mmd -o ../images/data-flow.png
mmdc -i cli-workflow.mmd -o ../images/cli-workflow.png
mmdc -i monitoring-workflow.mmd -o ../images/monitoring-workflow.png
mmdc -i system-components.mmd -o ../images/system-components.png
```

### Including in Documentation

Reference in RST files:
```rst
.. image:: images/package-architecture.png
   :alt: SyInfo Package Architecture
   :width: 800
```

Reference in Markdown:
```markdown
![SyInfo Package Architecture](images/package-architecture.png)
```

## Maintenance

- Update diagrams when architecture changes
- Keep diagrams in sync with code structure
- Regenerate images after updates
- Test rendering in different environments
