/** An mdast node rendered as the given HTML element. */
export function element(tagName, properties, children = []) {
  return {
    type: 'paragraph',
    data: { hName: tagName, hProperties: properties },
    children,
  };
}
