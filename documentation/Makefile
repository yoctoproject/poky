# This is a single Makefile to handle all generated Yocto Project documents.
# The Makefile needs to live in the documents directory and all figures used
# in any manuals must be PNG files and live in the individual book's figures
# directory.
#
# The Makefile has these targets:
#
#    pdf: generates a PDF version of a manual.  Not valid for the Quick Start
#    html: generates an HTML version of a manual.
#    tarball: creates a tarball for the doc files.
#    validate: validates 
#    publish: pushes generated files to the Yocto Project website
#    clean: removes files
#
# The Makefile generates an HTML and PDF version of every document except the
# Yocto Project Quick Start.  The Quick Start is in HTML form only.  The variable
# The command-line argument DOC represents the folder name in which a particular 
# document is stored.  The command-line argument VER represents the distro 
# version of the Yocto Release for which the manuals are being generated.
# You must invoke the Makefile with the DOC and VER arguments.
# Examples:
#
#     make DOC=bsp-guide VER=1.1
#     make DOC=yocto-project-qs VER=1.1
#     make pdf DOC=yocto-project-qs VER=1.1
#
# The first example generates the HTML and PDF versions of the BSP Guide for 
# the Yocto Project 1.1 Release.  The second example generates the HTML version
# of the Quick Start.  The third example generates an error because you cannot
# generate a PDF version of the Quick Start.
#
# Use the publish target to push the generated manuals to the Yocto Project 
# website.  All files needed for the manual's HTML form are pushed as well as the 
# PDF version (if applicable).  
# Examples:
#
#    make publish DOC=bsp-guide VER=1.1
#    make publish DOC=adt-manual VER=1.1
#

ifeq ($(DOC),bsp-guide)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = style.css bsp-guide.html bsp-guide.pdf figures/bsp-title.png
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css

endif

ifeq ($(DOC),dev-manual)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = style.css dev-manual.html dev-manual.pdf figures/dev-title.png figures/bsp-dev-flow.png \
           figures/index-downloads.png figures/kernel-example-repos.png figures/source-repos.png \
           figures/yp-download.png figures/git-workflow.png figures/kernel-dev-flow.png
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css

endif

ifeq ($(DOC),yocto-project-qs)
XSLTOPTS = --stringparam html.stylesheet style.css \
           --xinclude
ALLPREQ = html tarball
TARFILES = yocto-project-qs.html style.css figures/yocto-environment.png figures/building-an-image.png figures/using-a-pre-built-image.png figures/yocto-project-transp.png
MANUALS = $(DOC)/$(DOC).html
FIGURES = figures
STYLESHEET = $(DOC)/*.css
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
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css
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
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css
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
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css
endif


##
# These URI should be rewritten by your distribution's xml catalog to
# match your localy installed XSL stylesheets.
XSL_BASE_URI  = http://docbook.sourceforge.net/release/xsl/current
XSL_XHTML_URI = $(XSL_BASE_URI)/xhtml/docbook.xsl

all: $(ALLPREQ)

pdf:
ifeq ($(DOC),yocto-project-qs)
	@echo " "
	@echo "ERROR: You cannot generate a PDF file for the Yocto Project Quick Start"
	@echo " "
else
	cd $(DOC); ../tools/poky-docbook-to-pdf $(DOC).xml ../template; cd ..
endif
    
html:
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	cd $(DOC); xsltproc $(XSLTOPTS) -o $(DOC).html $(DOC)-customization.xsl $(DOC).xml; cd ..

tarball: html
	cd $(DOC); tar -cvzf $(DOC).tgz $(TARFILES); cd ..

validate:
	cd $(DOC); xmllint --postvalid --xinclude --noout $(DOC).xml; cd ..


publish:
	scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)
	cd $(DOC); scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)/figures

clean:
	rm -f $(MANUALS)
