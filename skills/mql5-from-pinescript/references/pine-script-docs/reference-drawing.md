<!-- source: https://www.tradingview.com/pine-script-reference/v6/ | fetched 2026-09-23 | examples omitted -->

<!-- anchor: fun_label.new -->
Creates new label object.

#### Syntax & Overloads

label.new(point, text, xloc, yloc, color, style, textcolor, size, textalign, tooltip, text_font_family, force_overlay, text_formatting) → series label

label.new(x, y, text, xloc, yloc, color, style, textcolor, size, textalign, tooltip, text_font_family, force_overlay, text_formatting) → series label

#### Arguments

**point (chart.point) **A chart.point object that specifies the label's location.

**text (series string) **Label text. Default is empty string.

**xloc (series string) **See description of x argument. Possible values: xloc.bar_index and xloc.bar_time. Default is xloc.bar_index.

**yloc (series string) **Possible values are yloc.price, yloc.abovebar, yloc.belowbar. If yloc=yloc.price, y argument specifies the price of the label position. If yloc=yloc.abovebar, label is located above bar. If yloc=yloc.belowbar, label is located below bar. Default is yloc.price.

**color (series color) **Color of the label border and arrow

**style (series string) **Label style. Possible values: label.style_none, label.style_xcross, label.style_cross, label.style_triangleup, label.style_triangledown, label.style_flag, label.style_circle, label.style_arrowup, label.style_arrowdown, label.style_label_up, label.style_label_down, label.style_label_left, label.style_label_right, label.style_label_lower_left, label.style_label_lower_right, label.style_label_upper_left, label.style_label_upper_right, label.style_label_center, label.style_square, label.style_diamond, label.style_text_outline. Default is label.style_label_down.

**textcolor (series color) **Text color.

**size (series int/string) **Optional. Size of the label. Accepts a positive int value or one of the built-in `size.*` constants. The constants and their equivalent numeric sizes are: size.auto (0), size.tiny (~7), size.small (~10), size.normal (12), size.large (18), size.huge (24). The default value is size.normal, which represents the numeric size of 12.

**textalign (series string) **Label text alignment. Possible values: text.align_left, text.align_center, text.align_right. Default value is text.align_center.

**tooltip (series string) **Hover to see tooltip label.

**text_font_family (series string) **The font family of the text. Optional. The default value is font.family_default. Possible values: font.family_default, font.family_monospace.

**force_overlay (const bool) **If true, the drawing will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

**text_formatting (series text_format) **The formatting of the displayed text. Formatting options support addition. For example, `text.format_bold + text.format_italic` will make the text both bold and italicized. Possible values: text.format_none, text.format_bold, text.format_italic. Optional. The default is text.format_none.

#### Returns

Label ID object which may be passed to label.setXXX and label.getXXX functions.

#### See also

label.delete()label.set_x()label.set_y()label.set_xy()label.set_xloc()label.set_yloc()label.set_color()label.set_textcolor()label.set_style()label.set_size()label.set_textalign()label.set_tooltip()label.set_text()label.set_text_formatting()

<!-- anchor: fun_label.set_xy -->
Sets bar index/time and price of the label position.

#### Syntax

```
label.set_xy(id, x, y) → void
```

#### Arguments

**id (series label) **Label object.

**x (series int) **New bar index or bar time of the label position. Note that objects positioned using xloc.bar_index cannot be drawn further than 500 bars into the future.

**y (series int/float) **New price of the label position.

#### See also

label.new()

<!-- anchor: fun_label.set_text -->
Sets label text

#### Syntax

```
label.set_text(id, text) → void
```

#### Arguments

**id (series label) **Label object.

**text (series string) **New label text.

#### See also

label.new()label.set_text_formatting()

<!-- anchor: fun_label.delete -->
Deletes the specified label object. If it has already been deleted, does nothing.

#### Syntax

```
label.delete(id) → void
```

#### Arguments

**id (series label) **Label object to delete.

#### See also

label.new()

<!-- anchor: fun_table.new -->
The function creates a new table.

#### Syntax

```
table.new(position, columns, rows, bgcolor, frame_color, frame_width, border_color, border_width, force_overlay) → series table
```

#### Arguments

**position (series string) **Position of the table. Possible values are: position.top_left, position.top_center, position.top_right, position.middle_left, position.middle_center, position.middle_right, position.bottom_left, position.bottom_center, position.bottom_right.

**columns (series int) **The number of columns in the table.

**rows (series int) **The number of rows in the table.

**bgcolor (series color) **The background color of the table. Optional. The default is no color.

**frame_color (series color) **The color of the outer frame of the table. Optional. The default is no color.

**frame_width (series int) **The width of the outer frame of the table. Optional. The default is 0.

**border_color (series color) **The color of the borders of the cells (excluding the outer frame). Optional. The default is no color.

**border_width (series int) **The width of the borders of the cells (excluding the outer frame). Optional. The default is 0.

**force_overlay (const bool) **If true, the drawing will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

#### Returns

The ID of a table object that can be passed to other table.*() functions.

#### Remarks

This function creates the table object itself, but the table will not be displayed until its cells are populated. To define a cell and change its contents or attributes, use table.cell() and other table.cell_*() functions.

One table.new() call can only display one table (the last one drawn), but the function itself will be recalculated on each bar it is used on. For performance reasons, it is wise to use table.new() in conjunction with either the var keyword (so the table object is only created on the first bar) or in an if barstate.islast block (so the table object is only created on the last bar).

#### See also

table.cell()table.clear()table.delete()table.set_bgcolor()table.set_border_color()table.set_border_width()table.set_frame_color()table.set_frame_width()table.set_position()

<!-- anchor: fun_table.cell -->
The function defines a cell in the table and sets its attributes.

#### Syntax

```
table.cell(table_id, column, row, text, width, height, text_color, text_halign, text_valign, text_size, bgcolor, tooltip, text_font_family, text_formatting) → void
```

#### Arguments

**table_id (series table) **A table object.

**column (series int) **The index of the cell's column. Numbering starts at 0.

**row (series int) **The index of the cell's row. Numbering starts at 0.

**text (series string) **The text to be displayed inside the cell. Optional. The default is empty string.

**width (series int/float) **The width of the cell as a % of the indicator's visual space. Optional. By default, auto-adjusts the width based on the text inside the cell. Value 0 has the same effect.

**height (series int/float) **The height of the cell as a % of the indicator's visual space. Optional. By default, auto-adjusts the height based on the text inside of the cell. Value 0 has the same effect.

**text_color (series color) **The color of the text. Optional. The default is color.black.

**text_halign (series string) **The horizontal alignment of the cell's text. Optional. The default value is text.align_center. Possible values: text.align_left, text.align_center, text.align_right.

**text_valign (series string) **The vertical alignment of the cell's text. Optional. The default value is text.align_center. Possible values: text.align_top, text.align_center, text.align_bottom.

**text_size (series int/string) **Size of the object. The size can be any positive integer, or one of the size.* built-in constant strings. The constant strings and their equivalent integer values are: size.auto (0), size.tiny (8), size.small (10), size.normal (14), size.large (20), size.huge (36). The default value is size.normal or 14.

**bgcolor (series color) **The background color of the text. Optional. The default is no color.

**tooltip (series string) **The tooltip to be displayed inside the cell. Optional.

**text_font_family (series string) **The font family of the text. Optional. The default value is font.family_default. Possible values: font.family_default, font.family_monospace.

**text_formatting (series text_format) **The formatting of the displayed text. Formatting options support addition. For example, `text.format_bold + text.format_italic` will make the text both bold and italicized. Possible values: text.format_none, text.format_bold, text.format_italic. Optional. The default is text.format_none.

#### Remarks

This function does not create the table itself, but defines the table’s cells. To use it, you first need to create a table object with table.new().

Each table.cell() call overwrites all previously defined properties of a cell. If you call table.cell() twice in a row, e.g., the first time with text='Test Text', and the second time with text_color=color.red but without a new text argument, the default value of the 'text' being an empty string, it will overwrite 'Test Text', and your cell will display an empty string. If you want, instead, to modify any of the cell's properties, use the table.cell_set_*() functions.

A single script can only display one table in each of the possible locations. If table.cell() is used on several bars to change the same attribute of a cell (e.g. change the background color of the cell to red on the first bar, then to yellow on the second bar), only the last change will be reflected in the table, i.e., the cell’s background will be yellow. Avoid unnecessary setting of cell properties by enclosing function calls in an if barstate.islast block whenever possible, to restrict their execution to the last bar of the series.

#### See also

table.cell_set_bgcolor()table.cell_set_height()table.cell_set_text()table.cell_set_text_formatting()table.cell_set_text_color()table.cell_set_text_halign()table.cell_set_text_size()table.cell_set_text_valign()table.cell_set_width()table.cell_set_tooltip()

<!-- anchor: fun_line.new -->
Creates new line object.

#### Syntax & Overloads

line.new(first_point, second_point, xloc, extend, color, style, width, force_overlay) → series line

line.new(x1, y1, x2, y2, xloc, extend, color, style, width, force_overlay) → series line

#### Arguments

**first_point (chart.point) **A chart.point object that specifies the line's starting coordinate.

**second_point (chart.point) **A chart.point object that specifies the line's ending coordinate.

**xloc (series string) **See description of x1 argument. Possible values: xloc.bar_index and xloc.bar_time. Default is xloc.bar_index.

**extend (series string) **If extend=extend.none, draws segment starting at point (x1, y1) and ending at point (x2, y2). If extend is equal to extend.right or extend.left, draws a ray starting at point (x1, y1) or (x2, y2), respectively. If extend=extend.both, draws a straight line that goes through these points. Default value is extend.none.

**color (series color) **Line color.

**style (series string) **Line style. Possible values: line.style_solid, line.style_dotted, line.style_dashed, line.style_arrow_left, line.style_arrow_right, line.style_arrow_both.

**width (series int) **Line width in pixels.

**force_overlay (const bool) **If true, the drawing will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

#### Returns

Line ID object which may be passed to line.setXXX and line.getXXX functions.

#### See also

line.delete()line.set_x1()line.set_y1()line.set_xy1()line.set_x2()line.set_y2()line.set_xy2()line.set_xloc()line.set_color()line.set_extend()line.set_style()line.set_width()

<!-- anchor: fun_line.set_x2 -->
Sets bar index or bar time (depending on the xloc) of the second point.

#### Syntax

```
line.set_x2(id, x) → void
```

#### Arguments

**id (series line) **Line object.

**x (series int) **Bar index or bar time. Note that objects positioned using xloc.bar_index cannot be drawn further than 500 bars into the future.

#### See also

line.new()

<!-- anchor: fun_line.set_style -->
Sets the line style

#### Syntax

```
line.set_style(id, style) → void
```

#### Arguments

**id (series line) **Line object.

**style (series string) **New line style.

#### See also

line.style_solidline.style_dottedline.style_dashedline.style_arrow_leftline.style_arrow_rightline.style_arrow_bothline.new()

<!-- anchor: fun_line.set_color -->
Sets the line color

#### Syntax

```
line.set_color(id, color) → void
```

#### Arguments

**id (series line) **Line object.

**color (series color) **New line color

#### See also

line.new()

<!-- anchor: fun_line.delete -->
Deletes the specified line object. If it has already been deleted, does nothing.

#### Syntax

```
line.delete(id) → void
```

#### Arguments

**id (series line) **Line object to delete.

#### See also

line.new()
