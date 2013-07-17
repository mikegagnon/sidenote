Creating documents with Sidenote is simple
------------------------------------------

The Sidenote compiler joins a group of [Markdown](##markdown) files into a single <tt>html</tt> file.

Steps to create a new Sidenote document:

1. [Download Sidenote](##download) with <tt>git clone</tt>.
2. Run [<tt>mknote.sh</tt>](##mknote) to create a new, minimal Sidenote document.
3. Use [Markdown syntax](##markdown) to author [as many <tt>.md</tt> files as you like](##other_md_file)
4. Use [Sidenote-link syntax](##sidenote_link) to link to a column.
5. Use [Tilde-anchor syntax](##tilde_anchor) to define mulitple columns in the same Markdown file.
6. There are two special <tt>.md</tt> files:
    1. The [<tt>header.md</tt>](##header_file)
    2. The [<tt>main.md</tt>](##main_file)
7. Use <tt>[sidenote.sh](##sidenote_sh)</tt> to compile your directory of <tt>.md</tt> files into a single html file.

Use the [Style Guide](##styleguide) when writing Sidenote documents.

~tilde_anchor
### Tilde-anchor syntax

You can define several independent columns in the same Markdown file using *tilde-anchor* syntax.

Example <tt>main.md</tt> that uses tilde anchors:

		# Main header
		blah blah...
		[link to column #2](##column2)
		[link to column #3](##col3)

		~column2
		# Column2 header
		blah blah...

		~col3
		# Column3 header
		blah blah...

In this example, <tt>main.md</tt> defines three independent columns:

* <tt>main<tt>
* <tt>column2<tt>
* <tt>col3<tt>
