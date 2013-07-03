<tt>mknote.sh</tt>
------------------

Creates a new, minimal Sidenote document.

Usage:

    ./mknote.sh new_directory_name

Where <tt>new_directory_name</tt> is the name of a new directory that <tt>mknote.sh</tt> will create.

### <tt>mknote.sh</tt> does the following:

1. Creates <tt>new_directory_name</tt> to hold your document's <tt>.md</tt> files.
2. Creates a [<tt>sidenote.sh</tt>](##sidenote_sh) script, which you can use to compile this specific document.
3. Creates a minimal <tt>[header.md](##header_file)</tt> file.
4. Creates a minimal <tt>[main.md](##main_file)</tt> file.
5. Copies necessary javascript files into <tt>new_directory_name</tt>.
