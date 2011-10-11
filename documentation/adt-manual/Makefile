# You must call this Makefile using the following form:
#
#     make
#     make html
#     make pdf
#     make tarball
#     make clean
#     make publish
#
# "make" creates the HTML, PDF, and tarballs.
# "make html" creates just the HTML
# "make pdf" creates just the PDF
# "make tarball" creates the tarball
# "make clean" removes the HTML and PDF files
# "make publish" pushes the HTML, PDF, figures, and stylesheet to the web server
#

XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
VER = 1.0
DOC = adt-manual
ALLPREQ = html pdf tarball
TARFILES = adt-manual.html adt-manual.pdf style.css figures/adt-title.png
MANUALS = $(DOC).html $(DOC).pdf
FIGURES = figures
STYLESHEET = *.css

##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.
XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: html pdf tarball

pdf:
	../tools/poky-docbook-to-pdf adt-manual.xml ../template

##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.

html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 

#	xsltproc $(XSLTOPTS) -o adt-manual.html $(XSL_XHTML_URI) adt-manual.xml
	xsltproc $(XSLTOPTS) -o adt-manual.html adt-manual-customization.xsl adt-manual.xml

tarball: html
	cd $(DOC); tar -cvzf $(DOC).tgz $(TARFILES); cd ..

validate:
	xmllint --postvalid --xinclude --noout adt-manual.xml

publish:
	scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)
	scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)/figures

clean:
	rm -f $(MANUALS)
