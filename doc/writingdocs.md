Writing Sidenote documents is easy
----------------------------------

Every column goes in its own <tt>.md</tt> Markdown file (see [daringfireball.net/...](http://daringfireball.net/projects/markdown/)).

1. Create a new directory, say <tt>doc</tt>.
   Here is the contents of the <tt>doc</tt> directory used to build this document:

        header.md
        main.md
        license.md
        opensource.md
        todo.md
        why.md
        writingdocs.md

2. There must be a file named <tt>header.md</tt> and a file named <tt>main.md</tt>
    * These files contain the header content and the left-column content, respectively.
3. The other <tt>.md</tt> files contain right-column content.
4. To link to a column, say <tt>opensource.md</tt>,  do:

   > <tt>&#91;Open source](&#35;&#35;opensource)</tt>

5. Then compile using <tt>[sidenote.py](##commandline)</tt>