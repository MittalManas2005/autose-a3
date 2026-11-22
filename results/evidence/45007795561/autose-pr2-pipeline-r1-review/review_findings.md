# Independent reviewer findings (address every item)

The fix is minimal and correct: a valueless `data-toc-label` (stored as None by attr_list) is now ignored, the attribute is still removed, and the heading text is used. The full suite passes. The one gap is that `data-toc-label=""` still gives an empty TOC entry, which is unchanged existing behaviour.


