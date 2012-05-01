# This is a single Makefile to handle all generated Yocto Project documents.
# The Makefile needs to live in the documents directory and all figures used
# in any manuals must be .PNG files and live in the individual book's figures
# directory.  Note that the figures for the Yocto Project Development Manual
# differ between the 'master' and 'edison' branches.
#
# The Makefile has these targets:
#
#    pdf:      generates a PDF version of a manual.  Not valid for the Quick Start
#    html:     generates an HTML version of a manual.
#    tarball:  creates a tarball for the doc files.
#    validate: validates 
#    publish:  pushes generated files to the Yocto Project website
#    clean:    removes files
#
# The Makefile generates an HTML and PDF version of every document except the
# Yocto Project Quick Start.  The Quick Start is in HTML form only.  The variable
# DOC is used to indicate the folder name for a given manual. The variable
# VER represents the distro version of the Yocto Release for which the manuals 
# are being generated.  The variable BRANCH is used to indicate the 'edison'
# branch and is used only when DOC=dev-manual (making the YP Development
# Manual).  
#
# To build the HTML and PDF versions of the manual you must invoke the Makefile
# with the DOC argument.  If you are going to publish the manual then you 
# you must invoke the Makefile with both the DOC and the VER argument.
# If you are building the 'edison' version of the YP DEvelopment Manual then
# you must use the DOC and BRANCH arguments.  
#
# Examples:
#
#     make DOC=bsp-guide
#     make DOC=yocto-project-qs
#     make pdf DOC=poky-ref-manual
#     make DOC=dev-manual BRANCH=edison
#
# The first example generates the HTML and PDF versions of the BSP Guide.
# The second example generates the HTML version only of the Quick Start.  Note that 
# the Quick Start only has an HTML version available.  The third example generates 
# both the PDF and HTML versions of the Yocto Project Reference Manual. The 
# last example generates both the PDF and HTML 'edison' versions of the YP 
# Development Manual.
#
# Use the publish target to push the generated manuals to the Yocto Project 
# website.  All files needed for the manual's HTML form are pushed as well as the 
# PDF version (if applicable).  
# Examples:
#
#    make publish DOC=bsp-guide VER=1.2
#    make publish DOC=adt-manual VER=1.2
#    make publish DOC=dev-manual VER=1.1.1 BRANCH=edison
#    make publish DOC=dev-manual VER=1.2 
#
# The first example publishes the 1.2 version of both the PDF and HTML versions of 
# the BSP Guide.  The second example publishes the 1.2 version of both the PDF and 
# HTML versions of the ADT Manual. The third example publishes the PDF and HTML
# 'edison' versions of the YP Development Manual.  Finally, the last example publishes
# the PDF and HTML 'master' versions of the YP Development Manual. 
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
#
# Note that the tarfile might produce the "Cannot stat: No such file or directory" error
# message for .PNG files that are not present when building a particular branch.  The 
# list of files is all-inclusive for all branches.  Note, if you don't provide a BRANCH
# option, it defaults to the latest stuff.  This would be appropriate for "master" branch.
#

	ifeq ($(BRANCH),edison)
TARFILES = style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-example-repos-edison.png \
           figures/kernel-overview-1.png figures/kernel-overview-2.png \
           figures/kernel-overview-3-edison.png \
           figures/source-repos.png figures/yp-download.png \
           figures/wip.png
	else ifeq ($(BRANCH),denzil)
TARFILES = style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-example-repos-denzil.png \
           figures/kernel-overview-1.png figures/kernel-overview-2.png \
           figures/kernel-overview-3-denzil.png \
           figures/source-repos.png figures/yp-download.png \
           figures/wip.png
        else
TARFILES = style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-example-repos-denzil.png \
           figures/kernel-overview-1.png figures/kernel-overview-2.png \
           figures/kernel-overview-3-denzil.png \
           figures/source-repos.png figures/yp-download.png \
           figures/wip.png
	endif

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
TARFILES = poky-ref-manual.html style.css figures/poky-title.png
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
	cd $(DOC); scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC)

clean:
	rm -f $(MANUALS)
