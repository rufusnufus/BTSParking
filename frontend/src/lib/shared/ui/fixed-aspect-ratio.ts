/** Enforces a fixed aspect ratio (width / height) on an element dynamically. */
export default function fixedAspectRatio<NodeType extends HTMLElement>(
  node: NodeType,
  aspectRatio: number
): Record<string, never> {
  const { width } = node.getBoundingClientRect();
  const { height: parentHeight } = node.parentElement?.getBoundingClientRect() ?? { height: 0 };
  const nodeStyle = getComputedStyle(node);
  const verticalMargins = parseInt(nodeStyle.marginTop, 10) + parseInt(nodeStyle.marginBottom, 10);
  const heightLimit = parentHeight - verticalMargins;

  const computedHeight = width / aspectRatio;
  node.style.height = `${computedHeight}px`;

  if (computedHeight > heightLimit) {
    const computedWidth = heightLimit * aspectRatio;
    node.style.flexBasis = `${computedWidth}px`;
    node.style.flexGrow = '0';
    node.style.height = `${heightLimit}px`;
  }

  // TODO: add resize observer
  // TODO: rotate the parking lot on vertical screens

  return {};
}
