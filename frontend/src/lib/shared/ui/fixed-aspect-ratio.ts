interface ActionOutput<Parameters> {
  update?: (parameters: Parameters) => void;
  destroy?: () => void;
}

function getDimensions(entry: ResizeObserverEntry) {
  if (entry.contentBoxSize) {
    // Firefox implements `contentBoxSize` as a single content rect, rather than an array
    const contentBoxSize: ResizeObserverSize = Array.isArray(
      entry.contentBoxSize
    )
      ? entry.contentBoxSize[0]
      : entry.contentBoxSize;
    return {
      width: contentBoxSize.inlineSize,
      height: contentBoxSize.blockSize,
    };
  } else {
    return { width: entry.contentRect.width, height: entry.contentRect.height };
  }
}

/** Enforces a fixed aspect ratio (width / height) on an element dynamically. */
export function fixedAspectRatio<NodeType extends HTMLElement>(
  node: NodeType,
  aspectRatio: number
): ActionOutput<number> {
  const nodeStyle = getComputedStyle(node);
  const verticalMargins =
    parseInt(nodeStyle.marginTop, 10) + parseInt(nodeStyle.marginBottom, 10);
  const horizontalMargins =
    parseInt(nodeStyle.marginLeft, 10) + parseInt(nodeStyle.marginRight, 10);

  const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
      const { height: parentHeight, width: parentWidth } = getDimensions(entry);
      const heightLimit = parentHeight - verticalMargins;
      const widthLimit = parentWidth - horizontalMargins;

      const computedHeight = widthLimit / aspectRatio;

      if (computedHeight > heightLimit) {
        const computedWidth = heightLimit * aspectRatio;
        node.style.flexBasis = `${computedWidth}px`;
        node.style.flexGrow = '0';
        node.style.height = `${heightLimit}px`;
      } else {
        node.style.height = `${computedHeight}px`;
      }
    }
  });

  if (node.parentElement !== null) {
    resizeObserver.observe(node.parentElement);
  }

  return {
    destroy() {
      resizeObserver.disconnect();
    },
  };

  // TODO: rotate the parking lot on vertical screens
}
