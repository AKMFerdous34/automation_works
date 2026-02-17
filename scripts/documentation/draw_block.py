def generate_svg(module_name, inputs, outputs, filename="block.svg"):

    width = 1920
    height = 1080
    block_width = 200

    num_ports = max(len(inputs), len(outputs))
    block_height = num_ports * 30 + 40

    x_block = 200
    y_block = 50

    svg = []

    svg.append(f'<svg width="{width}" height="{height}" '
               f'xmlns="http://www.w3.org/2000/svg">')

    # Draw rectangle
    svg.append(
        f'<rect x="{x_block}" y="{y_block}" '
        f'width="{block_width}" height="{block_height}" '
        f'style="fill:none;stroke:black;stroke-width:2"/>'
    )

    # Module name
    svg.append(
        f'<text x="{x_block + block_width/2}" '
        f'y="{y_block + block_height/2}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="16" font-weight="bold">'
        f'{module_name}</text>'
    )

    # Inputs
    for i, name in enumerate(inputs):
        y = y_block + 30 + i * 30

        # Arrow line
        svg.append(
            f'<line x1="{x_block - 80}" y1="{y}" '
            f'x2="{x_block}" y2="{y}" '
            f'style="stroke:black;stroke-width:2"/>'
        )

        # Arrow head
        svg.append(
            f'<polygon points="{x_block},{y} '
            f'{x_block-8},{y-5} '
            f'{x_block-8},{y+5}" '
            f'style="fill:black"/>'
        )

        # Text
        svg.append(
            f'<text x="{x_block - 85}" y="{y}" '
            f'text-anchor="end" dominant-baseline="middle">'
            f'{name}</text>'
        )

    # Outputs
    for i, name in enumerate(outputs):
        y = y_block + 30 + i * 30

        # Arrow line
        svg.append(
            f'<line x1="{x_block + block_width}" y1="{y}" '
            f'x2="{x_block + block_width + 80}" y2="{y}" '
            f'style="stroke:black;stroke-width:2"/>'
        )

        # Arrow head
        svg.append(
            f'<polygon points="{x_block + block_width + 80},{y} '
            f'{x_block + block_width + 72},{y-5} '
            f'{x_block + block_width + 72},{y+5}" '
            f'style="fill:black"/>'
        )

        # Text
        svg.append(
            f'<text x="{x_block + block_width + 85}" y="{y}" '
            f'dominant-baseline="middle">'
            f'{name}</text>'
        )

    svg.append('</svg>')

    with open(filename, "w") as f:
        f.write("\n".join(svg))

generate_svg("counter", ["clk", "rst_n","en","clr","up","a","b","c","d","e","f"],["count[4:0]", "overflow","underflow","error"])

