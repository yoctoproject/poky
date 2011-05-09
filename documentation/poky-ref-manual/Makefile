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
DOC = poky-ref-manual
ALLPREQ = html pdf tarball
TARFILES = poky-ref-manual.html poky-ref-manual.pdf style.css figures/yocto-project-transp.png figures/poky-ref-manual.png screenshots/ss-sato.png
MANUALS = $(DOC).html $(DOC).pdf
FIGURES = figures
SCREENSHOTS = screenshots
STYLESHEET = *.css

##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.
XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: html pdf tarball

pdf:
	../tools/poky-docbook-to-pdf poky-ref-manual.xml ../template

html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	xsltproc $(XSLTOPTS) -o poky-ref-manual.html poky-ref-manual-customization.xsl poky-ref-manual.xml

tarball: html
	cd $(DOC); tar -cvzf $(DOC).tgz $(TARFILES); cd ..

validate:
	xmllint --postvalid --xinclude --noout poky-ref-manual.xml

publish:
	scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)
	scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)/figures
	scp -r $(SCREENSHOTS) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)/screenshots

clean:
	rm -f $(MANUALS)
