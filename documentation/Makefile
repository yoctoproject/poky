# This is a single Makefile to handle all generated Yocto Project documents.
# The Makefile needs to live in the documents directory and all figures used
# in any manuals must be .PNG files and live in the individual book's figures
# directory as well as in the figures directory for the mega-manual.  
# Note that the figures for the Yocto Project Development Manual
# differ depending on the BRANCH being built.
#
# The Makefile has these targets:
#
#    pdf:      generates a PDF version of a manual.  Not valid for the Quick Start
#              or the mega-manual (single, large HTML file comprised of all 
#              Yocto Project manuals).
#    html:     generates an HTML version of a manual.
#    tarball:  creates a tarball for the doc files.
#    validate: validates 
#    publish:  pushes generated files to the Yocto Project website
#    clean:    removes files
#
# The Makefile generates an HTML and PDF version of every document except the
# Yocto Project Quick Start and the single, HTML mega-manual, which is comprised
# of all the individual Yocto Project manuals.  These two manuals are in HTML 
# form only.  The variable DOC indicates the folder name for a given manual. The 
# variable VER represents the distro version of the Yocto Release for which the 
# manuals are being generated.  The variable BRANCH is used to indicate the 
# branch (edison or denzil) and is used only when DOC=dev-manual or 
# DOC=mega-manual.  If you do not specify a BRANCH, the default branch used 
# will be for the latest Yocto Project release.  If you build for either 
# edison or denzil, you must use BRANCH. You do not need to use BRANCH for
# any release beyond denzil.  
#
# To build a manual, you must invoke Makefile with the DOC argument.  If you 
# are going to publish the manual, then you must invoke Makefile with both the 
# DOC and the VER argument.  Furthermore, if you are building or publishing
# the edison or denzil versions of the Yocto Poject Development Manual or 
# the mega-manual, you must also use the BRANCH argument.  
#
# Examples:
#
#     make DOC=bsp-guide
#     make DOC=yocto-project-qs
#     make pdf DOC=poky-ref-manual
#     make DOC=dev-manual BRANCH=edison
#     make DOC=mega-manual BRANCH=denzil
#
# The first example generates the HTML and PDF versions of the BSP Guide.
# The second example generates the HTML version only of the Quick Start.  Note that 
# the Quick Start only has an HTML version available.  The third example generates 
# both the PDF and HTML versions of the Yocto Project Reference Manual. The 
# fourth example generates both the PDF and HTML 'edison' versions of the YP 
# Development Manual.  The last exmample generates the HTML version of the 
# mega-manual and uses the 'denzil' branch when choosing figures for the 
# tarball of figures.  Any example that does not use the BRANCH argument 
# builds the current version of the manual set.
#
# Use the publish target to push the generated manuals to the Yocto Project 
# website.  All files needed for the manual's HTML form are pushed as well as the 
# PDF version (if applicable).  
# Examples:
#
#    make publish DOC=bsp-guide VER=1.3
#    make publish DOC=adt-manual VER=1.3
#    make publish DOC=dev-manual VER=1.1.1 BRANCH=edison
#    make publish DOC=dev-manual VER=1.2 BRANCH=denzil 
#
# The first example publishes the 1.3 version of both the PDF and HTML versions of 
# the BSP Guide.  The second example publishes the 1.3 version of both the PDF and 
# HTML versions of the ADT Manual. The third example publishes the PDF and HTML
# 'edison' versions of the YP Development Manual.  The fourth example publishes
# the PDF and HTML 'denzil' versions of the YP Development Manual.
#

ifeq ($(DOC),bsp-guide)
XSLTOPTS = --stringparam html.stylesheet bsp-style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = bsp-style.css bsp-guide.html bsp-guide.pdf figures/bsp-title.png
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css

endif

ifeq ($(DOC),dev-manual)
XSLTOPTS = --stringparam html.stylesheet dev-style.css \
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
TARFILES = dev-style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-example-repos-edison.png \
           figures/kernel-overview-1.png figures/kernel-overview-2.png \
           figures/kernel-overview-3-edison.png \
           figures/source-repos.png figures/yp-download.png \
           figures/wip.png
	else ifeq ($(BRANCH),denzil)
TARFILES = dev-style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-example-repos-denzil.png \
           figures/kernel-overview-1.png figures/kernel-overview-2.png \
           figures/kernel-overview-3-denzil.png \
           figures/source-repos.png figures/yp-download.png \
           figures/wip.png
        else
TARFILES = dev-style.css dev-manual.html dev-manual.pdf \
           figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
           figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
           figures/kernel-overview-1.png figures/kernel-overview-2-generic.png \
           figures/source-repos.png figures/yp-download.png
	endif

MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css

endif

ifeq ($(DOC),yocto-project-qs)
XSLTOPTS = --stringparam html.stylesheet qs-style.css \
           --xinclude
ALLPREQ = html tarball
TARFILES = yocto-project-qs.html qs-style.css figures/yocto-environment.png figures/building-an-image.png figures/using-a-pre-built-image.png figures/yocto-project-transp.png
MANUALS = $(DOC)/$(DOC).html
FIGURES = figures
STYLESHEET = $(DOC)/*.css
endif

ifeq ($(DOC),mega-manual)
XSLTOPTS = --stringparam html.stylesheet mega-style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html tarball

	ifeq ($(BRANCH),edison)
TARFILES = mega-manual.html mega-style.css figures/yocto-environment.png figures/building-an-image.png  \
	figures/using-a-pre-built-image.png \
	figures/poky-title.png \
	figures/adt-title.png figures/bsp-title.png \
	figures/kernel-title.png figures/kernel-architecture-overview.png \
	figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
	figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
	figures/kernel-example-repos-edison.png \
	figures/kernel-overview-1.png figures/kernel-overview-2.png \
	figures/kernel-overview-3-edison.png \
	figures/source-repos.png figures/yp-download.png \
	figures/wip.png
	else ifeq ($(BRANCH),denzil)
TARFILES = mega-manual.html mega-style.css figures/yocto-environment.png figures/building-an-image.png  \
	figures/using-a-pre-built-image.png \
	figures/poky-title.png \
	figures/adt-title.png figures/bsp-title.png \
	figures/kernel-title.png figures/kernel-architecture-overview.png \
	figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
	figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
	figures/kernel-example-repos-denzil.png \
	figures/kernel-overview-1.png figures/kernel-overview-2.png \
	figures/kernel-overview-3-denzil.png \
	figures/source-repos.png figures/yp-download.png \
	figures/wip.png
        else
TARFILES = mega-manual.html mega-style.css figures/yocto-environment.png figures/building-an-image.png  \
	figures/using-a-pre-built-image.png \
	figures/poky-title.png \
	figures/adt-title.png figures/bsp-title.png \
	figures/kernel-title.png figures/kernel-architecture-overview.png \
	figures/app-dev-flow.png figures/bsp-dev-flow.png figures/dev-title.png \
	figures/git-workflow.png figures/index-downloads.png figures/kernel-dev-flow.png \
	figures/kernel-overview-1.png figures/kernel-overview-2-generic.png \
	figures/source-repos.png figures/yp-download.png
	endif

MANUALS = $(DOC)/$(DOC).html
FIGURES = figures
STYLESHEET = $(DOC)/*.css

endif

ifeq ($(DOC),poky-ref-manual)
XSLTOPTS = --stringparam html.stylesheet ref-style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = poky-ref-manual.html ref-style.css figures/poky-title.png
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css
endif


ifeq ($(DOC),adt-manual)
XSLTOPTS = --stringparam html.stylesheet adt-style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = adt-manual.html adt-manual.pdf adt-style.css figures/adt-title.png
MANUALS = $(DOC)/$(DOC).html $(DOC)/$(DOC).pdf
FIGURES = figures
STYLESHEET = $(DOC)/*.css
endif

ifeq ($(DOC),kernel-manual)
XSLTOPTS = --stringparam html.stylesheet kernel-style.css \
           --stringparam  chapter.autolabel 1 \
           --stringparam  appendix.autolabel A \
           --stringparam  section.autolabel 1 \
           --stringparam  section.label.includes.component.label 1 \
           --xinclude
ALLPREQ = html pdf tarball
TARFILES = kernel-manual.html kernel-manual.pdf kernel-style.css figures/kernel-title.png figures/kernel-architecture-overview.png
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
	@echo "ERROR: You cannot generate a yocto-project-qs PDF file."
	@echo " "

else ifeq ($(DOC),mega-manual)
	@echo " "
	@echo "ERROR: You cannot generate a mega-manual PDF file."
	@echo " "

else

	cd $(DOC); ../tools/poky-docbook-to-pdf $(DOC).xml ../template; cd ..
endif
    
html:
ifeq ($(DOC),mega-manual)
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	@echo " "
	@echo "******** Building "$(DOC)
	@echo " "
	cd $(DOC); xsltproc $(XSLTOPTS) -o $(DOC).html $(DOC)-customization.xsl $(DOC).xml; cd ..
	@echo " "
	@echo "******** Using mega-manual.sed to process external links"
	@echo " "
	cd $(DOC); sed -f ../tools/mega-manual.sed < mega-manual.html > mega-output.html; cd ..
	@echo " "
	@echo "******** Cleaning up transient file mega-output.html"
	@echo " "
	cd $(DOC); rm mega-manual.html; mv mega-output.html mega-manual.html; cd ..
else
#       See http://www.sagehill.net/docbookxsl/HtmlOutput.html 
	@echo " "
	@echo "******** Building "$(DOC)
	@echo " "
	cd $(DOC); xsltproc $(XSLTOPTS) -o $(DOC).html $(DOC)-customization.xsl $(DOC).xml; cd ..
endif


tarball: html
	@echo " "
	@echo "******** Creating Tarball of document files"
	@echo " "
	cd $(DOC); tar -cvzf $(DOC).tgz $(TARFILES); cd ..

validate:
	cd $(DOC); xmllint --postvalid --xinclude --noout $(DOC).xml; cd ..


publish:
	@if test -f $(DOC)/$(DOC).html; \
	  then \
            echo " "; \
            echo "******** Publishing "$(DOC)".html"; \
            echo " "; \
            scp -r $(MANUALS) $(STYLESHEET) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC); \
            cd $(DOC); scp -r $(FIGURES) www.yoctoproject.org:/srv/www/www.yoctoproject.org-docs/$(VER)/$(DOC); \
	else \
          echo " "; \
          echo $(DOC)".html missing.  Generate the file first then try again."; \
          echo " "; \
	fi

clean:
	rm -f $(MANUALS)
