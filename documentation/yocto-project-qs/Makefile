# You must call this Makefile using the following form:
#
#     make
#     make html
#     make tarball
#     make clean
#     make publish
#
# "make" creates the HTML and tarball.
# "make html" creates just the HTML
# "make tarball" creates the tarball
# "make clean" removes the HTML file
# "make publish" pushes the HTML, figures, and stylesheet to the web server
#

XSLTOPTS = --stringparam html.stylesheet style.css \
         --xinclude

VER = 1.0
DOC = yocto-quick-start
ALLPREQ = html pdf tarball
TARFILES = yocto-project-qs.html style.css figures/yocto-environment.png figures/building-an-image.png figures/using-a-pre-built-image.png figures/yocto-project-transp.png
MANUALS = yocto-project-qs.html
FIGURES = figures
STYLESHEET = *.css

XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: html tarball

##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.

html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 

#	xsltproc $(XSLTOPTS) -o yocto-project-qs.html $(XSL_XHTML_URI) yocto-project-qs.xml
	xsltproc $(XSLTOPTS) -o yocto-project-qs.html yocto-project-qs-customization.xsl yocto-project-qs.xml

tarball: html
	cd $(DOC); tar -cvzf yocto-project-qs.tgz $(TARFILES); cd ..

validate:
	xmllint --postvalid --xinclude --noout yocto-project-qs.xml

publish:
	scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)
	scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)/figures

clean:
	rm -f $(MANUALS)
