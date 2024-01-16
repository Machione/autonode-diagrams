# Autonode Diagrams

The Python [Diagrams](https://diagrams.mingrammer.com) project is an excellent resource for drawing technical diagrams using code, allowing diagrams to be version controlled easily and you to spend time writing content rather than fussing over formatting.

However, one current limitation is that all nodes of the diagram must have both a label and an icon to be displayed. Although [Diagrams](https://diagrams.mingrammer.com) comes with a large number of relevant node types and corresponding icons pre-installed, and the [custom node](https://diagrams.mingrammer.com/docs/nodes/custom) allows you to extend this even further, sometimes you don't have a suitable icon for the node available, or you want to quickly generate a diagram and worry about populating the icons later.

This package extends the [Diagram's Custom Node](https://diagrams.mingrammer.com/docs/nodes/custom) and automatically generates an icon based on the text in the node's label if no icon is provided. It is designed to be used in conjunction with, not as a replacement to, [Diagrams](https://diagrams.mingrammer.com).

![Demonstration](https://raw.githubusercontent.com/Machione/autonode-diagrams/main/demonstration.png)

## Installation

This [package is available on PyPI](https://pypi.org/project/autonode-diagrams/) for installation. Use Pip or your preferred method of installing Python packages.

```shell
pip install autonode-diagrams
```

## Quick Start

Most of this code is taken from the [Diagram's Quick Start guide](https://diagrams.mingrammer.com/docs/getting-started/installation#quick-start) plus [Custom nodes with remote icons guide](https://diagrams.mingrammer.com/docs/nodes/custom#custom-with-remote-icons). This is to show how Autonode Diagram's `Icon` class integrates seamlessly with the rest of the regular Python Diagram's functionality, allowing the two to be used side-by-side.

```python
from diagrams import Diagram
from diagrams.programming.language import Python
from diagrams.custom import Custom
from autonode_diagrams import Icon
from urllib.request import urlretrieve

with Diagram("Quick Start", show=False):
    # Get a remote PNG to prove that autonode_diagrams.Icon can also work just like normal diagrams.custom.Custom
    emoji_url = "https://openmoji.org/php/download_asset.php?type=emoji&emoji_hexcode=2728&emoji_variant=color"
    emoji_fp = "./sparkle.png"
    urlretrieve(emoji_url, emoji_fp) # You can delete this file later
    
    Icon("Just a label, no icon given", border=True) >> Python("Autonode Diagrams") >> Icon("Something beautiful", emoji_fp)
```

## Prerequisites

- Arial font.
- Python [Diagrams](https://diagrams.mingrammer.com/docs/getting-started/installation) along with their dependencies (specifically [Graphviz](https://graphviz.gitlab.io/download/) will need to be installed).
