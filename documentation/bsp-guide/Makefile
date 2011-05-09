XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
         --xinclude

##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.
XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: html pdf tarball

pdf:
	../tools/poky-docbook-to-pdf bsp-guide.xml ../template

html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	xsltproc $(XSLTOPTS) -o bsp-guide.html bsp-guide-customization.xsl bsp-guide.xml

tarball: html
	tar -cvzf bsp-guide.tgz style.css bsp-guide.html bsp-guide.pdf figures/bsp-title.png

validate:
	xmllint --postvalid --xinclude --noout bsp-guide.xml

MANUALS = bsp-guide.html bsp-guide.pdf
FIGURES = figures/*.png
STYLESHEET = *.css

publish:
	scp -r $(MANUALS) $(STYLESHEET) srifenbark@www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/bsp-guide
	scp -r $(FIGURES) srifenbark@www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/bsp-guide/figures

clean:
	rm -f $(OUTPUTS)
