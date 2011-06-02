DISTROVERSION=1.1
ifeq ($(DOC),bsp-guide)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = style.css bsp-guide.html bsp-guide.pdf figures/bsp-title.png
endif

ifeq ($(DOC),yocto-project-qs)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --xinclude
ALLPREQ = html tarball
TARFILES = yocto-project-qs.html style.css figures/yocto-environment.png figures/building-an-image.png figures/using-a-pre-built-image.png figures/yocto-project-transp.png
endif

ifeq ($(DOC),poky-ref-manual)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = poky-ref-manual.html style.css figures/poky-title.png figures/ss-sato.png
endif


ifeq ($(DOC),adt-manual)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = adt-manual.html adt-manual.pdf style.css figures/adt-title.png
endif

ifeq ($(DOC),kernel-manual)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = kernel-manual.html kernel-manual.pdf style.css figures/kernel-title.png figures/kernel-architecture-overview.png
endif


##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.
XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: $(ALLPREQ)

pdf:
	cd $(DOC); ../tools/poky-docbook-to-pdf $(DOC).xml ../template; cd ..
    
html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	cd $(DOC); xsltproc $(XSLTOPTS) -o $(DOC).html $(DOC)-customization.xsl $(DOC).xml; cd ..

tarball: html
	cd $(DOC); tar -cvzf $(DOC).tgz $(TARFILES); cd ..

validate:
	cd $(DOC); xmllint --postvalid --xinclude --noout $(DOC).xml; cd ..

MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = $(DOC)/figures/*.png
STYLESHEET = $(DOC)/*.css

publish:
	scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(DISTROVERSION)/$(DOC)
	scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(DISTROVERSION)/$(DOC)/figures

clean:
	rm -f $(MANUALS)
