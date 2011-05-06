XSLTOPTS = --stringparam html.stylesheet style.css \
         --xinclude

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
	tar -cvzf yocto-project-qs.tgz yocto-project-qs.html style.css figures/yocto-environment.png figures/building-an-image.png figures/using-a-pre-built-image.png figures/yocto-project-transp.png

validate:
	xmllint --postvalid --xinclude --noout yocto-project-qs.xml

MANUALS = yocto-project-qs.html
FIGURES = figures/*.png
STYLESHEET = *.css

publish:
	scp -r $(MANUALS) $(STYLESHEET) srifenbark@www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/yocto-quick-start
	scp -r $(FIGURES) srifenbark@www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/yocto-quick-start/figures

clean:
	rm -f $(MANUALS)
